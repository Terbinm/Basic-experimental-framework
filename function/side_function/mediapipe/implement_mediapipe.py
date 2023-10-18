from mp_setting import mp_set
from point_set import p_set
from frame_data import frame_datas
import cv2
import time
import json
import os

class implement():
    def __init__(self):
        self.PoseDetector = mp_set()
        self.point_set = p_set()
        self.frame_data = frame_datas()

        self.pose_data = []
        self.point_data = None
        self.image = None
        # self.run_time = config_data["mediapipe"]["run_time"]
        self.run_time = 30
        self.start_time = time.time()

        self.frame = None


    def process_pose_estimation(self):
        self.out =  self.save_video()
        while self.PoseDetector.cap.isOpened():
            self.image = self.frame_data.point_set_import()
            #frame_data矩陣寫入
            self.frame = self.frame_data.record_point()
            self.pose_data.append(self.frame)
            # self.pose_data.append(self.point_data)
            # 将帧写入输出视频
            self.out.write(self.image)
            # self.video_point.image_point()
            self.frame_data.image_point()


            if cv2.waitKey(1) == 27 or (self.start_time > 100 and time.time()
                - self.start_time >= self.run_time):
                # 在程序结束时创建独立的JSON文件
                self.json_data()
                break


        self.out.release()
        cv2.destroyAllWindows()


    def save_video(self):
        video_folder = "video"
        if not os.path.exists(video_folder):
            os.makedirs(video_folder)

        # 设置视频编码器
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # 创建一个名字基于当前时间的唯一文件名
        output_filename = os.path.join(video_folder, f"out_video.avi")
        out = cv2.VideoWriter(output_filename, fourcc, 20.0, (640, 480))  #偵率
        return(out)


    def json_data(self):
        # 定义要保存 JSON 文件的文件夹路径
        json_folder = "json"

        # 确保文件夹存在，如果不存在就创建它
        if not os.path.exists(json_folder):
            os.makedirs(json_folder)

        # 创建完整的文件路径
        output_filename = os.path.join(json_folder, f"pose_data.json")
        with open(output_filename, "w", encoding='utf-8') as json_file:
            json.dump(self.pose_data, json_file, indent=4, ensure_ascii=False)
