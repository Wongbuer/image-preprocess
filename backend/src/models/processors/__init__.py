"""
图像处理器包
"""
from src.models.image_processor_manager import ImageProcessorManager
from src.models.processors.color_processors import (
    HSVSplitProcessor,
    HSVFixedChannelProcessor,
    WhiteBalanceProcessor,
    GreyWorldProcessor,
    HistogramEqualizationProcessor,
    AutomaticWhiteBalanceProcessor
)
from src.models.processors.filter_processors import (
    MeanFilterProcessor,
    GaussianFilterProcessor,
    MedianFilterProcessor,
    SobelFilterProcessor,
    CannyEdgeProcessor,
    PyramidFilterProcessor,
    ResizeProcessor
)
from src.models.processors.morphology_processors import (
    ErosionProcessor,
    DilationProcessor,
    MorphologyExProcessor,
    ThresholdProcessor
)
from src.models.processors.contour_processors import (
    ContourDetectionProcessor,
    HoughLinesProcessor,
    HoughCirclesProcessor
)
from src.models.processors.enhancement_processors import (
    RetinexSingleScaleProcessor,
    RetinexMultiScaleProcessor,
    AutomaticWhiteBalanceProcessor
)


# 注册所有处理器
def register_all_processors():
    """注册所有处理器"""
    # 色彩处理器
    ImageProcessorManager.register(HSVSplitProcessor)
    ImageProcessorManager.register(HSVFixedChannelProcessor)
    ImageProcessorManager.register(WhiteBalanceProcessor)
    ImageProcessorManager.register(GreyWorldProcessor)
    ImageProcessorManager.register(HistogramEqualizationProcessor)
    
    # 滤波处理器
    ImageProcessorManager.register(MeanFilterProcessor)
    ImageProcessorManager.register(GaussianFilterProcessor)
    ImageProcessorManager.register(MedianFilterProcessor)
    ImageProcessorManager.register(SobelFilterProcessor)
    ImageProcessorManager.register(CannyEdgeProcessor)
    ImageProcessorManager.register(PyramidFilterProcessor)
    ImageProcessorManager.register(ResizeProcessor)
    
    # 形态学处理器
    ImageProcessorManager.register(ErosionProcessor)
    ImageProcessorManager.register(DilationProcessor)
    ImageProcessorManager.register(MorphologyExProcessor)
    ImageProcessorManager.register(ThresholdProcessor)
    
    # 轮廓和边缘检测处理器
    ImageProcessorManager.register(ContourDetectionProcessor)
    ImageProcessorManager.register(HoughLinesProcessor)
    ImageProcessorManager.register(HoughCirclesProcessor)
    
    # 增强处理器
    ImageProcessorManager.register(RetinexSingleScaleProcessor)
    ImageProcessorManager.register(RetinexMultiScaleProcessor)
    ImageProcessorManager.register(AutomaticWhiteBalanceProcessor)


# 自动注册所有处理器
register_all_processors() 