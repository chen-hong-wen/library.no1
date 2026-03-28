#!/usr/bin/env python3
"""
项目目录结构自动创建脚本
"""
import os
from pathlib import Path


def create_project_structure(base_path="."):
    """创建项目目录结构"""
    base = Path(base_path)

    # 主要目录结构
    dirs = [
        # 核心目录
        "src/api/endpoints",
        "src/api/schemas",
        "src/detection/utils",
        "src/detection/models",
        "src/processing",
        "src/database",
        "src/utils",
        "src/services",

        # 数据目录
        "data/raw/images",
        "data/raw/videos",
        "data/raw/test_images",
        "data/processed/train/images",
        "data/processed/train/labels",
        "data/processed/val/images",
        "data/processed/val/labels",
        "data/processed/test",
        "data/annotations/labelImg/xmls",
        "data/annotations/labelImg/txts",
        "data/models/yolov8",
        "data/models/export/onnx",
        "data/models/export/tensorrt",

        # 其他目录
        "configs",
        "notebooks",
        "tests/fixtures/test_images",
        "tests/fixtures/test_configs",
        "docs/api",
        "docs/deployment",
        "docs/models",
        "scripts",
        "logs/app",
        "logs/training",
        "logs/api",
        "docker/nginx",
        "results/training/plots",
        "results/training/reports",
        "results/predictions/images",
        "results/predictions/videos",
        "results/evaluations"
    ]

    # 创建所有目录
    for dir_path in dirs:
        full_path = base / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"创建目录: {full_path}")

    # 创建必要文件
    files = {
        "README.md": "# 图书馆智能座位视觉系统\n\n## 项目概述\n\n## 快速开始\n\n## 目录结构",
        ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
*.manifest
*.spec

# Virtual Environment
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 数据和大文件
data/raw/
data/processed/
logs/
results/
!data/annotations/
!data/models/
""",
        ".env.example": """# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=library_seat
DB_USER=root
DB_PASSWORD=your_password

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# 应用配置
APP_SECRET_KEY=your_secret_key
DEBUG=True

# 模型配置
MODEL_PATH=data/models/yolov8/best.pt
CONFIDENCE_THRESHOLD=0.5
DEVICE=cuda:0  # or cpu
""",
        "configs/app_config.yaml": """app:
  name: "图书馆座位视觉系统"
  version: "1.0.0"
  debug: true

server:
  host: "0.0.0.0"
  port: 8000
  workers: 4

detection:
  model_path: "data/models/yolov8/best.pt"
  confidence_threshold: 0.5
  iou_threshold: 0.45
  device: "cuda:0"
""",
        "src/__init__.py": "",
        "src/main.py": """#!/usr/bin/env python3
"""
        
            """
            
            import uvicorn
            from src.api.app import create_app
            
            app = create_app()
            
            if __name__ == "__main__":
                uvicorn.run(
                    "src.main:app",
                    host="0.0.0.0",
                    port=8000,
                    reload=True,
                    log_level="info"
                )
            """,
        "data/annotations/dataset.yaml": """# 数据集配置文件
path: ../data/processed
train: train/images
val: val/images

# 类别数量
nc: 2

# 类别名称
names: 
  0: "occupied_seat"
  1: "empty_seat"
""",
        "scripts/train.py": """#!/usr/bin/env python3
"""
       
            """
            
            from ultralytics import YOLO
            
            def train_model():
                # 加载预训练模型
                model = YOLO('yolov8n.pt')
            
                # 训练模型
                results = model.train(
                    data='data/annotations/dataset.yaml',
                    epochs=100,
                    imgsz=640,
                    batch=16,
                    name='yolov8_seat_detection'
                )
            
                return results
            
            if __name__ == "__main__":
                train_model()
            """
    }

    # 创建文件
    for file_path, content in files.items():
        full_path = base / file_path
        if not full_path.exists():
            full_path.write_text(content, encoding='utf-8')
            print(f"创建文件: {full_path}")

    print("\n✅ 项目结构创建完成！")
    print("📁 请复制以下命令激活虚拟环境并安装依赖：")
    print("venv\\Scripts\\activate  # Windows")
    print("source venv/bin/activate  # Linux/Mac")
    print("pip install -r requirements.txt")


if __name__ == "__main__":
    create_project_structure()