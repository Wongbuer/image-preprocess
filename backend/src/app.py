"""
FastAPI应用实例
"""
from fastapi import FastAPI
from src.middlewares.cors import setup_cors
from src.controllers.user_controller import router as user_router
from src.controllers.health_controller import router as health_router


def create_app() -> FastAPI:
    """
    创建FastAPI应用实例
    
    Returns:
        FastAPI应用实例
    """
    app = FastAPI(
        title="MVC后端应用",
        description="一个基于FastAPI的MVC后端应用",
        version="0.1.0",
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
    
    # 注册用户路由
    app.include_router(user_router)
    
    # 在这里可以注册更多路由
    # app.include_router(other_router) 