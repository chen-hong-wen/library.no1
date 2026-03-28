# scripts/convert_xml_to_yolo.py
"""
将Pascal VOC XML格式转换为YOLO格式
"""

import xml.etree.ElementTree as ET
import os
import glob
import yaml


def convert_xml_to_yolo_with_mapping(xml_dir, output_dir, target_classes, class_mapping):
    """
    将XML标注转换为YOLO格式，支持类别映射

    参数:
        xml_dir: XML文件目录
        output_dir: 输出YOLO标签目录
        target_classes: 目标类别名称列表，如 ['occupied_seat', 'empty_seat']
        class_mapping: 原始类别到目标类别的映射字典
    """

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 创建目标类别的ID映射
    target_class_to_id = {name: idx for idx, name in enumerate(target_classes)}
    print(f"目标类别映射: {target_class_to_id}")
    print(f"类别映射关系: {class_mapping}")

    # 获取所有XML文件
    xml_files = glob.glob(os.path.join(xml_dir, "*.xml"))
    print(f"找到 {len(xml_files)} 个XML文件")

    conversion_count = 0
    error_count = 0
    skipped_count = 0

    for xml_file in xml_files:
        try:
            # 解析XML
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # 获取图片尺寸
            size = root.find('size')
            if size is None:
                print(f"警告: {os.path.basename(xml_file)} 没有size信息，跳过")
                skipped_count += 1
                continue

            img_width = int(size.find('width').text)
            img_height = int(size.find('height').text)

            # 获取文件名（不含扩展名）
            filename = os.path.splitext(os.path.basename(xml_file))[0]
            output_file = os.path.join(output_dir, f"{filename}.txt")

            # 存储所有检测框
            yolo_lines = []

            # 遍历所有物体标注
            for obj in root.iter('object'):
                # 获取原始类别名称
                original_class = obj.find('name').text

                # 应用类别映射
                if original_class in class_mapping:
                    target_class = class_mapping[original_class]
                    class_id = target_class_to_id[target_class]
                else:
                    # 如果原始类别不在映射中，跳过
                    print(f"警告: XML文件 {filename}.xml 中的类别 '{original_class}' 不在映射表中，跳过")
                    continue

                # 获取边界框坐标
                bndbox = obj.find('bndbox')
                if bndbox is None:
                    print(f"警告: XML文件 {filename}.xml 中的对象没有边界框，跳过")
                    continue

                xmin = float(bndbox.find('xmin').text)
                ymin = float(bndbox.find('ymin').text)
                xmax = float(bndbox.find('xmax').text)
                ymax = float(bndbox.find('ymax').text)

                # 转换为YOLO格式（归一化中心坐标和宽高）
                x_center = (xmin + xmax) / 2 / img_width
                y_center = (ymin + ymax) / 2 / img_height
                width = (xmax - xmin) / img_width
                height = (ymax - ymin) / img_height

                # 确保坐标在0-1范围内
                x_center = max(0.0, min(1.0, x_center))
                y_center = max(0.0, min(1.0, y_center))
                width = max(0.0, min(1.0, width))
                height = max(0.0, min(1.0, height))

                # 写入YOLO格式行
                yolo_line = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
                yolo_lines.append(yolo_line)

            # 写入YOLO格式文件
            if yolo_lines:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(yolo_lines))
                conversion_count += 1
                if conversion_count <= 3:  # 显示前3个转换示例
                    print(f"转换: {filename}.xml -> {len(yolo_lines)} 个标注")
            else:
                print(f"警告: {filename}.xml 没有找到有效的标注（可能所有类别都不在映射表中）")
                error_count += 1

        except Exception as e:
            print(f"错误: 处理 {xml_file} 时出错: {e}")
            error_count += 1

    print(f"\n转换完成!")
    print(f"成功转换: {conversion_count} 个文件")
    print(f"转换失败: {error_count} 个文件")
    print(f"跳过处理: {skipped_count} 个文件（无size信息等）")
    print(f"输出目录: {output_dir}")

    return conversion_count, error_count, skipped_count


