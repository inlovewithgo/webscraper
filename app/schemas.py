from pydantic import BaseModel
from typing import List, Any

class ScrapeRequest(BaseModel):
    url: str

class ScrapeResponse(BaseModel):
    task_id: int
    status: str

class ScrapeResultSchema(BaseModel):
    id: int
    task_id: int
    data: List[dict]

    class Config:
        from_attributes = True
