import os
# 导入 os 模块 用来处理文件夹、文件路径、文件名等操作
image_dir = "images"
# 图片文件夹路径
# 当前 script.py 在 03_detection 下
# 所以这里的 "images" 指的是：
# 03_detection/images/

label_dir = "labels"
# YOLO 标签文件夹路径
# 03_detection/labels/


image_files = os.listdir(image_dir)
# os.listdir()：获取指定文件夹中的所有文件和文件夹名称
# 例如 images 中有：
# 000000000009.jpg
# 000000000025.jpg
# 那么 image_files 大概就是：
# ["000000000009.jpg", "000000000025.jpg"]

label_files = os.listdir(label_dir)
# 获取 labels 文件夹中的所有文件
# ["000000000009.txt", "000000000025.txt"]

image_names = set()
# 创建一个空集合
# 我们最终只保存图片的“文件名主体”
# 000000000009.jpg
# ↓
# 000000000009

label_names = set()
# 创建一个空集合用来保存 label 的文件名主体
# 000000000009.txt
# ↓
# 000000000009

for file in image_files:
    # 遍历 images 文件夹中的每一个文件
    name = os.path.splitext(file)[0]
    # os.path.splitext() 可以把“文件名”和“扩展名”分开
    # "000000000009.jpg"会得到：
    # ("000000000009", ".jpg")
    # [0] 表示取第一个元素
    # 所以 name = "000000000009"

    image_names.add(name)
    # 把文件名主体加入 image_names 集合
    # 最后可能得到：
    # {
    #     "000000000009",
    #     "000000000025",
    #     "000000000030"
    # }

for file in label_files:
    # 遍历 labels 文件夹中的每一个文件

    name = os.path.splitext(file)[0]
    # 去掉 .txt
    # "000000000009.txt"
    # ↓
    # "000000000009"

    label_names.add(name)
    # 把 label 文件名主体加入 label_names 集合
# ==================================================
# 1. 检查图片和标签是否一一对应
# ==================================================

missing_labels = image_names - label_names
# 集合的“差集”
# image_names - label_names
#
# 意思是：
# 图片有，但是 label 没有
# image_names = {A, B, C}
# label_names = {A, B}
# 那么：missing_labels = {C}
# 表示 C 这张图片没有对应的 label

missing_images = label_names - image_names
# 反过来检查：label 有，但是图片没有
# image_names = {A, B}
# label_names = {A, B, C}
# missing_images = {C}
print("图片数量：", len(image_names))
# len() 计算集合中有多少个元素  输出图片数量
print("标签数量：", len(label_names))
# 输出 label 数量

print("\n缺少 label 的图片：")

for name in missing_labels:
    # 遍历所有“缺少 label 的图片”
    print(name)
    # 输出图片名称

print("\n缺少 image 的 label：")
for name in missing_images:
    # 遍历所有“缺少图片的 label”
    print(name)
    # 输出对应的 label 名称
# ==================================================
# 2. 检查 YOLO 标签内容
# ==================================================
print("\n开始检查标签内容...")
#接下来开始检查 txt 文件内部的数据
bad_labels = []
# 创建一个空列表 用来保存发现的错误
#
# 例如：
# [
#     "000000000009.txt 第 2 行：格式错误",
#     "000000000025.txt 第 1 行：width 超出范围"
# ]

for file in label_files:
    # 一个一个检查 labels 文件夹中的 txt 文件
    label_path = os.path.join(label_dir, file)
    # os.path.join() 用来拼接文件路径
    # label_dir = "labels"
    # file = "000000000009.txt"

    # label_path =
    # "labels/000000000009.txt"

    with open(label_path, "r") as f:
        # 打开当前 label 文件  "r" = read表示读取文件
        # with 的好处是：
        # 文件读取完成后会自动关闭

        lines = f.readlines()
        # 读取文件中的所有行
        # 1 0.125 0.275 0.05 0.05
        # 2 0.550 0.425 0.10 0.10
        # lines 大概是：
        #
        # [
        #     "1 0.125 0.275 0.05 0.05\n",
        #     "2 0.550 0.425 0.10 0.10\n"
        # ]

    for line_number, line in enumerate(lines, start=1):
        # 一行一行检查
        # enumerate() 可以同时得到：line_number → 当前是第几行
        # line → 当前这一行的内容
        # start=1 表示从第 1 行开始计数
        # 例如：
        # 第一次：
        # line_number = 1
        #
        # 第二次：
        # line_number = 2
        parts = line.strip().split()
        # 这一句非常重要
        # strip()：
        # 去掉这一行前后的空格和换行符
        # split()：
        # 按空格拆分

        # "1 0.125 0.275 0.05 0.05\n"
        # ↓ strip()
        # "1 0.125 0.275 0.05 0.05"
        # ↓ split()
        # [
        #     "1",
        #     "0.125",
        #     "0.275",
        #     "0.05",
        #     "0.05"
        # ]
        # ==========================================
        # YOLO 一行必须有 5 个值
        # ==========================================

        if len(parts) != 5:
            #正常 Y0LO 格式：
            # class_id
            # x_center
            # y_center
            # width
            # height
            bad_labels.append(
                f"{file} 第 {line_number} 行：格式错误"
            )
            # 把错误信息保存到 bad_labels 列表
            # f"..." 是 Python 的 f-string可以把变量直接放进字符串中
            # 例如：
            #
            # file = "000000000009.txt"
            # line_number = 2
            # "000000000009.txt 第 2 行：格式错误"
            continue
            # 发现这一行格式错误后不再继续处理这一行
            # 直接进入下一行


        class_id = int(parts[0])
        # 第 0 个数据是类别编号
        # int() 把字符串 "1"转换成整数 1


        x_center = float(parts[1])
        # 第 1 个数据是 bbox 中心点 x
        # float() 把字符串转换成小数
        y_center = float(parts[2])
        # 第 2 个数据是 bbox 中心点 y
        width = float(parts[3])
        # 第 3 个数据是 bbox 宽度
        height = float(parts[4])
        # 第 4 个数据是 bbox 高度

        # 检查 x_center 是否在 0~1
        if not (0 <= x_center <= 1):
            # YOLO 归一化坐标应该在 0~1
            # not 表示“不是”not (0 <= x_center <= 1)就是：x_center 不在 0~1 范围内

            bad_labels.append(
                f"{file} 第 {line_number} 行：x_center 超出范围"
            )
            # 把错误信息保存下来

        if not (0 <= y_center <= 1):
            bad_labels.append(
                f"{file} 第 {line_number} 行：y_center 超出范围"
            )
        if not (0 <= width <= 1):
            bad_labels.append(
                f"{file} 第 {line_number} 行：width 超出范围"
            )

        if not (0 <= height <= 1):
            # 检查 bbox 高度是否在 0~1
            bad_labels.append(
                f"{file} 第 {line_number} 行：height 超出范围"
            )
# ==================================================
# 3. 输出最终检查结果
# ==================================================
print("\n====================")
# 输出一个分隔线，让结果更清楚

if len(bad_labels) == 0:
    # 如果 bad_labels 里面没有任何错误
    #
    # len(bad_labels) == 0
    # 没有发现错误
    print("标签内容检查通过！")
    # 输出检查通过


else:
    print("发现问题：")
    # 提示发现问题

    for error in bad_labels:
        # 遍历所有错误信息
        print(error)
        # 一个一个打印出来