"""
形态学变换相关的图像处理器
"""
import cv2
import numpy as np
from typing import List
from src.models.image_processor import ImageProcessor, ProcessorParameter


class ErosionProcessor(ImageProcessor):
    """腐蚀处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "erosion"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行腐蚀处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="kernel_size",
                type="int",
                description="结构元素大小",
                required=False,
                min_value=3,
                max_value=21,
                step=2,
                default=3
            ),
            ProcessorParameter(
                name="iterations",
                type="int",
                description="迭代次数",
                required=False,
                min_value=1,
                max_value=10,
                default=1
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        kernel_size = kwargs.get("kernel_size", 3)
        iterations = kwargs.get("iterations", 1)
        
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.erode(src=image, kernel=kernel, iterations=iterations)


class DilationProcessor(ImageProcessor):
    """膨胀处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "dilation"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行膨胀处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="kernel_size",
                type="int",
                description="结构元素大小",
                required=False,
                min_value=3,
                max_value=21,
                step=2,
                default=3
            ),
            ProcessorParameter(
                name="iterations",
                type="int",
                description="迭代次数",
                required=False,
                min_value=1,
                max_value=10,
                default=1
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        kernel_size = kwargs.get("kernel_size", 3)
        iterations = kwargs.get("iterations", 1)
        
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        return cv2.dilate(src=image, kernel=kernel, iterations=iterations)


class MorphologyExProcessor(ImageProcessor):
    """形态学操作处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "morphology_ex"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行形态学操作处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="operation",
                type="str",
                description="操作类型，可选值：open, close, gradient, tophat, blackhat",
                required=True
            ),
            ProcessorParameter(
                name="kernel_size",
                type="int",
                description="结构元素大小",
                required=False,
                min_value=3,
                max_value=21,
                step=2,
                default=5
            ),
            ProcessorParameter(
                name="convert_to_gray",
                type="bool",
                description="是否转换为灰度图",
                required=False,
                default=False
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        operation_str = kwargs.get("operation", "open").lower()
        kernel_size = kwargs.get("kernel_size", 5)
        convert_to_gray = kwargs.get("convert_to_gray", False)
        
        # 定义操作类型映射
        operation_map = {
            "open": cv2.MORPH_OPEN,
            "close": cv2.MORPH_CLOSE,
            "gradient": cv2.MORPH_GRADIENT,
            "tophat": cv2.MORPH_TOPHAT,
            "blackhat": cv2.MORPH_BLACKHAT
        }
        
        if operation_str not in operation_map:
            raise ValueError(f"不支持的操作: {operation_str}")
        
        operation = operation_map[operation_str]
        
        # 创建结构元素
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        
        # 如果需要转换为灰度图
        if convert_to_gray and len(image.shape) == 3 and image.shape[2] == 3:
            image_gray = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)
            return cv2.morphologyEx(src=image_gray, op=operation, kernel=kernel)
        else:
            return cv2.morphologyEx(src=image, op=operation, kernel=kernel)


class ThresholdProcessor(ImageProcessor):
    """阈值处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "threshold"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行阈值处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="threshold",
                type="int",
                description="阈值",
                required=False,
                min_value=0,
                max_value=255,
                default=128
            ),
            ProcessorParameter(
                name="max_value",
                type="int",
                description="最大值",
                required=False,
                min_value=0,
                max_value=255,
                default=255
            ),
            ProcessorParameter(
                name="threshold_type",
                type="str",
                description="阈值类型，可选值：binary, binary_inv, trunc, tozero, tozero_inv",
                required=False,
                default="binary"
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        threshold = kwargs.get("threshold", 128)
        max_value = kwargs.get("max_value", 255)
        threshold_type_str = kwargs.get("threshold_type", "binary").lower()
        
        # 定义阈值类型映射
        threshold_type_map = {
            "binary": cv2.THRESH_BINARY,
            "binary_inv": cv2.THRESH_BINARY_INV,
            "trunc": cv2.THRESH_TRUNC,
            "tozero": cv2.THRESH_TOZERO,
            "tozero_inv": cv2.THRESH_TOZERO_INV
        }
        
        if threshold_type_str not in threshold_type_map:
            raise ValueError(f"不支持的阈值类型: {threshold_type_str}")
        
        threshold_type = threshold_type_map[threshold_type_str]
        
        # 如果是彩色图像，转换为灰度图
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_gray = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(src=image_gray, thresh=threshold, maxval=max_value, type=threshold_type)
            return thresh
        else:
            _, thresh = cv2.threshold(src=image, thresh=threshold, maxval=max_value, type=threshold_type)
            return thresh 