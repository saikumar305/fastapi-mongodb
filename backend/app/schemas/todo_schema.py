from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.models.user_model import User

class TodoCreate(BaseModel):
    title: str = Field(..., title='Title', max_length=55, min_length=1)
    content: str = Field(..., title='Title', max_length=755, min_length=1)
    status: Optional[bool] = False
    
    
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(..., title='Title', max_length=55, min_length=1)
    content: Optional[str] = Field(..., title='Title', max_length=755, min_length=1)
    status: Optional[bool] = False
    

class TodoOut(BaseModel):
    todo_id: UUID
    status: bool
    title: str
    content: str
    created_at: datetime
    updated_at: datetime