def verify_conversion(xml_dir, yolo_dir, image_dir=None):
    """验证转换结果"""
    print("\n=== 验证转换结果 ===")

    # 检查文件数量
    xml_files = glob.glob(os.path.join(xml_dir, "*.xml"))
    yolo_files = glob.glob(os.path.join(yolo_dir, "*.txt"))

    print(f"XML文件数: {len(xml_files)}")
    print(f"YOLO文件数: {len(yolo_files)}")

    if len(xml_files) != len(yolo_files):
        print(f"⚠️ 警告: 文件数量不匹配! 相差 {abs(len(xml_files) - len(yolo_files))} 个文件")

    # 检查文件对应关系
    missing_yolo = []
    for xml_file in xml_files[:10]:  # 检查前10个
        filename = os.path.splitext(os.path.basename(xml_file))[0]
        yolo_file = os.path.join(yolo_dir, f"{filename}.txt")

        if not os.path.exists(yolo_file):
            missing_yolo.append(filename)

    if missing_yolo:
        print(f"⚠️ 警告: {len(missing_yolo)} 个XML文件没有对应的YOLO文件")
        print(f"  例如: {missing_yolo[:3]}")

    # 检查图片文件是否存在（如果提供了图片目录）
    if image_dir and os.path.exists(image_dir):
        image_files = {os.path.splitext(f)[0] for f in os.listdir(image_dir)
                       if f.lower().endswith(('.jpg', '.jpeg', '.png'))}

        missing_images = []
        for xml_file in xml_files[:10]:
            filename = os.path.splitext(os.path.basename(xml_file))[0]
            if filename not in image_files:
                missing_images.append(filename)

        if missing_images:
            print(f"⚠️ 警告: {len(missing_images)} 个标注文件没有对应的图片")
            print(f"  例如: {missing_images[:3]}")


