import rosbag
import cv2
import numpy as np
import os

# ======== 参数设置 ========
input_folder = '/home/mengrey/Workspace/data_generator/Data/1st'  # 输入文件夹路径，包含多个 .bag 文件
output_folder = '/home/mengrey/Workspace/data_generator/Data/广工'  # 输出视频文件夹路径
image_topic = '/hk_camera/image_raw/compressed'  # 替换为你的图像话题名
fps = 30  # 你希望的视频帧率
video_codec = 'XVID'  # 可选：'XVID', 'MJPG', 'mp4v'

# ======== 创建输出文件夹 ========
os.makedirs(output_folder, exist_ok=True)

# ======== 遍历文件夹下所有 .bag 文件 ========
for bag_file in os.listdir(input_folder):
    if not bag_file.endswith('.bag'):
        continue

    bag_path = os.path.join(input_folder, bag_file)
    base_name = os.path.splitext(os.path.basename(bag_path))[0]
    output_video_path = os.path.join(output_folder, f"{base_name}.avi")

    video_writer = None
    image_size = None
    frame_count = 0

    print(f"处理文件: {bag_path}")
    print(f"图像话题: {image_topic}")
    print(f"输出路径: {output_video_path}")

    try:
        with rosbag.Bag(bag_path, 'r') as bag:
            for topic, msg, t in bag.read_messages(topics=[image_topic]):
                try:
                    np_arr = np.frombuffer(msg.data, np.uint8)
                    cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                    if video_writer is None:
                        image_size = (cv_image.shape[1], cv_image.shape[0])
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
    except Exception as e:
        print(f"处理 {bag_path} 时出错: {e}")

print("全部 bag 文件处理完成。")