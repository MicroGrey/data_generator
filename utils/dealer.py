import os
import shutil
import random

def distribute_files(source_dir, target_dir, shuffle_files=True):
    # 获取所有目标子文件夹
    subfolders = [os.path.join(target_dir, d) for d in os.listdir(target_dir)
                  if os.path.isdir(os.path.join(target_dir, d))]
    subfolders.sort()  # 可选：排序保持一致性
    if not subfolders:
        print("目标文件夹下没有任何子文件夹！")
        return

    # 获取源文件列表
    files = [f for f in os.listdir(source_dir)
             if os.path.isfile(os.path.join(source_dir, f))]

    if shuffle_files:
        random.shuffle(files)  # 随机打乱文件顺序

    print(f"共 {len(files)} 个文件，将平均分给 {len(subfolders)} 个子文件夹。")

    # 轮流分发
    for i, file_name in enumerate(files):
        src_path = os.path.join(source_dir, file_name)
        dst_folder = subfolders[i % len(subfolders)]
        dst_path = os.path.join(dst_folder, file_name)
        shutil.copy2(src_path, dst_path)
        print(f"复制 {file_name} 到 {dst_folder}")

# 示例用法
source_dir = '../vali/labels'
target_dir ='../vali/labels_new'

distribute_files(source_dir, target_dir, shuffle_files=True)
