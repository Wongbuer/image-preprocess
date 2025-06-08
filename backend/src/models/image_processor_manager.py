"""
图像处理器管理模块，负责注册和获取图像处理器
"""
from typing import Dict, Type, List, Any, Optional
import numpy as np
from src.models.image_processor import ImageProcessor


class ImageProcessorManager:
    """图像处理器管理器"""
    _processors: Dict[str, Type[ImageProcessor]] = {}
    
    @classmethod
    def register(cls, processor_class: Type[ImageProcessor]) -> None:
        """
        注册处理器
        
        Args:
            processor_class: 处理器类
        """
        processor_name = processor_class.name()
        cls._processors[processor_name] = processor_class
    
    @classmethod
    def get_processor(cls, name: str) -> Optional[Type[ImageProcessor]]:
        """
        获取处理器
        
        Args:
            name: 处理器名称
            
        Returns:
            处理器类，若不存在则返回None
        """
        return cls._processors.get(name)
    
    @classmethod
    def list_processors(cls) -> List[Dict[str, Any]]:
        """
        列出所有处理器
        
        Returns:
            处理器信息列表
        """
        return [
            {
                "name": processor.name(),
                "description": processor.description(),
                "parameters": [param.dict() for param in processor.parameters()]
            }
            for processor in cls._processors.values()
        ]
    
    @classmethod
    def process_image(cls, name: str, image: np.ndarray, **kwargs) -> np.ndarray:
        """
        处理图像
        
        Args:
            name: 处理器名称
            image: 输入图像
            **kwargs: 处理参数
            
        Returns:
            处理后的图像
            
        Raises:
            ValueError: 处理器不存在
        """
        processor_class = cls.get_processor(name)
        if not processor_class:
            raise ValueError(f"处理器不存在: {name}")
        
        # 验证参数
        validated_params = processor_class.validate_parameters(**kwargs)
        
        # 创建处理器实例并处理图像
        processor = processor_class()
        return processor.process(image, **validated_params) 