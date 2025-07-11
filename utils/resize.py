import os
import cv2
import shutil

# 用户参数
image_dir = "/home/mengrey/Documents/local_videos/data_generator/Data/20250627_energy_test/images"
label_dir = "/home/mengrey/Documents/local_videos/data_generator/Data/20250627_energy_test/labels"
save_image_dir = "/home/mengrey/Documents/local_videos/data_generator/Data/20250627_energy_test/processed_images"
save_label_dir = "/home/mengrey/Documents/local_videos/data_generator/Data/20250627_energy_test/processed_labels"
target_class_id = {0,3}  # 指定作为中心的类别ID
target_width = 384  # 目标宽度
target_height = 640  # 目标高度
target_ratio = target_height / target_width  # 目标高宽比 (h/w)

# 创建输出目录
os.makedirs(save_image_dir, exist_ok=True)
os.makedirs(save_label_dir, exist_ok=True)

# 获取图片列表
image_list = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.png'))]

for image_name in image_list:
    # 加载图片
    img_path = os.path.join(image_dir, image_name)
    img = cv2.imread(img_path)
    h_ori, w_ori = img.shape[:2]

    # 加载标签
    label_path = os.path.join(label_dir, os.path.splitext(image_name)[0] + ".txt")
    if not os.path.exists(label_path):
        print(f"[WARN] No label for {image_name}")
        continue

    with open(label_path, 'r') as f:
        lines = f.readlines()

    # 解析标签（支持多种格式）
    labels_data = []  # 存储 (format_type, cls_id, data)
    center_y_for_crop = None
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 5:
            # 标准YOLO格式
            try:
                cls_id, x, y, w, h = int(float(parts[0])), *map(float, parts[1:])
                labels_data.append(('yolo', cls_id, [x, y, w, h]))
                if cls_id in target_class_id and center_y_for_crop is None:
                    center_y_for_crop = y * h_ori
            except ValueError as e:
                print(f"[WARN] Error parsing YOLO label in {image_name}: {line.strip()} - {e}")
                continue
        elif len(parts) == 9:
            # 多边形格式
            try:
                cls_id = int(float(parts[0]))
                coords = list(map(float, parts[1:]))
                labels_data.append(('polygon', cls_id, coords))
                
                # 为了找裁剪中心，计算边界框
                x_coords = [coords[i] for i in range(0, 8, 2)]
                y_coords = [coords[i] for i in range(1, 8, 2)]
                min_x, max_x = min(x_coords), max(x_coords)
                min_y, max_y = min(y_coords), max(y_coords)
                y = (min_y + max_y) / 2
                
                if cls_id in target_class_id and center_y_for_crop is None:
                    center_y_for_crop = y * h_ori
            except ValueError as e:
                print(f"[WARN] Error parsing polygon label in {image_name}: {line.strip()} - {e}")
                continue
        else:
            print(f"[WARN] Invalid label format in {image_name}: expected 5 or 9 values, got {len(parts)}")
            continue

    if center_y_for_crop is None:
        print(f"[WARN] No target class {target_class_id} found in {image_name}")
        continue

    # 按固定尺寸裁剪区域
    # 计算裁剪尺寸（优先保证完整裁剪区域）
    crop_width = min(w_ori, target_width)
    crop_height = min(h_ori, target_height)
    
    # 如果原图尺寸小于目标尺寸，保持原图尺寸
    if w_ori < target_width or h_ori < target_height:
        print(f"[WARN] Image {image_name} is smaller than target size ({w_ori}x{h_ori} < {target_width}x{target_height})")
        crop_width = w_ori
        crop_height = h_ori
    
    # 计算裁剪区域（纵向裁剪）
    x_center = w_ori // 2  # 水平居中
    y_center = int(center_y_for_crop)  # 以目标类别为纵向中心
    
    x1 = max(0, x_center - crop_width // 2)
    x2 = x1 + crop_width
    if x2 > w_ori:
        x2 = w_ori
        x1 = w_ori - crop_width
        if x1 < 0:
            x1 = 0
            x2 = w_ori
    
    y1 = max(0, y_center - crop_height // 2)
    y2 = y1 + crop_height
    if y2 > h_ori:
        y2 = h_ori
        y1 = h_ori - crop_height
        if y1 < 0:
            y1 = 0
            y2 = h_ori

    # 裁剪图像（不缩放）
    cropped_img = img[y1:y2, x1:x2]

    # 转换标签坐标
    new_labels = []
    for format_type, cls_id, data in labels_data:
        if format_type == 'yolo':
            x, y, w, h = data
            abs_x = x * w_ori
            abs_y = y * h_ori
            abs_w = w * w_ori
            abs_h = h * h_ori

            # 判断是否在裁剪范围内
            if abs_x < x1 or abs_x > x2 or abs_y < y1 or abs_y > y2:
                continue

            # 裁剪后坐标（不缩放）
            new_x = abs_x - x1
            new_y = abs_y - y1

            # 归一化到裁剪后的图像尺寸
            norm_x = new_x / crop_width
            norm_y = new_y / crop_height
            norm_w = abs_w / crop_width
            norm_h = abs_h / crop_height

            new_labels.append(f"{cls_id} {norm_x:.6f} {norm_y:.6f} {norm_w:.6f} {norm_h:.6f}")
            
        elif format_type == 'polygon':
            coords = data
            new_coords = []
            in_crop_area = False
            
            for i in range(0, 8, 2):
                abs_x = coords[i] * w_ori
                abs_y = coords[i+1] * h_ori
                
                # 检查是否有顶点在裁剪区域内
                if x1 <= abs_x <= x2 and y1 <= abs_y <= y2:
                    in_crop_area = True
                
                # 转换坐标（不缩放）
                new_x = abs_x - x1
                new_y = abs_y - y1
                
                # 归一化到裁剪后的图像尺寸
                norm_x = new_x / crop_width
                norm_y = new_y / crop_height
                
                new_coords.extend([norm_x, norm_y])
            
            # 只保留在裁剪区域内的多边形
            if in_crop_area:
                coord_str = " ".join([f"{coord:.5f}" for coord in new_coords])
                new_labels.append(f"{cls_id:.5f} {coord_str}")

    # 保存处理后的图像和标签
    save_img_path = os.path.join(save_image_dir, image_name)
    save_lbl_path = os.path.join(save_label_dir, os.path.splitext(image_name)[0] + ".txt")
    cv2.imwrite(save_img_path, cropped_img)
    with open(save_lbl_path, 'w') as f:
        f.write("\n".join(new_labels))

    print(f"[INFO] Processed {image_name}")