def update_dataset_yaml(yaml_path, target_classes, xml_dir):
    """更新dataset.yaml文件中的类别信息"""

    try:
        # 读取现有的YAML文件
        with open(yaml_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # 更新类别信息
        config['names'] = target_classes
        config['nc'] = len(target_classes)

        # 写入更新后的内容
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

        print(f"\n✅ 已更新配置文件: {yaml_path}")
        print(f"  类别数量 (nc): {len(target_classes)}")
        print(f"  类别名称 (names): {target_classes}")

    except FileNotFoundError:
        # 如果文件不存在，创建新的
        config = {
            'path': '../',  # 根据实际结构调整
            'train': 'processed/train/images',
            'val': 'processed/val/images',
            'nc': len(target_classes),
            'names': target_classes
        }

        # 确保目录存在
        os.makedirs(os.path.dirname(yaml_path), exist_ok=True)

        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

        print(f"\n✅ 已创建配置文件: {yaml_path}")
    except Exception as e:
        print(f"⚠️  更新配置文件失败: {e}")


if __name__ == "__main__":
    # 🔴【批注1】根据您的截图，XML文件在 data/xmls/ 而不是 data/annotations_xml/
    # 修改为您的实际XML文件路径
    XML_DIR = "E:/Libseat_system/computer_vision/data/annotations/xmls"

    # 🔴【批注2】根据您的项目结构，YOLO标签应该输出到 data/processed/train/labels/
    YOLO_OUTPUT_DIR = "E:/Libseat_system/computer_vision/data/annotations/txts"

    # 🔴【批注3】图片可能在 data/processed/train/images/
    IMAGE_DIR = "E:/Libseat_system/computer_vision/data/processed/val/images"

    # 🔴【类别映射设置】
    # 在转换脚本中使用映射
    class_mapping = {
        'people': 'occupied_seat',  # 人 → 座位被占用
        'chair': 'empty_seat',  # 椅子 → 空座位
        'bag': 'occupied_seat',  # 包 → 座位被占用
    }

    # 目标类别列表
    TARGET_CLASSES = ['occupied_seat', 'empty_seat']  # 目标类别只有2个

    # dataset.yaml文件路径
    DATASET_YAML_PATH = "../data/data/xmls/dataset.yaml"  # 或根据实际位置调整

    print("=" * 60)
    print("XML转YOLO格式转换器")
    print("=" * 60)

    # 先检查XML目录是否存在
    if not os.path.exists(XML_DIR):
        print(f"❌ 错误: XML目录不存在: {XML_DIR}")
        print(f"请检查您的项目结构，XML文件应该在: {os.path.abspath(XML_DIR)}")

        # 列出当前目录结构
        print(f"\n当前 data/ 目录内容:")
        if os.path.exists("../data/data"):
            for item in os.listdir("../data/data"):
                item_path = os.path.join("../data/data", item)
                if os.path.isdir(item_path):
                    print(f"  📁 {item}/")
                    # 显示子目录中的内容
                    try:
                        sub_items = os.listdir(item_path)[:3]  # 只显示前3个
                        for sub_item in sub_items:
                            print(f"    ├─ {sub_item}")
                    except:
                        pass
                else:
                    print(f"  📄 {item}")
        exit(1)

    # 检查XML文件
    xml_files = glob.glob(os.path.join(XML_DIR, "*.xml"))
    if not xml_files:
        print(f"❌ 错误: 在 {XML_DIR} 中没有找到XML文件")
        print("请确保您的XML文件扩展名为 .xml")
        exit(1)

    print(f"找到 {len(xml_files)} 个XML文件")
    print(f"目标输出目录: {YOLO_OUTPUT_DIR}")
    print(f"类别映射关系: {class_mapping}")
    print(f"目标类别: {TARGET_CLASSES}")

    # 开始转换
    print("\n" + "=" * 60)
    print("开始转换XML到YOLO格式...")

    conversion_count, error_count, skipped_count = convert_xml_to_yolo_with_mapping(
        XML_DIR, YOLO_OUTPUT_DIR, TARGET_CLASSES, class_mapping
    )

    # 验证转换结果
    print("\n" + "=" * 60)
    verify_conversion(XML_DIR, YOLO_OUTPUT_DIR, IMAGE_DIR)

    # 显示示例文件内容
    print("\n" + "=" * 60)
    print("示例文件内容:")

    yolo_files = glob.glob(os.path.join(YOLO_OUTPUT_DIR, "*.txt"))
    if yolo_files:
        # 显示前3个文件的内容
        for i, sample_file in enumerate(yolo_files[:3]):
            print(f"\n示例文件 {i + 1}: {os.path.basename(sample_file)}")
            with open(sample_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    lines = content.split('\n')
                    print(f"  包含 {len(lines)} 个标注:")
                    for j, line in enumerate(lines[:3]):  # 显示前3个标注
                        parts = line.split()
                        if len(parts) == 5:
                            class_id, x, y, w, h = parts
                            class_name = TARGET_CLASSES[int(class_id)] if int(class_id) < len(
                                TARGET_CLASSES) else f"未知({class_id})"
                            print(f"    标注{j + 1}: 类别={class_name}({class_id}), 中心=({x},{y}), 尺寸=({w},{h})")
                        else:
                            print(f"    标注{j + 1}: 格式错误 - {line}")
                else:
                    print("  警告: 文件为空")
    else:
        print("❌ 没有生成YOLO标签文件")

    # 更新dataset.yaml配置文件
    print("\n" + "=" * 60)
    if os.path.exists(DATASET_YAML_PATH):
        print(f"发现配置文件: {DATASET_YAML_PATH}")
        update_dataset_yaml(DATASET_YAML_PATH, TARGET_CLASSES, XML_DIR)
    else:
        print(f"未找到配置文件: {DATASET_YAML_PATH}")
        print("将在转换后创建...")
        update_dataset_yaml(DATASET_YAML_PATH, TARGET_CLASSES, XML_DIR)

    print("\n" + "=" * 60)
    print("转换完成!")
    print("=" * 60)