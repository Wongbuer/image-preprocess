"""
主入口文件，启动FastAPI应用
"""
import uvicorn
# 确保处理器被注册
import src.models.processors
from src.app import create_app

app = create_app()

if __name__ == "__main__":
    """
    直接运行此文件可以启动应用
    """
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
