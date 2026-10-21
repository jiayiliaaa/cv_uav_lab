def compute_iou(box1, box2):
    # box = [x1, y1, x2, y2]每个框的格式是 [x1, y1, x2, y2]，代表左上角坐标 (x1, y1) 和右下角坐标 (x2, y2)。
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
''''box1[0] 是 box1 左上角的 x 坐标，box2[0] 是 box2 左上角的 x 坐标。
取两者最大值，得到重叠区域的左上角 x 坐标。同理，y1 是重叠区域的左上角 y 坐标。
取两者最小值，得到重叠区域的右下角 x 坐标。'''
    inter = max(0, x2 - x1) * max(0, y2 - y1)
    area1 = (box1[2]-box1[0]) * (box1[3]-box1[1])
    area2 = (box2[2]-box2[0]) * (box2[3]-box2[1])
    union = area1 + area2 - inter#求交集并集
    return inter / union if union > 0 else 0 #IoU = 交集面积 ÷ 并集面积。

print(compute_iou([0,0,100,100], [50,50,150,150]))  # 应约为 0.1429