import cv2
import os

# 参数配置
video_directory = '/home/mengrey/Documents/local_videos/2025-06-25_11_51_14'
output_dir = '/home/mengrey/Documents/local_videos/image/blue'
interval_sec = 0.5  # 每隔多少秒提一帧

# 创建输出文件夹
os.makedirs(output_dir, exist_ok=True)

# 遍历所有视频文件（支持 .avi, .mkv）
for video_name in os.listdir(video_directory):
    if not (video_name.endswith('.avi') or video_name.endswith('.mkv')):
        continue  # 只处理 .avi 和 .mkv 文件

    full_video_path = os.path.join(video_directory, video_name)
    save_prefix = os.path.splitext(video_name)[0]  # 如 Video_20250510230513482

    print(f"Processing {video_name}...")

    cap = cv2.VideoCapture(full_video_path)
    if not cap.isOpened():
        print(f"Cannot open video {video_name}!")
        continue

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    
    # 检查值是否有效
    if fps <= 0 or total_frames <= 0:
        print(f"警告: 无法获取有效的视频信息 fps={fps}, frames={total_frames}")
        print("尝试逐帧读取...")
        
        frame_num = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_num % int(fps * interval_sec) == 0:  # 按间隔提取
                output_path = os.path.join(output_dir, f'{save_prefix}_{frame_num//int(fps * interval_sec)}.png')
                
                # 处理文件同名的情况
                counter = 0
                base_output_path = output_path
                while os.path.exists(output_path):
                    counter += 1
                    name_without_ext = os.path.splitext(base_output_path)[0]
                    output_path = f"{name_without_ext}_{counter}.png"
                
                cv2.imwrite(output_path, frame)
                print(f"保存帧到 {output_path}")
            
            frame_num += 1
            
        print(f"✅ 成功提取帧自视频 {video_name}")
    else:
        duration = total_frames / fps
        print(f"fps: {fps}, total frames: {int(total_frames)}, duration: {duration:.2f}s")

        sec = 0
        frame_num = 0

        while sec < duration:
            frame_index = int(sec * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = cap.read()

            if not ret:
                print(f"无法读取帧 sec={sec:.2f}, index={frame_index}")
                break

            output_path = os.path.join(output_dir, f'{save_prefix}_{frame_num}.png')
            
            # 处理文件同名的情况
            counter = 0
            base_output_path = output_path
            while os.path.exists(output_path):
                counter += 1
                name_without_ext = os.path.splitext(base_output_path)[0]
                output_path = f"{name_without_ext}_{counter}.png"
            
            cv2.imwrite(output_path, frame)
            print(f"保存帧到 {output_path}")

            frame_num += 1
            sec += interval_sec

    cap.release()
    print(f"✅ 视频 {video_name} 处理完成")

print("全部视频处理完成 ✅")