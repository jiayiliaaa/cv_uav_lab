# cv_uav_lab
> 计算机视觉与三维无人机目标感知、跟踪与轨迹预测学习实验室。

本项目记录了从 PyTorch 基础到 YOLO 目标检测、卡尔曼滤波多目标跟踪（SORT）的完整实践历程。

## 🚀 核心项目：无人机视角小目标检测与多目标跟踪 (YOLOv8 + SORT)

- **项目简介**：基于 VisDrone 数据集微调 YOLOv8，结合自研的 SORT 跟踪算法，实现无人机视频流中的多目标稳定 ID 分配与轨迹平滑。
- **技术栈**：Python, PyTorch, OpenCV, NumPy, SciPy。
- **核心产出**：
  1. `03_detection/`：完成了 VisDrone 数据集的 YOLOv8 微调训练，产出了针对小目标的 `best.pt` 权重，并生成了混淆矩阵与 PR 曲线进行误差分析。
  2. `04_tracking/`：**从零手写**了基于 7 维状态空间的卡尔曼滤波器（Kalman Filter），利用匈牙利算法（Hungarian Algorithm）实现全局最优 IoU 匹配，成功串联 YOLO 输出，实现了视频级的轨迹跟踪与 ID 维持。

## 📁 目录结构
- `02_pytorch/`：PyTorch 基础训练闭环实验（线性回归、MNIST CNN）。
- `03_detection/`：YOLO 批量推理、IoU/NMS 手写实现、VisDrone 微调。
- `04_tracking/`：卡尔曼滤波、匈牙利匹配、YOLO+SORT 完整视频跟踪管线。
- `08_remote_sensing/`：遥感图像场景分类（EuroSAT + ResNet18 迁移学习）。
- `notes/`：底层算法理论手写笔记（卡尔曼、SORT、IoU 等）。

## 🛠️ 实验原则
1. 每次实验记录环境、数据、参数、命令、结果和结论。
2. 大型原始数据集与模型权重不直接提交到 Git（已配置 `.gitignore`）。
3. 代码、配置和实验结果尽量做到可重复。
