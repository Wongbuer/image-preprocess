"""
响应实体类，定义API响应格式
"""
from typing import Any, Dict, Optional
from pydantic import BaseModel


class ResponseModel(BaseModel):
    """响应模型"""
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None


def success_response(data: Any = None, message: str = "success") -> Dict[str, Any]:
    """
    成功响应
    
    Args:
        data: 响应数据
        message: 响应消息
        
    Returns:
        响应字典
    """
    return ResponseModel(code=200, message=message, data=data).dict()


def error_response(code: int = 500, message: str = "error") -> Dict[str, Any]:
    """
    错误响应
    
    Args:
        code: 错误码
        message: 错误消息
        
    Returns:
        响应字典
    """
    return ResponseModel(code=code, message=message).dict() 