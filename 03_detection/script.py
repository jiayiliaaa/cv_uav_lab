import os
import cv2


def convert_annotation(image_path, annotation_path, output_path):

    image = cv2.imread(image_path)

    H = image.shape[0]
    W = image.shape[1]

    with open(annotation_path, "r") as f:
        lines = f.readlines()

    with open(output_path, "w") as f:

        for line in lines:

            part = line.split(",")

            x = float(part[0])
            y = float(part[1])
            w = float(part[2])
            h = float(part[3])

            category = int(part[5])

            x_center = x + w / 2
            y_center = y + h / 2

            x_center = x_center / W
            y_center = y_center / H
            width = w / W
            height = h / H

            class_id = category - 1

            result = [
                class_id,
                x_center,
                y_center,
                width,
                height
            ]

            output_line = " ".join(str(x) for x in result)

            f.write(output_line + "\n")


# =========================
# 批量转换
# =========================

image_dir = "images"
annotation_dir = "annotations"
label_dir = "labels"

os.makedirs(label_dir, exist_ok=True)


for image_name in os.listdir(image_dir):

    image_path = os.path.join(
        image_dir,
        image_name
    )

    annotation_name = image_name.replace(
        ".jpg",
        ".txt"
    )

    annotation_path = os.path.join(
        annotation_dir,
        annotation_name
    )

    output_path = os.path.join(
        label_dir,
        annotation_name
    )

    convert_annotation(
        image_path,
        annotation_path,
        output_path
    )
    for image_name in os.listdir(image_dir):
        image_path = os.path.join(image_dir, image_name)

        annotation_name = image_name.replace(".jpg", ".txt")

        annotation_path = os.path.join(annotation_dir, annotation_name)

        output_path = os.path.join(label_dir, annotation_name)

        convert_annotation(image_path, annotation_path, output_path)
for image_name in os.listdir(image_dir):

    image_path = os.path.join(image_dir, image_name)

    annotation_name = image_name.replace(".jpg", ".txt")

    annotation_path = os.path.join(annotation_dir, annotation_name)

    output_path = os.path.join(label_dir, annotation_name)

    convert_annotation(image_path, annotation_path, output_path)