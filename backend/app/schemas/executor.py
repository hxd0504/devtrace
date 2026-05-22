from pydantic import BaseModel


class ExecutorRecommendation(BaseModel):
    name: str
    type: str
    score: float
