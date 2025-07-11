import os
import cv2
import glob
import numpy as np

# === 设置 ===

src_pts_img = [  # 原图图像上的点（归一化之后恢复出来）
    (235.74821, 98.21249),
    (97.96821, 235.99249),
    (235.74821, 736.4593),
    (373.52821, 235.99249)
]

dst_pts_obj = [  # 物体图上的目标点（物理坐标）
    (65, 381),
    (174, 736.4593),
    (297.5, 736.4593),
    (406.5, 381)
]

# 要变换的 tag_id 列表
tag_ids_to_transform = {2, 5}


def compute_homography(src, dst):
    src = np.array(src, dtype=np.float32)
    dst = np.array(dst, dtype=np.float32)
    H, _ = cv2.findHomography(src, dst)
    return H


def process_file(txt_path, out_path, tag_filter):
    lines_out = []
    with open(txt_path, 'r') as f:
        for line in f:
            tokens = line.strip().split()
            if len(tokens) != 9:
                lines_out.append(line)
                continue
            tag_id = int(float(tokens[0]))
            coords_norm = list(map(float, tokens[1:]))
            coords_points = [(coords_norm[i], coords_norm[i+1]) for i in range(0, len(coords_norm), 2)]
            H = compute_homography(src_pts_img, coords_points)

            if tag_id in tag_filter:
                pts = np.array(dst_pts_obj, dtype=np.float32).reshape(-1, 1, 2)
                transformed = cv2.perspectiveTransform(pts, H).reshape(-1, 2)
                # 再归一化（注意是除以物体宽高）
                coords_new_norm = [(x , y ) for x, y in transformed]
                flat = [f"{val:.6f}" for pt in coords_new_norm for val in pt]
                new_line = f"{tag_id} {' '.join(flat)}\n"
                lines_out.append(new_line)
            else:
                lines_out.append(line)

    with open(out_path, 'w') as f:
        f.writelines(lines_out)
    print(f"写入完成：{out_path}")


def process_folder(txt_folder, output_folder, tag_ids, src_pts_img, dst_pts_obj):
    os.makedirs(output_folder, exist_ok=True)
    txt_files = glob.glob(os.path.join(txt_folder, "*.txt"))
    for txt_file in txt_files:
        out_path = os.path.join(output_folder, os.path.basename(txt_file))
        process_file(txt_file, out_path, tag_ids)

if __name__ == "__main__":
    process_folder(
        txt_folder='/home/mengrey/Documents/local_videos/data_generator/Data/20250627_energy_test/labels',
        output_folder='/home/mengrey/Documents/local_videos/data_generator/Data/20250627_energy_test/labels_transformed',
        tag_ids=tag_ids_to_transform,
        src_pts_img=src_pts_img,
        dst_pts_obj=dst_pts_obj
    )
