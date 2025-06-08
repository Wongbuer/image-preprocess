"""
轮廓和边缘检测相关的图像处理器
"""
import cv2
import numpy as np
from typing import List, Tuple
from src.models.image_processor import ImageProcessor, ProcessorParameter


class ContourDetectionProcessor(ImageProcessor):
    """轮廓检测处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "contour_detection"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行轮廓检测处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="mode",
                type="str",
                description="轮廓检索模式，可选值：external, list, ccomp, tree",
                required=False,
                default="list"
            ),
            ProcessorParameter(
                name="method",
                type="str",
                description="轮廓近似方法，可选值：none, simple, tc89_l1, tc89_kcos",
                required=False,
                default="none"
            ),
            ProcessorParameter(
                name="color",
                type="str",
                description="轮廓颜色，格式为'R,G,B'",
                required=False,
                default="255,255,255"
            ),
            ProcessorParameter(
                name="thickness",
                type="int",
                description="轮廓线宽",
                required=False,
                min_value=1,
                max_value=10,
                default=2
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        mode_str = kwargs.get("mode", "list").lower()
        method_str = kwargs.get("method", "none").lower()
        color_str = kwargs.get("color", "255,255,255")
        thickness = kwargs.get("thickness", 2)
        
        # 定义模式映射
        mode_map = {
            "external": cv2.RETR_EXTERNAL,
            "list": cv2.RETR_LIST,
            "ccomp": cv2.RETR_CCOMP,
            "tree": cv2.RETR_TREE
        }
        
        # 定义方法映射
        method_map = {
            "none": cv2.CHAIN_APPROX_NONE,
            "simple": cv2.CHAIN_APPROX_SIMPLE,
            "tc89_l1": cv2.CHAIN_APPROX_TC89_L1,
            "tc89_kcos": cv2.CHAIN_APPROX_TC89_KCOS
        }
        
        if mode_str not in mode_map:
            raise ValueError(f"不支持的轮廓检索模式: {mode_str}")
        
        if method_str not in method_map:
            raise ValueError(f"不支持的轮廓近似方法: {method_str}")
        
        # 解析颜色
        try:
            r, g, b = map(int, color_str.split(","))
            color = (b, g, r)  # OpenCV使用BGR顺序
        except (ValueError, AttributeError):
            raise ValueError(f"颜色格式错误，应为'R,G,B': {color_str}")
        
        # 转换为灰度图
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_gray = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)
        else:
            image_gray = image
        
        # 检测轮廓
        contours, _ = cv2.findContours(
            image=image_gray, 
            mode=mode_map[mode_str], 
            method=method_map[method_str]
        )
        
        # 绘制轮廓
        result = image.copy() if len(image.shape) == 3 else cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(
            image=result, 
            contours=contours, 
            contourIdx=-1,  # 绘制所有轮廓
            color=color, 
            thickness=thickness
        )
        
        return result


class HoughLinesProcessor(ImageProcessor):
    """霍夫线变换处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "hough_lines"
    
    @classmethod
    def description(cls) -> str:
        return "使用霍夫变换检测图像中的直线"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="threshold",
                type="int",
                description="阈值参数",
                required=False,
                min_value=1,
                max_value=500,
                default=50
            ),
            ProcessorParameter(
                name="min_line_length",
                type="int",
                description="最小线长",
                required=False,
                min_value=0,
                max_value=500,
                default=20
            ),
            ProcessorParameter(
                name="max_line_gap",
                type="int",
                description="最大线间隔",
                required=False,
                min_value=0,
                max_value=500,
                default=10
            ),
            ProcessorParameter(
                name="color",
                type="str",
                description="线条颜色，格式为'R,G,B'",
                required=False,
                default="0,255,0"
            ),
            ProcessorParameter(
                name="thickness",
                type="int",
                description="线宽",
                required=False,
                min_value=1,
                max_value=10,
                default=2
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        threshold = kwargs.get("threshold", 50)
        min_line_length = kwargs.get("min_line_length", 20)
        max_line_gap = kwargs.get("max_line_gap", 10)
        color_str = kwargs.get("color", "0,255,0")
        thickness = kwargs.get("thickness", 2)
        
        # 解析颜色
        try:
            r, g, b = map(int, color_str.split(","))
            color = (b, g, r)  # OpenCV使用BGR顺序
        except (ValueError, AttributeError):
            raise ValueError(f"颜色格式错误，应为'R,G,B': {color_str}")
        
        # 转换为灰度图
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_gray = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)
        else:
            image_gray = image
        
        # 边缘检测
        edges = cv2.Canny(image=image_gray, threshold1=50, threshold2=150)
        
        # 霍夫线变换
        theta = np.pi / 180
        lines = cv2.HoughLinesP(
            image=edges, 
            rho=1, 
            theta=theta, 
            threshold=threshold,
            minLineLength=min_line_length,
            maxLineGap=max_line_gap
        )
        
        # 绘制直线
        result = image.copy() if len(image.shape) == 3 else cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(img=result, pt1=(x1, y1), pt2=(x2, y2), color=color, thickness=thickness)
        
        return result


