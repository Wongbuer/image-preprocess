"""
用户控制器，处理用户相关的HTTP请求
"""
from fastapi import APIRouter, HTTPException
from src.entity.user import User
from src.services.user_service import UserService


# 创建路由
router = APIRouter(prefix="/api/users", tags=["users"])
user_service = UserService()


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """
    获取用户信息
    
    Args:
        user_id: 用户ID
        
    Returns:
        用户信息
    """
    try:
        return user_service.get_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=User)
async def create_user(user: User):
    """
    创建用户
    
    Args:
        user: 用户信息
        
    Returns:
        创建后的用户信息
    """
    try:
        return user_service.create_user(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 