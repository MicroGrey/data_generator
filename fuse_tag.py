import os

def convert_tags(tag1, tag2):
    """将最后的两个标签转换为单个数字"""
    if tag1 == 0 and tag2 == 0:
        return 0
    elif tag1 == 0 and tag2 == 1:
        return 1
    elif tag1 == 1 and tag2 == 0:
        return 2
    elif tag1 == 1 and tag2 == 1:
        return 3
    else:
        raise ValueError(f"Invalid tags: {tag1}, {tag2}")

def process_file(input_path, output_path):
    """处理单个文件"""
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            # 移除前后空白并分割数据
            parts = line.strip().split()
            
            # 确保数据格式正确
            if len(parts) != 10:  # 8个数字+2个标签
                continue
                
            # 提取前8个数字和最后两个标签
            numbers = parts[:8]
            tag1, tag2 = map(int, parts[8:])
            
            # 转换标签
            new_tag = convert_tags(tag1, tag2)
            
            # 写入新格式
            new_line = f"{new_tag} {' '.join(numbers)}\n"
            outfile.write(new_line)

def process_all_files(input_dir, output_dir):
    """处理输入目录中的所有txt文件"""
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历输入目录中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            process_file(input_path, output_path)
            print(f"Processed: {filename}")

# 使用示例
input_directory = '../vali/labels'  # 原始数据文件夹
output_directory = '../vali/sampled_labels'  # 输出文件夹

process_all_files(input_directory, output_directory)