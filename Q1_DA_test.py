import json

from matplotlib import pyplot as plt


class BoundingBox:
    def __init__(self, x_center=0, y_center=0, width=0, height=0, iou=0):
        self.x_center = x_center
        self.y_center = y_center
        self.width = width
        self.height = height
        self.iou = iou


def read_lean_map_of_bboxes(input_json_file_path: str):
    with open(input_json_file_path, 'r') as json_stream:
        raw_object = json.load(json_stream)
    return {k: [BoundingBox(**item) for item in v] for k, v in raw_object.items()}


def get_minimum_and_maximum_height(boxes, iou_threshold):
    min_height = float('inf')
    max_height = float('-inf')

    for frame_name, list_of_boxes in boxes.items():
        for box in list_of_boxes:
            if getattr(box, 'iou', 0) > iou_threshold:
                height = box.height
                min_height = min(min_height, height)
                max_height = max(max_height, height)

    return min_height, max_height



def create_historgram(boxes, iou_threshold):
    iou_values = []
    # Iterate through each frame and its boxes
    for frame_name, box_list in boxes.items():
        for box in box_list:
            # Check if the box passes the iou_threshold
            if getattr(box, 'iou', 0) > iou_threshold:
                iou_values.append(box.iou)

    # Output the IOU values histogram
    plt.hist(iou_values, bins=10, edgecolor='black')
    plt.xlabel('IOU Values')
    plt.ylabel('Occurrences')
    plt.title(f'IOU Values Histogram (Threshold: {iou_threshold})')
    plt.show()


def calculate_average_iou(boxes, iou):
    sum_iou = 0
    count = 0

    # Iterate through each frame and its boxes
    for frame_name, box_list in boxes.items():
        for box in box_list:
            # Check if the box passes the iou_threshold
            if getattr(box, 'iou', 0) > iou:
                sum_iou += box.iou
                count += 1

    # Calculate average IOU
    average_iou = sum_iou / count if count > 0 else 0
    return average_iou


def calculate_iou_for_2_boxes(box1, box2):
    # Calculate intersection coordinates
    x_left = max(box1.x_center - box1.width / 2, box2.x_center - box2.width / 2)
    y_top = max(box1.y_center - box1.height / 2, box2.y_center - box2.height / 2)
    x_right = min(box1.x_center + box1.width / 2, box2.x_center + box2.width / 2)
    y_bottom = min(box1.y_center + box1.height / 2, box2.y_center + box2.height / 2)

    # Calculate intersection area
    intersection_area = max(0, x_right - x_left) * max(0, y_bottom - y_top)

    # Calculate union area
    box1_area = box1.width * box1.height
    box2_area = box2.width * box2.height
    union_area = box1_area + box2_area - intersection_area

    # Calculate IoU
    iou = intersection_area / union_area if union_area > 0 else 0

    return iou


if __name__ == '__main__':
    path_detection_boxes_json = "Q1_system_output.json"
    path_groundtruth_boxes_json = "Q1_gt.json"
    iou_threshold = 0.5

    detection_boxes = read_lean_map_of_bboxes(path_detection_boxes_json)
    ground_truth_boxes = read_lean_map_of_bboxes(path_groundtruth_boxes_json)

    for name, detection_bounding_box_list in detection_boxes.items():
        ground_truth_bounding_box_list = ground_truth_boxes[name]
        for det_box in detection_bounding_box_list:
            for gt_bbox in ground_truth_bounding_box_list:
                iou = calculate_iou_for_2_boxes(det_box, gt_bbox)
                # saving the highest iou for a detection bounding box
                if iou > getattr(det_box, 'iou', 0):
                    det_box.iou = iou

    # calculate average iou for the boxes that pass > iou_threshold
    average_iou = calculate_average_iou(detection_boxes, iou_threshold)
    print(f"The average_iou is: {average_iou}")

    # create histogram for the boxes that pass iou_threshold.
    # x_axis: iou, y_axis: occurrences
    create_historgram(detection_boxes, iou_threshold)

    # find the minimum and the maximum height for the boxes that pass > iou_threshold
    min_height, max_height = get_minimum_and_maximum_height(detection_boxes, iou_threshold)
    print(f"The min_height is: {min_height} and the max_height is: {max_height}")



