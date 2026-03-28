
from ultralytics import YOLO
import torch

if __name__ == '__main__':  # 关键：添加这行保护
    config_path = r"E:\Libseat_system\computer_vision\configs\seat_detection.yaml"
    # 或者使用相对路径时确保正确
    # config_path = os.path.join(os.path.dirname(__file__), "..", "configs", "seat_detection.yaml")

    model = YOLO('../models/weight/yolov8l.pt')

    # 训练模型
    results = model.train(
        data=config_path,  # 使用明确的路径
        epochs=100,
        imgsz=640,
        batch=16,
        device='cuda' if torch.cuda.is_available() else 'cpu'
    )
