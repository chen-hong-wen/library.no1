if __name__ == '__main__':
    from ultralytics import YOLO
    import cv2

    # 1. 加载模型
    model = YOLO("E:/Libseat_system/computer_vision/scripts/runs/detect/train23/weights/best.pt")

    # 2. 检测图片
    image_path = "E:/Libseat_system/computer_vision/data/raw/images/微信图片_20260328164613_470_29.jpg"
    results = model.predict(image_path, save=True, show=False)

    # 3. 获取结果并自定义绘制
    result = results[0]
    print(f"检测到 {len(result.boxes) if result.boxes is not None else 0} 个目标")

    # 关键：使用plot函数时自定义参数
    annotated_img = result.plot(
        font='Arial.ttf',  # 字体文件（可选）
        font_size=0.5,  # 字体大小，默认1.0，建议0.3-0.8
        line_width=2,  # 框线宽度
        pil=True  # 使用PIL绘制（字体更清晰）
    )

    # 4. 显示
    cv2.imshow("检测结果", annotated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()