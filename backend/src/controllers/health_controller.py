"""
健康检查控制器
"""
from fastapi import APIRouter
from src.entity.response import success_response


# 创建路由
router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("")
async def health_check():
    """
    健康检查
    
    Returns:
        健康状态
    """
    return success_response(data={"status": "ok"}, message="服务正常运行") 