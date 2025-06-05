"""
用户实体类
"""
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    """用户实体类"""
    id: Optional[int] = None
    username: str
    email: str 