from views import process_pose_estimation
import cv2
from implement_mediapipe import implement

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    # 检查摄像头是否成功打开
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("无法打开摄像头。请检查连接或驱动程序。")
            break

        # 在窗口中显示帧
        cv2.imshow('Camera', image)

        # 如果按下空格键，则执行姿势估计
        if cv2.waitKey(1) == 32:  # 空格键的ASCII码是32
            run_time=300
            cv2.destroyWindow('Camera')
            # process_pose_estimation(cap, run_time)
            implement().process_pose_estimation()
        if cv2.waitKey(1) == 27:
            break

    # 释放摄像头并关闭窗口
    cap.release()
    cv2.destroyAllWindows()