import os
import random
import shutil

def select_random_images(src_folder, dst_folder, num_images=50):
    # 创建目标文件夹（如果不存在）
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    # 获取所有图片文件（支持常见格式）
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
    all_images = [f for f in os.listdir(src_folder) if f.lower().endswith(image_extensions)]

    # 检查是否有足够的图片
    if len(all_images) < num_images:
        raise ValueError(f"源文件夹中只有 {len(all_images)} 张图片，少于 {num_images} 张。")

    # 随机选择
    selected_images = random.sample(all_images, num_images)

    # 复制图片到目标文件夹
    for img_name in selected_images:
        src_path = os.path.join(src_folder, img_name)
        dst_path = os.path.join(dst_folder, img_name)
        shutil.move(src_path, dst_path)

    print(f"已成功从 '{src_folder}' 中抽取 {num_images} 张图片并复制到 '{dst_folder}'。")

# 示例用法
if __name__ == "__main__":
    source_folder = "/home/mengrey/Downloads/energy_new_dataset_20250514/ybw"   # 替换为你的源文件夹路径
    destination_folder = "/home/mengrey/Downloads/energy_new_dataset_20250514/flx"  # 替换为你的目标文件夹路径
    select_random_images(source_folder, destination_folder)
