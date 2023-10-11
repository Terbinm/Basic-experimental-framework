from mp_setting import mp_set

class p_set():


    def __init__(self):
        self.PoseDetector = mp_set()
        self.image = None
        self.results = None
        self.mp_pose = None
        self.origin = None
        self.origin_x = None
        self.origin_y = None
        self.origin_z = None

        self.nose = None
        self.left_eye_inner = None
        self.left_eye = None
        self.left_eye_outer = None
        self.right_eye_inner = None
        self.right_eye = None
        self.right_eye_outer = None
        self.left_ear = None
        self.right_ear = None
        self.mouth_left = None
        self.mouth_right = None
        self.left_shoulder = None
        self.right_shoulder = None
        self.left_elbow = None
        self.right_elbow = None
        self.left_wrist = None
        self.right_wrist = None
        self.left_pinky = None
        self.right_pinky = None
        self.left_index = None
        self.right_index = None
        self.left_thumb = None
        self.right_thumb = None
        self.left_hip = None
        self.right_hip = None
        self.left_knee = None
        self.right_knee = None
        self.left_ankle = None
        self.right_ankle = None
        self.left_heel = None
        self.right_heel = None
        self.left_foot_index = None
        self.right_foot_index = None

        self.image_height = None
        self.image_width = None
        self.z = None

        self.nose_coordinates = None
        self.left_eye_inner_coordinates = None
        self.left_eye_coordinates = None
        self.left_eye_outer_coordinates = None
        self.right_eye_inner_coordinates = None
        self.right_eye_coordinates = None
        self.right_eye_outer_coordinates = None
        self.left_ear_coordinates = None
        self.right_ear_coordinates = None
        self.mouth_left_coordinates = None
        self.mouth_right_coordinates = None
        self.left_shoulder_coordinates = None
        self.right_shoulder_coordinates = None
        self.left_elbow_coordinates = None
        self.right_elbow_coordinates = None
        self.left_wrist_coordinates = None
        self.right_wrist_coordinates = None
        self.left_pinky_coordinates = None
        self.right_pinky_coordinates = None
        self.left_index_coordinates = None
        self.right_index_coordinates = None
        self.left_thumb_coordinates = None
        self.right_thumb_coordinates = None
        self.left_hip_coordinates = None
        self.right_hip_coordinates = None
        self.left_knee_coordinates = None
        self.right_knee_coordinates = None
        self.left_ankle_coordinates = None
        self.right_ankle_coordinates = None
        self.left_heel_coordinates = None
        self.right_heel_coordinates = None
        self.left_foot_index_coordinates = None
        self.right_foot_index_coordinates = None


    def coordinate_set(self):
        self.results_set()
        self.log_key_point()
        self.center_point()
        self.new_point()

    def results_set(self):
        self.PoseDetector.image_setting()
        self.image = self.PoseDetector.image
        self.results = self.PoseDetector.results
        self.mp_pose = self.PoseDetector.mp_pose
        self.image_height, self.image_width, self.z = self.PoseDetector.image.shape

    def log_key_point(self):
        self.nose = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.NOSE]
        self.left_eye_inner = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_EYE_INNER]
        self.left_eye = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_EYE]
        self.left_eye_outer = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_EYE_OUTER]
        self.right_eye_inner = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_EYE_INNER]
        self.right_eye = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_EYE]
        self.right_eye_outer = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_EYE_OUTER]
        self.left_ear = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_EAR]
        self.right_ear = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_EAR]
        self.mouth_left = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.MOUTH_LEFT]
        self.mouth_right = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.MOUTH_RIGHT]
        self.left_shoulder = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        self.right_shoulder = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        self.left_elbow = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW]
        self.right_elbow = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW]
        self.left_wrist = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST]
        self.right_wrist = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST]
        self.left_pinky = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_PINKY]
        self.right_pinky = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_PINKY]
        self.left_index = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_INDEX]
        self.right_index = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_INDEX]
        self.left_thumb = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_THUMB]
        self.right_thumb = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_THUMB]
        self.left_hip = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP]
        self.right_hip = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP]
        self.left_knee = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_KNEE]
        self.right_knee = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_KNEE]
        self.left_ankle = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ANKLE]
        self.right_ankle = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
        self.left_heel = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HEEL]
        self.right_heel = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HEEL]
        self.left_foot_index = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
        self.right_foot_index = self.results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]


    def center_point(self):
        # 计算新原点的坐标，即左髋和右髋坐标的平均值
        self.origin_x = (self.left_hip.x + self.right_hip.x)/2.0
        self.origin_y = (self.left_hip.y + self.right_hip.y)/2.0
        self.origin_z = (self.left_hip.z + self.right_hip.z)/2.0

        # 新原点的坐标即为新的原点
        self.origin = (self.origin_x, self.origin_y, self.origin_z)


    def new_point(self):
        # 计算鼻子的歸一化坐標
        self.nose_coordinates = (
            (self.nose.x - self.origin_x),
            (self.origin_y - self.nose.y),
            (self.nose.z)
        )
        # 计算左眼内角的歸一化坐標
        self.left_eye_inner_coordinates = (
            (self.left_eye_inner.x - self.origin_x),
            (self.origin_y - self.left_eye_inner.y),
            (self.left_eye_inner.z)
        )
        # 计算左眼的歸一化坐標
        self.left_eye_coordinates = (
            (self.left_eye.x - self.origin_x),
            (self.origin_y - self.left_eye.y),
            (self.left_eye.z)
        )
        # 计算左眼外角的歸一化坐標
        self.left_eye_outer_coordinates = (
            (self.left_eye_outer.x - self.origin_x),
            (self.origin_y - self.left_eye_outer.y),
            (self.left_eye_outer.z)
        )
        # 计算右眼内角的歸一化坐標
        self.right_eye_inner_coordinates = (
            (self.right_eye_inner.x - self.origin_x),
            (self.origin_y - self.right_eye_inner.y),
            (self.right_eye_inner.z)
        )
        # 计算右眼的歸一化坐標
        self.right_eye_coordinates = (
            (self.right_eye.x - self.origin_x),
            (self.origin_y - self.right_eye.y),
            (self.right_eye.z)
        )
        # 计算右眼外角的歸一化坐標
        self.right_eye_outer_coordinates = (
            (self.right_eye_outer.x - self.origin_x),
            (self.origin_y - self.right_eye_outer.y),
            (self.right_eye_outer.z)
        )
        # 计算左耳的歸一化坐標
        self.left_ear_coordinates = (
            (self.left_ear.x - self.origin_x),
            (self.origin_y - self.left_ear.y),
            (self.left_ear.z)
        )
        # 计算右耳的歸一化坐標
        self.right_ear_coordinates = (
            (self.right_ear.x - self.origin_x),
            (self.origin_y - self.right_ear.y),
            (self.right_ear.z)
        )
        # 计算嘴巴左角的歸一化坐標
        self.mouth_left_coordinates = (
            (self.mouth_left.x - self.origin_x),
            (self.origin_y - self.mouth_left.y),
            (self.mouth_left.z)
        )
        # 计算嘴巴右角的歸一化坐標
        self.mouth_right_coordinates = (
            (self.mouth_right.x - self.origin_x),
            (self.origin_y - self.mouth_right.y),
            (self.mouth_right.z)
        )
        # 计算左肩的歸一化坐標
        self.left_shoulder_coordinates = (
            (self.left_shoulder.x - self.origin_x),
            (self.origin_y - self.left_shoulder.y),
            (self.left_shoulder.z)
        )
        # 计算右肩的歸一化坐標
        self.right_shoulder_coordinates = (
            (self.right_shoulder.x - self.origin_x),
            (self.origin_y - self.right_shoulder.y),
            (self.right_shoulder.z)
        )
        # 计算左肘的歸一化坐標
        self.left_elbow_coordinates = (
            (self.left_elbow.x - self.origin_x),
            (self.origin_y - self.left_elbow.y),
            (self.left_elbow.z)
        )
        # 计算右肘的歸一化坐標
        self.right_elbow_coordinates = (
            (self.right_elbow.x - self.origin_x),
            (self.origin_y - self.right_elbow.y),
            (self.right_elbow.z)
        )
        # 计算左腕的歸一化坐標
        self.left_wrist_coordinates = (
            (self.left_wrist.x - self.origin_x),
            (self.origin_y - self.left_wrist.y),
            (self.left_wrist.z)
        )
        # 计算右腕的歸一化坐標
        self.right_wrist_coordinates = (
            (self.right_wrist.x - self.origin_x),
            (self.origin_y - self.right_wrist.y),
            (self.right_wrist.z)
        )
        # 计算左小指的歸一化坐標
        self.left_pinky_coordinates = (
            (self.left_pinky.x - self.origin_x),
            (self.origin_y - self.left_pinky.y),
            (self.left_pinky.z)
        )
        # 计算右小指的歸一化坐標
        self.right_pinky_coordinates = (
            (self.right_pinky.x - self.origin_x),
            (self.origin_y - self.right_pinky.y),
            (self.right_pinky.z)
        )
        # 计算左食指的歸一化坐標
        self.left_index_coordinates = (
            (self.left_index.x - self.origin_x),
            (self.origin_y - self.left_index.y),
            (self.left_index.z)
        )
        # 计算右食指的歸一化坐標
        self.right_index_coordinates = (
            (self.right_index.x - self.origin_x),
            (self.origin_y - self.right_index.y),
            (self.right_index.z)
        )
        # 计算左拇指的歸一化坐標
        self.left_thumb_coordinates = (
            (self.left_thumb.x - self.origin_x),
            (self.origin_y - self.left_thumb.y),
            (self.left_thumb.z)
        )
        # 计算右拇指的歸一化坐標
        self.right_thumb_coordinates = (
            (self.right_thumb.x - self.origin_x),
            (self.origin_y - self.right_thumb.y),
            (self.right_thumb.z)
        )
        # 计算左髋的歸一化坐標
        self.left_hip_coordinates = (
            (self.left_hip.x - self.origin_x),
            (self.origin_y - self.left_hip.y),
            (self.left_hip.z)
        )
        # 计算右髋的歸一化坐標
        self.right_hip_coordinates = (
            (self.right_hip.x - self.origin_x),
            (self.origin_y - self.right_hip.y),
            (self.right_hip.z)
        )
        # 计算左膝的歸一化坐標
        self.left_knee_coordinates = (
            (self.left_knee.x - self.origin_x),
            (self.origin_y - self.left_knee.y),
            (self.left_knee.z)
        )
        # 计算右膝的歸一化坐標
        self.right_knee_coordinates = (
            (self.right_knee.x - self.origin_x),
            (self.origin_y - self.right_knee.y),
            (self.right_knee.z)
        )
        # 计算左踝的歸一化坐標
        self.left_ankle_coordinates = (
            (self.left_ankle.x - self.origin_x),
            (self.origin_y - self.left_ankle.y),
            (self.left_ankle.z)
        )
        # 计算右踝的歸一化坐標
        self.right_ankle_coordinates = (
            (self.right_ankle.x - self.origin_x),
            (self.origin_y - self.right_ankle.y),
            (self.right_ankle.z)
        )
        # 计算左脚跟的歸一化坐標
        self.left_heel_coordinates = (
            (self.left_heel.x - self.origin_x),
            (self.origin_y - self.left_heel.y),
            (self.left_heel.z)
        )
        # 计算右脚跟的歸一化坐標
        self.right_heel_coordinates = (
            (self.right_heel.x - self.origin_x),
            (self.origin_y - self.right_heel.y),
            (self.right_heel.z)
        )
        # 计算左脚大趾的歸一化坐標
        self.left_foot_index_coordinates = (
            (self.left_foot_index.x - self.origin_x),
            (self.origin_y - self.left_foot_index.y),
            (self.left_foot_index.z)
        )
        # 计算右脚大趾的歸一化坐標
        self.right_foot_index_coordinates = (
            (self.right_foot_index.x - self.origin_x),
            (self.origin_y - self.right_foot_index.y),
            (self.right_foot_index.z)
        )


