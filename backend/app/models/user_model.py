
from datetime import datetime
from typing import Optional
from uuid import UUID , uuid4
from beanie import Document,Indexed
from pydantic import Field, EmailStr


class User(Document):
    user_id : UUID =Field(default_factory=uuid4)
    username : Indexed(str ,unique =True)
    email : Indexed(EmailStr,unique=True)
    hashed_password : str
    first_name :Optional[str] = None
    last_name : Optional[str] = None
    disabled : Optional[bool] = None

    def __repr__(self) -> str:
        return f"<User {self.email}>"
    
    def __str__(self) -> str:
        return self.email
    
    def __hash__(self) -> int:
        return hash(self.email)
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, User):
            self.email == __value.email
        return False
    
    @property
    def create(self) -> datetime:
        return self.id.generation_time
    
    @classmethod
    async def by_email(self, email:str) -> "User":
        return await self.find_one(self.email == email)
    
    class Colection:
        name = "users"
