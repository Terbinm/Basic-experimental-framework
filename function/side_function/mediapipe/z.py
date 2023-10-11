import cv2
import torch
import torchvision.transforms as T
from torchvision.models.detection import fasterrcnn_resnet50_fpn
import numpy as np

# 加载Faster R-CNN模型（你也可以选择其他模型）
model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# 使用CPU或GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 相机内部参数（根据你的相机）
focal_length_x = 1000  # 焦距X轴
focal_length_y = 1000  # 焦距Y轴
center_x = 320  # 图像中心X坐标
center_y = 240  # 图像中心Y坐标

# 转换函数，将图像从OpenCV格式转换为Torch张量
transform = T.Compose([T.ToPILImage(), T.ToTensor()])

# 打开摄像头
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 转换图像并传递给模型
    input_image = transform(frame).to(device)
    with torch.no_grad():
        prediction = model([input_image])

    # 提取预测结果
    boxes = prediction[0]['boxes'].cpu().numpy()
    scores = prediction[0]['scores'].cpu().numpy()

    # 获取置信度高于阈值的框
    threshold = 0.5
    selected_boxes = boxes[scores > threshold]

    # 在图像上绘制检测到的框
    for box in selected_boxes:
        x1, y1, x2, y2 = box.astype(int)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 计算距离
        object_width = x2 - x1  # 检测到的物体宽度（像素）
        distance = (focal_length_x * object_width) / (x2 - center_x)
        print(f"估计的距离：{distance} 厘米")

    # 显示图像
    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 关闭摄像头
cap.release()
cv2.destroyAllWindows()
