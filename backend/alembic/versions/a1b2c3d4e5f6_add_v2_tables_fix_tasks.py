"""add v2 tables fix tasks

Revision ID: a1b2c3d4e5f6
Revises: 22ad1b827307
Create Date: 2026-05-25 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '22ad1b827307'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. 创建 conversations 表
    op.create_table('conversations',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('workspace_id', sa.BigInteger(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('source', sa.String(length=20), server_default='devtrace', nullable=True),
        sa.Column('created_by', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # 2. 创建 messages 表
    op.create_table('messages',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('conversation_id', sa.BigInteger(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('message_type', sa.String(length=20), server_default='text', nullable=True),
        sa.Column('extra_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_messages_conversation', 'messages', ['conversation_id'], unique=False)

    # 3. 创建 ai_tags 表
    op.create_table('ai_tags',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('ai_tool', sa.String(length=50), nullable=False),
        sa.Column('workspace_id', sa.BigInteger(), nullable=False),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('stats', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ai_tool', 'workspace_id', name='uq_ai_tags_tool_workspace')
    )

    # 4. 创建 dispatch_records 表
    op.create_table('dispatch_records',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('task_id', sa.BigInteger(), nullable=True),
        sa.Column('ai_tool', sa.String(length=50), nullable=False),
        sa.Column('dispatch_reason', sa.Text(), nullable=True),
        sa.Column('risk_level', sa.String(length=20), nullable=True),
        sa.Column('execution_prompt', sa.Text(), nullable=True),
        sa.Column('execution_result', sa.Text(), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('success', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_dispatch_task', 'dispatch_records', ['task_id'], unique=False)
    op.create_index('idx_dispatch_ai_tool', 'dispatch_records', ['ai_tool'], unique=False)

    # 5. 创建 thought_chains 表
    op.create_table('thought_chains',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('workspace_id', sa.BigInteger(), nullable=False),
        sa.Column('problem', sa.Text(), nullable=False),
        sa.Column('thought_chain', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('source', sa.Text(), server_default='auto_extract', nullable=True),
        sa.Column('related_issue_ids', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['workspace_id'], ['workspaces.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_thought_chains_workspace', 'thought_chains', ['workspace_id'], unique=False)

    # 6. 修复 tasks 表 schema drift
    op.drop_column('tasks', 'assignee_name')
    op.drop_column('tasks', 'evidence_note')
    op.add_column('tasks', sa.Column('owner_name', sa.String(length=100), nullable=True))
    op.add_column('tasks', sa.Column('evidence_source', sa.Text(), nullable=True))
    op.add_column('tasks', sa.Column('evidence_summary', sa.Text(), nullable=True))
    op.add_column('tasks', sa.Column('acceptance_criteria', sa.Text(), nullable=True))
    op.add_column('tasks', sa.Column('risk_level', sa.String(length=20), nullable=True))
    op.create_check_constraint('ck_tasks_risk_level', 'tasks', "risk_level IN ('low', 'medium', 'high')")


def downgrade() -> None:
    # 撤销 tasks 表 schema drift
    op.drop_constraint('ck_tasks_risk_level', 'tasks', type_='check')
    op.drop_column('tasks', 'risk_level')
    op.drop_column('tasks', 'acceptance_criteria')
    op.drop_column('tasks', 'evidence_summary')
    op.drop_column('tasks', 'evidence_source')
    op.drop_column('tasks', 'owner_name')
    op.add_column('tasks', sa.Column('evidence_note', sa.Text(), nullable=True))
    op.add_column('tasks', sa.Column('assignee_name', sa.String(length=100), nullable=True))

    # 删除 thought_chains 表
    op.drop_index('idx_thought_chains_workspace', table_name='thought_chains')
    op.drop_table('thought_chains')

    # 删除 dispatch_records 表
    op.drop_index('idx_dispatch_ai_tool', table_name='dispatch_records')
    op.drop_index('idx_dispatch_task', table_name='dispatch_records')
    op.drop_table('dispatch_records')

    # 删除 ai_tags 表
    op.drop_table('ai_tags')

    # 删除 messages 表
    op.drop_index('idx_messages_conversation', table_name='messages')
    op.drop_table('messages')

    # 删除 conversations 表
    op.drop_table('conversations')
