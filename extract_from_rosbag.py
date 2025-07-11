import rosbag
import cv2
import numpy as np
import os

# ======== 参数设置 ========
bag_path = '广工/2025-04-09-15-56-39.bag'  # 替换为你的 .bag 文件路径
image_topic = '/hk_camera/image_raw/compressed'  # 替换为你的图像话题名
fps = 30  # 你希望的视频帧率
video_codec = 'XVID'  # 可选：'XVID', 'MJPG', 'mp4v'

# ======== 自动设置输出路径（与bag同目录、同名） ========
base_name = os.path.splitext(os.path.basename(bag_path))[0]
output_dir = os.path.dirname(os.path.abspath(bag_path))
output_video_path = os.path.join(output_dir, f"{base_name}.avi")

# ======== 初始化 ========
video_writer = None
image_size = None
frame_count = 0

print(f"处理文件: {bag_path}")
print(f"图像话题: {image_topic}")
print(f"输出路径: {output_video_path}")

with rosbag.Bag(bag_path, 'r') as bag:
    for topic, msg, t in bag.read_messages(topics=[image_topic]):
        try:
            # 解码 sensor_msgs/CompressedImage 数据
            np_arr = np.frombuffer(msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # 初始化视频写入器
            if video_writer is None:
                image_size = (cv_image.shape[1], cv_image.shape[0])  # 宽, 高
                fourcc = cv2.VideoWriter_fourcc(*video_codec)
                video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, image_size)

            video_writer.write(cv_image)
            frame_count += 1

        except Exception as e:
            print(f"跳过一帧: {e}")
            continue

if video_writer:
    video_writer.release()

print(f"✅ 视频提取完成：{output_video_path}，共 {frame_count} 帧。")
