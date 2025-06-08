"""
图像增强相关的图像处理器
"""
import cv2
import numpy as np
from typing import List
from src.models.image_processor import ImageProcessor, ProcessorParameter


class RetinexSingleScaleProcessor(ImageProcessor):
    """单尺度Retinex处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "retinex_single_scale"
    
    @classmethod
    def description(cls) -> str:
        return "使用单尺度Retinex算法对图像进行增强"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="sigma",
                type="int",
                description="高斯核标准差",
                required=False,
                min_value=10,
                max_value=500,
                default=300
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        sigma = kwargs.get("sigma", 300)
        
        # 单尺度Retinex
        img = np.float64(image) + 1.0
        
        # 高斯模糊
        gaussian = cv2.GaussianBlur(img, (0, 0), sigma)
        gaussian = np.where(gaussian == 0, 0.01, gaussian)
        
        # 计算对数差
        retinex = np.log10(img) - np.log10(gaussian)
        
        # 转换到0-255范围
        for i in range(retinex.shape[2]):
            retinex[:, :, i] = (retinex[:, :, i] - np.min(retinex[:, :, i])) / \
                              (np.max(retinex[:, :, i]) - np.min(retinex[:, :, i])) * 255
        
        retinex = np.uint8(np.minimum(np.maximum(retinex, 0), 255))
        
        return retinex


class RetinexMultiScaleProcessor(ImageProcessor):
    """多尺度Retinex处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "retinex_multi_scale"
    
    @classmethod
    def description(cls) -> str:
        return "使用多尺度Retinex算法对图像进行增强"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="sigma_small",
                type="int",
                description="小尺度高斯核标准差",
                required=False,
                min_value=5,
                max_value=50,
                default=15
            ),
            ProcessorParameter(
                name="sigma_medium",
                type="int",
                description="中尺度高斯核标准差",
                required=False,
                min_value=50,
                max_value=200,
                default=80
            ),
            ProcessorParameter(
                name="sigma_large",
                type="int",
                description="大尺度高斯核标准差",
                required=False,
                min_value=200,
                max_value=500,
                default=250
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        sigma_small = kwargs.get("sigma_small", 15)
        sigma_medium = kwargs.get("sigma_medium", 80)
        sigma_large = kwargs.get("sigma_large", 250)
        
        sigma_list = [sigma_small, sigma_medium, sigma_large]
        
        # 多尺度Retinex
        img = np.float64(image) + 1.0
        retinex = np.zeros_like(img)
        
        for sigma in sigma_list:
            # 高斯模糊
            gaussian = cv2.GaussianBlur(img, (0, 0), sigma)
            gaussian = np.where(gaussian == 0, 0.01, gaussian)
            
            # 计算对数差
            retinex += np.log10(img) - np.log10(gaussian)
        
        # 平均
        retinex = retinex / len(sigma_list)
        
        # 转换到0-255范围
        for i in range(retinex.shape[2]):
            retinex[:, :, i] = (retinex[:, :, i] - np.min(retinex[:, :, i])) / \
                              (np.max(retinex[:, :, i]) - np.min(retinex[:, :, i])) * 255
        
        retinex = np.uint8(np.minimum(np.maximum(retinex, 0), 255))
        
        return retinex


class AutomaticWhiteBalanceProcessor(ImageProcessor):
    """自动白平衡处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "automatic_white_balance"
    
    @classmethod
    def description(cls) -> str:
        return "使用自动白平衡算法对图像进行增强"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return []
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        result = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        avg_a = np.average(result[:, :, 1])
        avg_b = np.average(result[:, :, 2])
        
        for x in range(result.shape[0]):
            for y in range(result.shape[1]):
                l, a, b = result[x, y, :]
                # fix for CV correction
                l *= 100 / 255.0
                result[x, y, 1] = a - ((avg_a - 128) * (l / 100.0) * 1.1)
                result[x, y, 2] = b - ((avg_b - 128) * (l / 100.0) * 1.1)
        
        return cv2.cvtColor(result, cv2.COLOR_LAB2BGR) 