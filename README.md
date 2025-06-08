# 图像预处理应用 🖼️✨

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.12+-green.svg)](https://fastapi.tiangolo.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.11.0+-red.svg)](https://opencv.org/)
[![NumPy](https://img.shields.io/badge/NumPy-2.3.0+-yellow.svg)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个功能强大的图像预处理应用，提供多种图像处理操作，包括色彩调整、滤波、形态学变换、边缘检测等。

![图像处理示例](https://miro.medium.com/max/1400/1*GsImz-edoeuqCuXCmj7TSQ.gif)

## 目录 📋

- [前端](#前端)
- [后端](#后端)
  - [特性](#特性)
  - [技术栈](#技术栈)
  - [安装与运行](#安装与运行)
  - [API接口](#api接口)
  - [处理器列表](#处理器列表)
  - [使用示例](#使用示例)
  - [开发指南](#开发指南)

## 前端

*待补充*

## 后端 🖥️

### 特性 ✨

- 🔄 多种图像预处理操作，包括色彩调整、滤波、形态学变换、边缘检测等
- 🚀 高性能处理，基于OpenCV优化算法
- 🔌 RESTful API接口，方便与前端或其他服务集成
- 📝 详细的API文档，基于Swagger UI
- 🧩 模块化设计，易于扩展新的处理操作
- 🔍 支持批量处理，可以对图像应用多个处理器

### 技术栈 🛠️

- [Python](https://www.python.org/) - 编程语言
- [FastAPI](https://fastapi.tiangolo.com/) - Web框架
- [OpenCV](https://opencv.org/) - 图像处理库
- [NumPy](https://numpy.org/) - 科学计算库
- [Uvicorn](https://www.uvicorn.org/) - ASGI服务器
- [uv](https://github.com/astral-sh/uv) - Python包管理工具

### 安装与运行 🚀

1. 克隆仓库

```bash
git clone https://github.com/yourusername/image-preprocess.git
cd image-preprocess
```

2. 使用uv安装依赖

```bash
cd backend
uv pip install -e .
```

3. 运行应用

```bash
cd backend
python main.py
```

应用将在`http://localhost:8000`上运行，API文档可在`http://localhost:8000/api/docs` 访问。

### API接口 📡

#### 获取所有处理器

```
GET /api/image/processors
```

返回所有可用的图像处理器及其参数信息。

#### 处理单张图像

```
POST /api/image/process
```

请求体示例：

```json
{
  "processor_name": "gaussian_filter",
  "image_data": "base64编码的图像数据",
  "params": {
    "kernel_size": 9,
    "sigma": 1.5
  }
}
```

#### 批量处理图像

```
POST /api/image/batch-process
```

请求体示例：

```json
{
  "processor_names": ["gaussian_filter", "canny_edge"],
  "image_data": "base64编码的图像数据",
  "params_list": [
    {
      "kernel_size": 9,
      "sigma": 1.5
    },
    {
      "threshold1": 125,
      "threshold2": 350
    }
  ]
}
```

### 处理器列表 📋

#### 色彩处理器

| 处理器名称 | 描述 | 主要参数 |
|----------|------|---------|
| hsv_split | 将图像转换为HSV色彩空间并分离通道 | channel (h/s/v) |
| hsv_fixed_channel | 将图像转换为HSV色彩空间并固定通道 | fix_h, fix_s, fix_v, h_value, s_value, v_value |
| white_balance | 对图像进行白平衡处理 | - |
| grey_world | 使用灰度世界算法对图像进行白平衡 | - |
| histogram_equalization | 对图像进行直方图均衡化处理 | - |
| automatic_white_balance | 对图像进行自动白平衡处理 | - |

#### 滤波处理器

| 处理器名称 | 描述 | 主要参数 |
|----------|------|---------|
| mean_filter | 对图像进行均值滤波处理 | kernel_size |
| gaussian_filter | 对图像进行高斯滤波处理 | kernel_size, sigma |
| median_filter | 对图像进行中值滤波处理 | kernel_size |
| sobel_filter | 对图像进行Sobel滤波处理 | dx, dy, kernel_size, scale, delta |
| canny_edge | 对图像进行Canny边缘检测处理 | threshold1, threshold2, invert |
| pyramid_filter | 对图像进行金字塔降采样和上采样处理 | operation (down/up/both) |
| resize | 对图像进行缩放处理 | scale, interpolation |

#### 形态学处理器

| 处理器名称 | 描述 | 主要参数 |
|----------|------|---------|
| erosion | 对图像进行腐蚀处理 | kernel_size, iterations |
| dilation | 对图像进行膨胀处理 | kernel_size, iterations |
| morphology_ex | 对图像进行形态学操作处理 | operation, kernel_size, convert_to_gray |
| threshold | 对图像进行阈值处理 | threshold, max_value, threshold_type |

#### 轮廓和边缘检测处理器

| 处理器名称 | 描述 | 主要参数 |
|----------|------|---------|
| contour_detection | 对图像进行轮廓检测处理 | mode, method, color, thickness |
| hough_lines | 使用霍夫变换检测图像中的直线 | threshold, min_line_length, max_line_gap, color, thickness |
| hough_circles | 使用霍夫变换检测图像中的圆 | dp, min_dist, param1, param2, min_radius, max_radius, color, thickness |

#### 增强处理器

| 处理器名称 | 描述 | 主要参数 |
|----------|------|---------|
| retinex_single_scale | 使用单尺度Retinex算法对图像进行增强 | sigma |
| retinex_multi_scale | 使用多尺度Retinex算法对图像进行增强 | sigma_small, sigma_medium, sigma_large |
| automatic_white_balance | 使用自动白平衡算法对图像进行增强 | - |

### 使用示例 🌟

#### 示例1：应用高斯模糊

```python
import requests
import base64

# 读取图像文件并转换为Base64
with open("example.jpg", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

# 构建请求体
data = {
    "processor_name": "gaussian_filter",
    "image_data": image_data,
    "params": {
        "kernel_size": 9,
        "sigma": 1.5
    }
}

# 发送请求
response = requests.post("http://localhost:8000/api/image/process", json=data)

# 处理响应
if response.status_code == 200:
    result = response.json()
    processed_image_data = result["data"]["processed_image"]
    
    # 将Base64转回图像并保存
    with open("processed_example.jpg", "wb") as image_file:
        image_file.write(base64.b64decode(processed_image_data))
    print("处理成功！")
else:
    print(f"处理失败：{response.text}")
```

#### 示例2：批量处理 - 先高斯模糊再边缘检测

```python
import requests
import base64

# 读取图像文件并转换为Base64
with open("example.jpg", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

# 构建请求体
data = {
    "processor_names": ["gaussian_filter", "canny_edge"],
    "image_data": image_data,
    "params_list": [
        {
            "kernel_size": 9,
            "sigma": 1.5
        },
        {
            "threshold1": 125,
            "threshold2": 350,
            "invert": True
        }
    ]
}

# 发送请求
response = requests.post("http://localhost:8000/api/image/batch-process", json=data)

# 处理响应
if response.status_code == 200:
    result = response.json()
    processed_image_data = result["data"]["processed_image"]
    
    # 将Base64转回图像并保存
    with open("processed_example_batch.jpg", "wb") as image_file:
        image_file.write(base64.b64decode(processed_image_data))
    print("批量处理成功！")
else:
    print(f"处理失败：{response.text}")
```

### 开发指南 🔧

#### 项目结构

```
backend/
├── main.py                # 主入口文件
├── pyproject.toml         # 项目依赖配置
├── src/
│   ├── app.py             # FastAPI应用实例
│   ├── controllers/       # 控制器层
│   │   ├── health_controller.py
│   │   ├── image_controller.py
│   │   └── __init__.py
│   ├── entity/            # 实体层
│   │   ├── response.py
│   │   └── __init__.py
│   ├── middlewares/       # 中间件
│   │   ├── cors.py
│   │   └── __init__.py
│   ├── models/            # 模型层
│   │   ├── image_processor.py
│   │   ├── image_processor_manager.py
│   │   ├── processors/    # 图像处理器
│   │   │   ├── color_processors.py
│   │   │   ├── contour_processors.py
│   │   │   ├── enhancement_processors.py
│   │   │   ├── filter_processors.py
│   │   │   ├── morphology_processors.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── services/          # 服务层
│   │   ├── image_service.py
│   │   └── __init__.py
│   └── utils/             # 工具类
│       └── __init__.py
```

#### 添加新的处理器

如果你想添加新的图像处理器，只需按照以下步骤操作：

1. 在适当的处理器文件中（如`color_processors.py`）创建一个新的处理器类，继承自`ImageProcessor`
2. 实现必要的方法：`name()`、`description()`、`parameters()`和`process()`
3. 在`processors/__init__.py`中注册新的处理器

示例：

```python
class MyNewProcessor(ImageProcessor):
    """我的新处理器"""
    
    @classmethod
    def name(cls) -> str:
        return "my_new_processor"
    
    @classmethod
    def description(cls) -> str:
        return "这是我的新处理器，用于..."
    
    @classmethod
    def parameters(cls) -> List[ProcessorParameter]:
        return [
            ProcessorParameter(
                name="my_param",
                type="int",
                description="我的参数",
                required=False,
                min_value=0,
                max_value=100,
                default=50
            )
        ]
    
    def process(self, image: np.ndarray, **kwargs) -> np.ndarray:
        my_param = kwargs.get("my_param", 50)
        
        # 处理逻辑...
        
        return processed_image
```

然后在`processors/__init__.py`中注册：

```python
# 在register_all_processors函数中添加
ImageProcessorManager.register(MyNewProcessor)
``` 