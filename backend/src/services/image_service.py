"""
图像处理服务
"""
import cv2
import numpy as np
import os
import base64
from typing import Dict, Any, List, Optional, Union, Tuple
import tempfile
from src.models.image_processor_manager import ImageProcessorManager
# 确保处理器被注册
import src.models.processors


class ImageService:
    """图像处理服务"""
    
    @staticmethod
    def list_processors() -> List[Dict[str, Any]]:
        """
        列出所有可用的图像处理器
        
        Returns:
            处理器信息列表
        """
        return ImageProcessorManager.list_processors()
    
    @staticmethod
    def process_image(processor_name: str, image_data: str, params: Dict[str, Any] = None) -> str:
        """
        处理图像
        
        Args:
            processor_name: 处理器名称
            image_data: Base64编码的图像数据
            params: 处理参数
            
        Returns:
            Base64编码的处理后图像数据
            
        Raises:
            ValueError: 处理器不存在或处理失败
        """
        if params is None:
            params = {}
        
        # 解码图像
        try:
            # 移除Base64前缀（如果有）
            if "base64," in image_data:
                image_data = image_data.split("base64,")[1]
            
            # 解码Base64
            image_bytes = base64.b64decode(image_data)
            
            # 创建临时文件保存图像
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(image_bytes)
                temp_file_path = temp_file.name
            
            # 读取图像
            image = cv2.imread(temp_file_path)
            
            # 删除临时文件
            os.unlink(temp_file_path)
            
            if image is None:
                raise ValueError("无法解码图像数据")
        except Exception as e:
            raise ValueError(f"图像数据解析失败: {str(e)}")
        
        # 处理图像
        processed_image = ImageProcessorManager.process_image(processor_name, image, **params)
        
        # 编码处理后的图像
        try:
            # 创建临时文件保存处理后的图像
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                cv2.imwrite(temp_file.name, processed_image)
                temp_file_path = temp_file.name
            
            # 读取处理后的图像并进行Base64编码
            with open(temp_file_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            
            # 删除临时文件
            os.unlink(temp_file_path)
            
            return encoded_image
        except Exception as e:
            raise ValueError(f"图像编码失败: {str(e)}")
    
    @staticmethod
    def batch_process_image(processor_names: List[str], image_data: str, params_list: List[Dict[str, Any]] = None) -> str:
        """
        批量处理图像
        
        Args:
            processor_names: 处理器名称列表
            image_data: Base64编码的图像数据
            params_list: 处理参数列表
            
        Returns:
            Base64编码的处理后图像数据
            
        Raises:
            ValueError: 处理器不存在或处理失败
        """
        if params_list is None:
            params_list = [{}] * len(processor_names)
        
        if len(processor_names) != len(params_list):
            raise ValueError("处理器名称列表与参数列表长度不匹配")
        
        # 解码图像
        try:
            # 移除Base64前缀（如果有）
            if "base64," in image_data:
                image_data = image_data.split("base64,")[1]
            
            # 解码Base64
            image_bytes = base64.b64decode(image_data)
            
            # 创建临时文件保存图像
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(image_bytes)
                temp_file_path = temp_file.name
            
            # 读取图像
            image = cv2.imread(temp_file_path)
            
            # 删除临时文件
            os.unlink(temp_file_path)
            
            if image is None:
                raise ValueError("无法解码图像数据")
        except Exception as e:
            raise ValueError(f"图像数据解析失败: {str(e)}")
        
        # 依次处理图像
        processed_image = image.copy()
        for processor_name, params in zip(processor_names, params_list):
            processed_image = ImageProcessorManager.process_image(processor_name, processed_image, **params)
        
        # 编码处理后的图像
        try:
            # 创建临时文件保存处理后的图像
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                cv2.imwrite(temp_file.name, processed_image)
                temp_file_path = temp_file.name
            
            # 读取处理后的图像并进行Base64编码
            with open(temp_file_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            
            # 删除临时文件
            os.unlink(temp_file_path)
            
            return encoded_image
        except Exception as e:
            raise ValueError(f"图像编码失败: {str(e)}") 