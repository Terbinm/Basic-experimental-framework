from point_set import p_set
import cv2

class frame_datas():
    def __init__(self):
        self.point_set = p_set()
        self.frame_data_list = []  # 用于存储每一帧的数据
        self.frame_data = None
        self.image = None

    def point_set_import(self):
        self.point_set.results_set()
        self.point_set.log_key_point()
        self.point_set.center_point()
        self.point_set.new_point()
        self.image = self.point_set.image
        return self.image

    def image_point(self):
        if self.point_set.results.pose_landmarks:
            prev_nose_coordinates = (int(self.point_set.nose.x * self.point_set.image_width), int(self.point_set.nose.y * self.point_set.image_height))
            prev_left_shoulder_coordinates = (int(self.point_set.left_shoulder.x * self.point_set.image_width), int(self.point_set.left_shoulder.y * self.point_set.image_height))
            prev_right_shoulder_coordinates = (int(self.point_set.right_shoulder.x * self.point_set.image_width), int(self.point_set.right_shoulder.y * self.point_set.image_height))

            cv2.putText(self.point_set.image, f'Nose (X,Y,Z): ({self.point_set.nose_coordinates[0]:.2f}, {self.point_set.nose_coordinates[1]:.2f}, {self.point_set.nose_coordinates[2]:.2f})',
                            (prev_nose_coordinates[0] + 10, prev_nose_coordinates[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 1)
            cv2.putText(self.point_set.image, f'Left Shoulder (X,Y,Z): ({self.point_set.left_shoulder_coordinates[0]:.2f}, {self.point_set.left_shoulder_coordinates[1]:.2f}, {self.point_set.left_shoulder_coordinates[2]:.2f})',
                            (prev_left_shoulder_coordinates[0] + 10, prev_left_shoulder_coordinates[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 1)
            cv2.putText(self.point_set.image, f'Right Shoulder (X,Y,Z): ({self.point_set.right_shoulder_coordinates[0]:.2f}, {self.point_set.right_shoulder_coordinates[1]:.2f}, {self.point_set.right_shoulder_coordinates[2]:.2f})',
                            (prev_right_shoulder_coordinates[0] + 10, prev_right_shoulder_coordinates[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 1)
            cv2.imshow('MediaPipe Pose', self.point_set.image)


    def record_point(self):
        self.frame_data = {}  # 为每一帧创建一个新的字典

        for i in range(32):  # 用你的实际关键点数量替换2
            landmark_name = self.point_set.mp_pose.PoseLandmark(i).name
            landmark_value = self.point_set.results.pose_landmarks.landmark[self.point_set.mp_pose.PoseLandmark(i).value]
            self.frame_data[landmark_name] = self.landmark_to_dict(landmark_value)

        # 将每一帧的数据添加到帧数据列表中
        self.frame_data_list.append(self.frame_data)

        # self.frame_data = {
        #     "鼻子": {
        #     "X": round(self.point_set.nose_coordinates[0], 2),
        #     "Y": round(self.point_set.nose_coordinates[1], 2),
        #     "Z": round(self.point_set.nose_coordinates[2], 2)
        # },
        #     "左肩": {
        #     "X": round(self.point_set.left_shoulder_coordinates[0], 2),
        #     "Y": round(self.point_set.left_shoulder_coordinates[1], 2),
        #     "Z": round(self.point_set.left_shoulder_coordinates[2], 2)
        # },
        #     "右肩": {
        #     "X": round(self.point_set.right_shoulder_coordinates[0], 2),
        #     "Y": round(self.point_set.right_shoulder_coordinates[1], 2),
        #     "Z": round(self.point_set.right_shoulder_coordinates[2], 2)
        # },
        # }
        return self.frame_data


    def landmark_to_dict(self,landmark):
        return {
            "x": landmark.x,
            "y": landmark.y,
            "z": landmark.z,
            "visibility": landmark.visibility,
        }