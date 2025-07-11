import os
import math

# 假设图像分辨率为如下值（可以根据实际情况调整）
IMG_WIDTH = 1280
IMG_HEIGHT = 768
LOG_PATH = "log/log.txt"

def log_(type_, file_name, message):
    with open(LOG_PATH, 'a') as log_file:
        log_file.write(f"[[{type_}]]: {message}\n")

def log___(file_name):
    with open(LOG_PATH, 'a') as log_file:
        log_file.write(f"{file_name}\n")

def parse_line(line):
    parts = line.strip().split()
    if len(parts) != 10:
        raise ValueError("每行必须包含4个点+2个tag，共10个数")
    coords = list(map(float, parts[:8]))
    tags = list(map(int, parts[8:]))
    return coords, tags

def get_center(points):
    xs = [points[i] for i in range(0, 8, 2)]
    ys = [points[i] for i in range(1, 8, 2)]
    cx = sum(xs) / 4 * IMG_WIDTH
    cy = sum(ys) / 4 * IMG_HEIGHT
    return cx, cy

def distance(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def is_ccw(pt1, pt2, pt3):
    """if true, pt1-pt2 is in the counter-clockwise of pt1-pt3"""
    return (pt2[0] - pt1[0]) * (pt3[1] - pt1[1]) - (pt2[1] - pt1[1]) * (pt3[0] - pt1[0]) < 0

def filter(filepath, points, center):
    # 计算每个点到中心的距离
    pts = [(points[i]*IMG_WIDTH, points[i+1]*IMG_HEIGHT) for i in range(0, 8, 2)]
    distances = [distance(center, pts[i]) for i in range(4)]
    # 找到最远的点
    if distances[0] != max(distances):
        log___(filepath)
        raise ValueError("第一个点不是最远点")
    return is_ccw(pts[0], pts[1], pts[2]) and is_ccw(pts[1], pts[2], pts[3]) and is_ccw(pts[2], pts[3], pts[0])
    

def check_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    if len(lines) == 1:
        return  # 合规
    elif len(lines) != 2:
        raise ValueError(f"{filepath}: 文件行数不是1或2")
    
    coords1, tags1 = parse_line(lines[0])
    coords2, tags2 = parse_line(lines[1])
    # 判断最后一位 tag 是否相同
    if tags1[1] != tags2[1]:
        raise ValueError(f"{filepath}: 最后一位 tag 不同：{tags1[1]} vs {tags2[1]}")

    # 判断倒数第二位 tag 是否相同且为 0 或 1
    if tags1[0] == tags2[0] and tags1[0] in [0, 1]:
        raise ValueError(f"{filepath}: 倒数第二位 tag 相同且为 {tags1[0]}")

    # 分别找出 tag 为 0 和 1 的
    if tags1[0] == 0 and tags2[0] == 1:
        base_coords, test_coords = coords1, coords2
    elif tags1[0] == 1 and tags2[0] == 0:
        base_coords, test_coords = coords2, coords1
    else:
        raise ValueError(f"{filepath}: 倒数第二位 tag 非法组合 {tags1[0]}, {tags2[0]}")

    center = get_center(base_coords)
    if not filter(filepath, test_coords, center):
        raise ValueError(f"{filepath}: tag=1 的点未按照逆时针顺序排列")

def check_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            try:
                check_file(os.path.join(folder_path, filename))
                print(f"{filename}: 合法")
            except Exception as e:
                log___(filename)
                print(f"{filename}: 错误 - {e}")
                
def main():
    folder_path = "/home/siberia/zhaodingyi/Work/rm/rm.cv/all"
    # 替换为实际路径
    check_folder(folder_path)
    print("检查完成")

if __name__ == "__main__":
    main()