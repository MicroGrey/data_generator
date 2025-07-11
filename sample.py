import os
import shutil
import random
from glob import glob

# 设置源文件夹
red_dir = '/home/mengrey/Documents/local_videos/image/red'
blue_dirs = ['/home/mengrey/Documents/local_videos/image/blue']

# 设置目标参数
total_images = 60
red_count = blue_count = total_images // 2
target_folder_num = 2
output_prefix = '/home/mengrey/Documents/local_videos/image/samples'

# 获取图像路径
def get_images_from_folder(folder):
    exts = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tif']
    files = []
    for ext in exts:
        files.extend(glob(os.path.join(folder, ext)))
    return files

red_images = get_images_from_folder(red_dir)
blue_images = []
for blue_dir in blue_dirs:
    blue_images.extend(get_images_from_folder(blue_dir))

# 检查图像数量是否充足
assert len(red_images) >= red_count, f"red文件夹中图片不足：需要{red_count}，仅有{len(red_images)}"
assert len(blue_images) >= blue_count, f"blue文件夹中图片不足：需要{blue_count}，仅有{len(blue_images)}"

# 随机采样
red_sample = random.sample(red_images, red_count)
blue_sample = random.sample(blue_images, blue_count)

# 合并并打乱
all_images = red_sample + blue_sample
random.shuffle(all_images)

# 创建输出文件夹
for i in range(target_folder_num):
    os.makedirs(f"{output_prefix}{i}", exist_ok=True)

# 分配图像
for idx, img_path in enumerate(all_images):
    folder_idx = idx % target_folder_num
    target_path = os.path.join(f"{output_prefix}{folder_idx}", os.path.basename(img_path))
    shutil.copy(img_path, target_path)

print(f"✅ 分发完成，共 {total_images} 张图像，已分入 {target_folder_num} 个文件夹。")