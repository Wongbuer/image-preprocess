"""
色彩处理相关的图像处理器
"""
import cv2
import numpy as np
from typing import List
from src.models.image_processor import ImageProcessor, ProcessorParameter


class HSVSplitProcessor(ImageProcessor):
    """HSV分离处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "hsv_split"
    
    @classmethod
    def description(cls) -> str:
        return "将图像转换为HSV色彩空间并分离H、S、V通道"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="channel",
                type="str",
                description="要提取的通道，可选值：h, s, v",
                required=True
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        channel = kwargs.get("channel", "h").lower()
        
        # 转换成HSV色彩空间
        hsv = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2HSV)
        
        # 分离通道
        h, s, v = cv2.split(hsv)
        
        # 根据参数返回相应通道
        if channel == "h":
            return h
        elif channel == "s":
            return s
        elif channel == "v":
            return v
        else:
            raise ValueError(f"不支持的通道: {channel}")


class HSVFixedChannelProcessor(ImageProcessor):
    """HSV固定通道处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "hsv_fixed_channel"
    
    @classmethod
    def description(cls) -> str:
        return "将图像转换为HSV色彩空间并固定特定通道的值"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="fix_h",
                type="bool",
                description="是否固定H通道",
                required=False,
                default=False
            ),
            ProcessorParameter(
                name="fix_s",
                type="bool",
                description="是否固定S通道",
                required=False,
                default=False
            ),
            ProcessorParameter(
                name="fix_v",
                type="bool",
                description="是否固定V通道",
                required=False,
                default=False
            ),
            ProcessorParameter(
                name="h_value",
                type="int",
                description="H通道固定值",
                required=False,
                min_value=0,
                max_value=255,
                default=255
            ),
            ProcessorParameter(
                name="s_value",
                type="int",
                description="S通道固定值",
                required=False,
                min_value=0,
                max_value=255,
                default=255
            ),
            ProcessorParameter(
                name="v_value",
                type="int",
                description="V通道固定值",
                required=False,
                min_value=0,
                max_value=255,
                default=255
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        fix_h = kwargs.get("fix_h", False)
        fix_s = kwargs.get("fix_s", False)
        fix_v = kwargs.get("fix_v", False)
        h_value = kwargs.get("h_value", 255)
        s_value = kwargs.get("s_value", 255)
        v_value = kwargs.get("v_value", 255)
        
        # 转换成HSV色彩空间
        hsv = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2HSV)
        
        # 分离通道
        h, s, v = cv2.split(hsv)
        
        # 固定通道
        if fix_h:
            h = np.full_like(a=h, fill_value=h_value)
        
        if fix_s:
            s = np.full_like(a=s, fill_value=s_value)
        
        if fix_v:
            v = np.full_like(a=v, fill_value=v_value)
        
        # 合并通道
        merge = cv2.merge([h, s, v])
        
        # 转回BGR
        return cv2.cvtColor(src=merge, code=cv2.COLOR_HSV2BGR)


class WhiteBalanceProcessor(ImageProcessor):
    """白平衡处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "white_balance"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行白平衡处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return []
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        r, g, b = cv2.split(image)
        r_avg = cv2.mean(r)[0]
        g_avg = cv2.mean(g)[0]
        b_avg = cv2.mean(b)[0]
        
        # 求各个通道所占增益
        k = (r_avg + g_avg + b_avg) / 3
        kr = k / r_avg
        kg = k / g_avg
        kb = k / b_avg
        
        r = cv2.addWeighted(src1=r, alpha=kr, src2=0, beta=0, gamma=0)
        g = cv2.addWeighted(src1=g, alpha=kg, src2=0, beta=0, gamma=0)
        b = cv2.addWeighted(src1=b, alpha=kb, src2=0, beta=0, gamma=0)
        
        return cv2.merge([b, g, r])


class GreyWorldProcessor(ImageProcessor):
    """灰度世界算法处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "grey_world"
    
    @classmethod
    def description(cls) -> str:
        return "使用灰度世界算法对图像进行白平衡处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return []
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        nimg = image.transpose(2, 0, 1).astype(np.uint32)
        avg_b = np.average(nimg[0])
        avg_g = np.average(nimg[1])
        avg_r = np.average(nimg[2])
        
        avg = (avg_b + avg_g + avg_r) / 3
        
        nimg[0] = np.minimum(nimg[0] * (avg / avg_b), 255)
        nimg[1] = np.minimum(nimg[1] * (avg / avg_g), 255)
        nimg[2] = np.minimum(nimg[2] * (avg / avg_r), 255)
        
        return nimg.transpose(1, 2, 0).astype(np.uint8)


class HistogramEqualizationProcessor(ImageProcessor):
    """直方图均衡化处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "histogram_equalization"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行直方图均衡化处理"
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return []
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
        channels = cv2.split(ycrcb)
        cv2.equalizeHist(channels[0], channels[0])
        cv2.merge(channels, ycrcb)
        return cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR)


class AutomaticWhiteBalanceProcessor(ImageProcessor):
    """自动白平衡处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "automatic_white_balance"
    
    @classmethod
    def description(cls) -> str:
        return "对图像进行自动白平衡处理"
    
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