class HoughCirclesProcessor(ImageProcessor):
    """霍夫圆变换处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "hough_circles"
    
    @classmethod
    def description(cls) -> str:
        return "使用霍夫变换检测图像中的圆"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="dp",
                type="float",
                description="累加器分辨率与图像分辨率的比值",
                required=False,
                min_value=1.0,
                max_value=10.0,
                step=0.5,
                default=2.0
            ),
            ProcessorParameter(
                name="min_dist",
                type="int",
                description="检测到的圆的最小距离",
                required=False,
                min_value=1,
                max_value=500,
                default=20
            ),
            ProcessorParameter(
                name="param1",
                type="int",
                description="Canny边缘检测的高阈值",
                required=False,
                min_value=1,
                max_value=500,
                default=200
            ),
            ProcessorParameter(
                name="param2",
                type="int",
                description="累加器阈值",
                required=False,
                min_value=1,
                max_value=500,
                default=100
            ),
            ProcessorParameter(
                name="min_radius",
                type="int",
                description="最小圆半径",
                required=False,
                min_value=0,
                max_value=500,
                default=15
            ),
            ProcessorParameter(
                name="max_radius",
                type="int",
                description="最大圆半径",
                required=False,
                min_value=0,
                max_value=500,
                default=50
            ),
            ProcessorParameter(
                name="color",
                type="str",
                description="圆的颜色，格式为'R,G,B'",
                required=False,
                default="0,255,0"
            ),
            ProcessorParameter(
                name="thickness",
                type="int",
                description="圆的线宽",
                required=False,
                min_value=1,
                max_value=10,
                default=2
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        dp = kwargs.get("dp", 2.0)
        min_dist = kwargs.get("min_dist", 20)
        param1 = kwargs.get("param1", 200)
        param2 = kwargs.get("param2", 100)
        min_radius = kwargs.get("min_radius", 15)
        max_radius = kwargs.get("max_radius", 50)
        color_str = kwargs.get("color", "0,255,0")
        thickness = kwargs.get("thickness", 2)
        
        # 解析颜色
        try:
            r, g, b = map(int, color_str.split(","))
            color = (b, g, r)  # OpenCV使用BGR顺序
        except (ValueError, AttributeError):
            raise ValueError(f"颜色格式错误，应为'R,G,B': {color_str}")
        
        # 转换为灰度图
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_gray = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)
        else:
            image_gray = image
        
        # 霍夫圆变换
        circles = cv2.HoughCircles(
            image=image_gray, 
            method=cv2.HOUGH_GRADIENT, 
            dp=dp, 
            minDist=min_dist,
            param1=param1, 
            param2=param2, 
            minRadius=min_radius, 
            maxRadius=max_radius
        )
        
        # 绘制圆
        result = image.copy() if len(image.shape) == 3 else cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                center = (i[0], i[1])
                radius = i[2]
                
                # 绘制圆心
                cv2.circle(img=result, center=center, radius=2, color=color, thickness=3)
                # 绘制圆轮廓
                cv2.circle(img=result, center=center, radius=radius, color=color, thickness=thickness)
        
        return result 