"""
图像处理控制器
"""
from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from src.services.image_service import ImageService
from src.entity.response import success_response, error_response


# 定义请求和响应模型
class ProcessImageRequest(BaseModel):
    """处理图像请求模型"""
    processor_name: str = Field(..., description="处理器名称")
    image_data: str = Field(..., description="Base64编码的图像数据")
    params: Dict[str, Any] = Field(default={}, description="处理参数")


class BatchProcessImageRequest(BaseModel):
    """批量处理图像请求模型"""
    processor_names: List[str] = Field(..., description="处理器名称列表")
    image_data: str = Field(..., description="Base64编码的图像数据")
    params_list: List[Dict[str, Any]] = Field(default=None, description="处理参数列表")


# 创建路由
router = APIRouter(prefix="/api/image", tags=["image"])


@router.get("/processors")
async def list_processors():
    """
    列出所有可用的图像处理器
    
    Returns:
        处理器信息列表
    """
    try:
        processors = ImageService.list_processors()
        return success_response(data=processors)
    except Exception as e:
        return error_response(code=500, message=str(e))


@router.post("/process")
async def process_image(request: ProcessImageRequest = Body(...)):
    """
    处理图像
    
    Args:
        request: 处理图像请求
        
    Returns:
        处理后的图像数据
    """
    try:
        processed_image = ImageService.process_image(
            processor_name=request.processor_name,
            image_data=request.image_data,
            params=request.params
        )
        return success_response(data={"processed_image": processed_image})
    except ValueError as e:
        return error_response(code=400, message=str(e))
    except Exception as e:
        return error_response(code=500, message=str(e))


@router.post("/batch-process")
async def batch_process_image(request: BatchProcessImageRequest = Body(...)):
    """
    批量处理图像
    
    Args:
        request: 批量处理图像请求
        
    Returns:
        处理后的图像数据
    """
    try:
        processed_image = ImageService.batch_process_image(
            processor_names=request.processor_names,
            image_data=request.image_data,
            params_list=request.params_list
        )
        return success_response(data={"processed_image": processed_image})
    except ValueError as e:
        return error_response(code=400, message=str(e))
    except Exception as e:
        return error_response(code=500, message=str(e)) 