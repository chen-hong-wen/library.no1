# split_dataset.py
import os
import random
import shutil

# 配置
dataset_root = "data/processed"
train_img_dir = os.path.join(dataset_root, "train/images")
train_label_dir = os.path.join(dataset_root, "train/labels")
val_img_dir = os.path.join(dataset_root, "val/images")
val_label_dir = os.path.join(dataset_root, "val/labels")

# 获取所有训练图片
all_images = [f for f in os.listdir(train_img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
print(f"找到 {len(all_images)} 张训练图片")

# 设置验证集比例 (20%)
val_ratio = 0.2
num_val = max(1, int(len(all_images) * val_ratio))

# 随机选择图片作为验证集
val_images = random.sample(all_images, num_val)
print(f"将 {len(val_images)} 张图片移动到验证集")

# 移动选中的图片和对应的标签
for img_name in val_images:
    # 移动图片
    src_img = os.path.join(train_img_dir, img_name)
    dst_img = os.path.join(val_img_dir, img_name)
    shutil.move(src_img, dst_img)

    # 移动对应的标签
    label_name = os.path.splitext(img_name)[0] + ".txt"
    src_label = os.path.join(train_label_dir, label_name)
    dst_label = os.path.join(val_label_dir, label_name)

    if os.path.exists(src_label):
        shutil.move(src_label, dst_label)
        print(f"移动: {img_name} 及其标签")
    else:
        print(f"警告: 图片 {img_name} 没有对应的标签文件")

print("数据集划分完成！")