"""
滤波相关的图像处理器
"""
import cv2
import numpy as np
from typing import List
from src.models.image_processor import ImageProcessor, ProcessorParameter


class MeanFilterProcessor(ImageProcessor):
    """均值滤波处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "mean_filter"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行均值滤波处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="kernel_size",
                type="int",
                description="滤波核大小",
                required=False,
                min_value=3,
                max_value=99,
                step=2,
                default=5
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        kernel_size = kwargs.get("kernel_size", 5)
        return cv2.blur(src=image, ksize=(kernel_size, kernel_size))


class GaussianFilterProcessor(ImageProcessor):
    """高斯滤波处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "gaussian_filter"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行高斯滤波处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="kernel_size",
                type="int",
                description="滤波核大小",
                required=False,
                min_value=3,
                max_value=99,
                step=2,
                default=9
            ),
            ProcessorParameter(
                name="sigma",
                type="float",
                description="高斯核标准差",
                required=False,
                min_value=0.1,
                max_value=10.0,
                step=0.1,
                default=1.5
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        kernel_size = kwargs.get("kernel_size", 9)
        sigma = kwargs.get("sigma", 1.5)
        return cv2.GaussianBlur(src=image, ksize=(kernel_size, kernel_size), sigmaX=sigma)


class MedianFilterProcessor(ImageProcessor):
    """中值滤波处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "median_filter"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行中值滤波处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="kernel_size",
                type="int",
                description="滤波核大小",
                required=False,
                min_value=3,
                max_value=99,
                step=2,
                default=5
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        kernel_size = kwargs.get("kernel_size", 5)
        return cv2.medianBlur(src=image, ksize=kernel_size)


class SobelFilterProcessor(ImageProcessor):
    """Sobel滤波处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "sobel_filter"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行Sobel滤波处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="dx",
                type="int",
                description="x方向的导数阶数",
                required=False,
                min_value=0,
                max_value=1,
                default=1
            ),
            ProcessorParameter(
                name="dy",
                type="int",
                description="y方向的导数阶数",
                required=False,
                min_value=0,
                max_value=1,
                default=0
            ),
            ProcessorParameter(
                name="kernel_size",
                type="int",
                description="滤波核大小",
                required=False,
                min_value=3,
                max_value=7,
                step=2,
                default=3
            ),
            ProcessorParameter(
                name="scale",
                type="float",
                description="缩放因子",
                required=False,
                min_value=0.1,
                max_value=10.0,
                step=0.1,
                default=0.4
            ),
            ProcessorParameter(
                name="delta",
                type="int",
                description="偏移量",
                required=False,
                min_value=0,
                max_value=255,
                default=128
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        dx = kwargs.get("dx", 1)
        dy = kwargs.get("dy", 0)
        kernel_size = kwargs.get("kernel_size", 3)
        scale = kwargs.get("scale", 0.4)
        delta = kwargs.get("delta", 128)
        
        # 转换为灰度图
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_gray = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)
        else:
            image_gray = image
        
        return cv2.Sobel(
            src=image_gray, 
            ddepth=cv2.CV_8U, 
            dx=dx, 
            dy=dy, 
            ksize=kernel_size, 
            scale=scale, 
            delta=delta, 
            borderType=cv2.BORDER_DEFAULT
        )


class CannyEdgeProcessor(ImageProcessor):
    """Canny边缘检测处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "canny_edge"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行Canny边缘检测处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="threshold1",
                type="int",
                description="第一个阈值",
                required=False,
                min_value=0,
                max_value=255,
                default=125
            ),
            ProcessorParameter(
                name="threshold2",
                type="int",
                description="第二个阈值",
                required=False,
                min_value=0,
                max_value=255,
                default=350
            ),
            ProcessorParameter(
                name="invert",
                type="bool",
                description="是否反转结果",
                required=False,
                default=True
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        threshold1 = kwargs.get("threshold1", 125)
        threshold2 = kwargs.get("threshold2", 350)
        invert = kwargs.get("invert", True)
        
        # 转换为灰度图
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_gray = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)
        else:
            image_gray = image
        
        edges = cv2.Canny(image=image_gray, threshold1=threshold1, threshold2=threshold2)
        
        if invert:
            return 255 - edges
        else:
            return edges


class PyramidFilterProcessor(ImageProcessor):
    """图像金字塔处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "pyramid_filter"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行金字塔降采样和上采样处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="operation",
                type="str",
                description="操作类型，可选值：down, up, both",
                required=False,
                default="both"
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        operation = kwargs.get("operation", "both").lower()
        
        if operation == "down":
            return cv2.pyrDown(src=image)
        elif operation == "up":
            return cv2.pyrUp(src=image)
        elif operation == "both":
            reduced = cv2.pyrDown(src=image)
            return cv2.pyrUp(src=reduced)
        else:
            raise ValueError(f"不支持的操作: {operation}")


class ResizeProcessor(ImageProcessor):
    """图像缩放处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "resize"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行缩放处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="scale",
                type="float",
                description="缩放比例",
                required=False,
                min_value=0.1,
                max_value=10.0,
                step=0.1,
                default=0.5
            ),
            ProcessorParameter(
                name="interpolation",
                type="str",
                description="插值方法，可选值：nearest, linear, cubic",
                required=False,
                default="cubic"
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        scale = kwargs.get("scale", 0.5)
        interpolation_str = kwargs.get("interpolation", "cubic").lower()
        
        interpolation_map = {
            "nearest": cv2.INTER_NEAREST,
            "linear": cv2.INTER_LINEAR,
            "cubic": cv2.INTER_CUBIC
        }
        
        interpolation = interpolation_map.get(interpolation_str, cv2.INTER_CUBIC)
        
        return cv2.resize(src=image, dsize=(0, 0), fx=scale, fy=scale, interpolation=interpolation) 