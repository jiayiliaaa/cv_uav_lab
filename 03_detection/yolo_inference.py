# ==========================================
# Day 10：YOLO 预训练模型批量推理
# 目标：对 images/ 里的所有图片做检测，保存带框结果
# ==========================================

from ultralytics import YOLO   # 导入 Ultralytics 的 YOLO 类，用来加载模型和推理
import os                       # 操作文件和目录路径
import time                     # 计时，用来统计每张图的推理耗时

# --- 1. 加载预训练模型 ---
# 'yolov8n.pt' 是 YOLOv8 nano 版权重，首次运行会自动从 GitHub 下载
# 如果你想用更大的模型，可以换成 'yolov8s.pt'、'yolov8m.pt'，但速度更慢
model = YOLO('yolov8n.pt')

# --- 2. 准备图片文件夹 ---
image_dir = 'images'   # 图片存放目录（相对路径，相对于当前脚本所在目录）

# os.listdir 列出目录下所有文件
# 列表推导式过滤出以 .jpg / .png / .jpeg 结尾的文件
# sorted 保证文件按名字顺序排列，方便结果可复现
image_files = sorted([f for f in os.listdir(image_dir)
                      if f.endswith(('.jpg', '.png', '.jpeg'))])

# 打印找到的图片数量，方便确认
print(f"共找到 {len(image_files)} 张图片，开始推理...\n")

# --- 3. 逐张推理 ---
total_time = 0   # 累计所有图片的推理耗时

for img_file in image_files:
    # os.path.join 拼接出完整路径，比如 'images/000000000009.jpg'
    img_path = os.path.join(image_dir, img_file)

    # 记录开始时间
    start = time.time()

    # 调用模型推理。 = 一个封装好的功能。返回一个列表，results[0] 是这张图的检测结果对象
    results = model(img_path)

    # 记录结束时间，算出耗时
    elapsed = time.time() - start
    total_time += elapsed

    # 保存带检测框的图片到 results/ 下，文件名加 'result_' 前缀
    output_path = os.path.join('results', f'result_{img_file}')
    results[0].save(filename=output_path)

    # 提取检测框信息
    boxes = results[0].boxes          # 该图片所有检测框的集合
    # boxes.cls 是每个框的类别索引（张量），int(c) 转成整数
    # model.names 是 {类别ID: 类别名} 的字典，比如 {0: 'person', 2: 'car'}
    class_names = [model.names[int(c)] for c in boxes.cls]

    # 打印本张图的检测结果：文件名、目标数、类别列表、耗时（毫秒）
    print(f"{img_file}: {len(boxes)} 个目标 | {class_names} | {elapsed*1000:.1f}ms")

# --- 4. 汇总 ---
print(f"\n全部完成！总共耗时 {total_time:.2f} 秒")
print(f"结果已保存到 results/ 文件夹")