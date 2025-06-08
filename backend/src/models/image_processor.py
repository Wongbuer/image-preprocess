"""
图像处理基类模块，定义所有图像预处理操作的抽象接口
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple, Union
import numpy as np
from pydantic import BaseModel, Field


class ProcessorParameter(BaseModel):
    """处理器参数模型"""
    name: str
    type: str
    required: bool = True
    description: str
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    step: Optional[Union[int, float]] = None
    default: Optional[Any] = None


class ImageProcessor(ABC):
    """图像处理器基类"""
    
    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """处理器名称"""
        pass
    
    @classmethod
    @abstractmethod
    def description(cls) -> str:
        """处理器描述"""
        pass
    
    @classmethod
    @abstractmethod
    def parameters(cls) -> List[ProcessorParameter]:
        """处理器参数列表"""
        pass
    
    @abstractmethod
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        """
        处理图像
        
        Args:
            image: 输入图像
            **kwargs: 处理参数
            
        Returns:
            处理后的图像
        """
        pass
    
    @classmethod
    def validate_parameters(cls, **kwargs) -> Dict[str, Any]:
        """
        验证参数
        
        Args:
            **kwargs: 处理参数
            
        Returns:
            验证后的参数
            
        Raises:
            ValueError: 参数验证失败
        """
        params = cls.parameters()
        validated_params = {}
        
        # 检查必填参数
        for param in params:
            if param.required and param.name not in kwargs:
                raise ValueError(f"缺少必填参数: {param.name}")
            
            if param.name in kwargs:
                value = kwargs[param.name]
                
                # 检查类型
                if param.type == "int" and not isinstance(value, int):
                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        raise ValueError(f"参数 {param.name} 必须是整数")
                
                elif param.type == "float" and not isinstance(value, float):
                    try:
                        value = float(value)
                    except (ValueError, TypeError):
                        raise ValueError(f"参数 {param.name} 必须是浮点数")
                
                # 检查范围
                if param.min_value is not None and value < param.min_value:
                    raise ValueError(f"参数 {param.name} 必须大于等于 {param.min_value}")
                
                if param.max_value is not None and value > param.max_value:
                    raise ValueError(f"参数 {param.name} 必须小于等于 {param.max_value}")
                
                validated_params[param.name] = value
            else:
                # 使用默认值
                if param.default is not None:
                    validated_params[param.name] = param.default
        
        return validated_params 