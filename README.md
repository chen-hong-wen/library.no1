# 图书馆智能座位视觉系统

## 项目概述

## 快速开始

## 目录结构
E:\libseat_system\computer_vision\
├── README.md                       # 项目说明文档
├── requirements.txt                # 依赖包列表（已有）
├── .gitignore                      # Git忽略文件
├── .env.example                    # 环境变量示例
├── .env                            # 本地环境变量（不提交）
├── pyproject.toml                  # 项目配置（可选）
├── configs/                        # 配置文件目录
│   ├── app_config.yaml             # 应用配置
│   ├── model_config.yaml           # 模型参数配置
│   └── database.yaml               # 数据库配置
│
├── src/                            # 源代码主目录（核心）
│   ├── __init__.py
│   ├── main.py                     # 程序主入口
│   ├── api/                        # FastAPI接口模块
│   │   ├── __init__.py
│   │   ├── app.py                  # FastAPI应用实例
│   │   ├── endpoints/              # API端点
│   │   │   ├── seat_detection.py   # 座位检测API
│   │   │   ├── occupancy.py        # 占用状态API
│   │   │   └── health.py           # 健康检查API
│   │   └── schemas/                # Pydantic数据模型
│   │       ├── seat_schema.py
│   │       └── request_schema.py
│   │
│   ├── detection/                  # 检测模块
│   │   ├── __init__.py
│   │   ├── seat_detector.py       # 座位检测器
│   │   ├── people_detector.py     # 人员检测器
│   │   ├── utils/                  # 检测工具
│   │   │   ├── preprocess.py      # 图像预处理
│   │   │   ├── postprocess.py     # 后处理
│   │   │   └── visualize.py       # 可视化工具
│   │   └── models/                 # 模型定义和加载
│   │       ├── yolov8_seat.py     # YOLO座位检测
│   │       └── model_manager.py    # 模型管理器
│   │
│   ├── processing/                 # 图像处理模块
│   │   ├── __init__.py
│   │   ├── camera_manager.py      # 摄像头管理
│   │   ├── image_processor.py     # 图像处理器
│   │   └── video_stream.py        # 视频流处理
│   │
│   ├── database/                   # 数据库模块
│   │   ├── __init__.py
│   │   ├── models.py              # SQLAlchemy数据模型
│   │   ├── crud.py                # CRUD操作
│   │   └── connections.py         # 数据库连接
│   │
│   ├── utils/                      # 通用工具函数
│   │   ├── __init__.py
│   │   ├── logger.py              # 日志配置
│   │   ├── config_loader.py       # 配置加载
│   │   ├── file_handler.py        # 文件处理
│   │   └── time_utils.py          # 时间工具
│   │
│   └── services/                   # 业务逻辑服务
│       ├── __init__.py
│       ├── seat_service.py        # 座位服务
│       ├── occupancy_service.py   # 占用服务
│       └── notification_service.py # 通知服务
│
├── data/                           # 数据目录（重要）
│   ├── raw/                        # 原始数据
│   │   ├── images/                 # 原始图片
│   │   ├── videos/                 # 视频文件
│   │   └── test_images/            # 测试图片
│   │
│   ├── processed/                  # 处理后的数据
│   │   ├── train/                  # 训练集
│   │   │   ├── images/
│   │   │   └── labels/
│   │   ├── val/                    # 验证集
│   │   │   ├── images/
│   │   │   └── labels/
│   │   └── test/                   # 测试集
│   │
│   ├── annotations/                # 标注文件
│   │   ├── labelImg/               # labelImg标注文件
│   │   │   ├── xmls/               # XML格式
│   │   │   ├── txts/               # YOLO格式
│   │   │   └── classes.txt         # 类别文件
│   │   └── dataset.yaml            # Ultralytics数据集配置
│   │
│   └── models/                     # 训练好的模型
│       ├── yolov8/                 # YOLOv8模型
│       │   ├── best.pt
│       │   ├── last.pt
│       │   └── args.yaml
│       └── export/                 # 导出模型
│           ├── onnx/
│           └── tensorrt/
│
├── notebooks/                      # Jupyter Notebooks（可选）
│   ├── 01_data_exploration.ipynb   # 数据探索
│   ├── 02_model_training.ipynb     # 模型训练
│   ├── 03_evaluation.ipynb         # 模型评估
│   └── 04_api_testing.ipynb        # API测试
│
├── tests/                          # 测试目录
│   ├── __init__.py
│   ├── test_detection.py          # 检测模块测试
│   ├── test_api.py                # API测试
│   ├── conftest.py                # pytest配置
│   └── fixtures/                  # 测试夹具
│       ├── test_images/
│       └── test_configs/
│
├── docs/                           # 文档目录
│   ├── api/                        # API文档
│   │   ├── endpoints.md
│   │   └── examples.md
│   ├── deployment/                 # 部署文档
│   │   ├── docker.md
│   │   └── setup.md
│   ├── models/                     # 模型文档
│   │   ├── training.md
│   │   └── evaluation.md
│   └── architecture.md             # 架构设计
│
├── scripts/                        # 脚本目录
│   ├── setup.sh                    # 环境设置脚本
│   ├── train.py                    # 训练脚本
│   ├── evaluate.py                 # 评估脚本
│   ├── export_model.py             # 模型导出
│   ├── label_images.py             # 自动标注脚本
│   └── process_dataset.py          # 数据处理脚本
│
├── logs/                           # 日志目录
│   ├── app/                        # 应用日志
│   │   ├── app_20240328.log
│   │   └── error.log
│   ├── training/                   # 训练日志
│   │   └── yolov8_training.log
│   └── api/                        # API访问日志
│
├── venv/                           # 虚拟环境（已有）
│
├── docker/                         # Docker配置
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx/
│       └── nginx.conf
│
└── results/                        # 实验结果
    ├── training/                   # 训练结果
    │   ├── plots/                  # 训练图表
    │   │   ├── loss_curve.png
    │   │   └── metrics.png
    │   └── reports/                # 训练报告
    │       └── training_report.md
    ├── predictions/                # 预测结果
    │   ├── images/                 # 带标注的预测图片
    │   └── videos/                 # 预测视频
    └── evaluations/                # 评估结果
        └── confusion_matrix.png