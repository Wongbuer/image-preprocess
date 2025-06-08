"""
FastAPI应用实例
"""
from fastapi import FastAPI
from src.middlewares.cors import setup_cors
from src.controllers.health_controller import router as health_router
from src.controllers.image_controller import router as image_router

# 导入处理器包以确保处理器注册
import src.models.processors


def create_app() -> FastAPI:
    """
    创建FastAPI应用实例
    
    Returns:
        FastAPI应用实例
    """
    app = FastAPI(
        title="图像预处理应用",
        description="一个基于FastAPI的图像预处理应用，提供多种图像处理功能",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )
    
    # 设置CORS
    setup_cors(app)
    
    # 注册路由
    register_routers(app)
    
    return app


def register_routers(app: FastAPI) -> None:
    """
    注册路由
    
    Args:
        app: FastAPI应用实例
    """
    # 注册健康检查路由
    app.include_router(health_router)
    
    # 注册图像处理路由
    app.include_router(image_router)
    
    # 在这里可以注册更多路由
    # app.include_router(other_router) 