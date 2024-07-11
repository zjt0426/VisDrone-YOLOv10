import os
from pathlib import Path
from PIL import Image
import glob



def convert_yolo_to_visdrone(size, box):
    dw, dh = size
    x_center, y_center, w, h = box
    left = (x_center - w / 2) * dw
    top = (y_center - h / 2) * dh
    width = w * dw
    height = h * dh
    return round(left), round(top), round(width), round(height)


def yolo2visdrone(yolo_dir, visdrone_dir, image_dir, count):
    os.makedirs(visdrone_dir, exist_ok=True)  # Create output directory if it doesn't exist

    for txt_file in glob.glob(f'{yolo_dir}/*.txt'):
        visdrone_lines = []
        try:
            with open(txt_file, 'r') as f:
                lines = f.readlines()
        except IOError:
            print(f"Error opening txt file {txt_file}. Skipping.")
            continue

        # Get the image size
        image_path = os.path.join(image_dir, os.path.basename(txt_file).replace('.txt', '.jpg'))
        if not os.path.exists(image_path):
            print(f"Image file {image_path} not found. Skipping.")
            continue

        try:
            with Image.open(image_path) as img:
                img_width, img_height = img.size
        except IOError:
            print(f"Error opening image {image_path}. Skipping.")
            continue

        if not lines:
            print(f"{txt_file} is empty. Creating corresponding empty VisDrone txt file.")
            count += 1
            visdrone_txt_file = os.path.join(visdrone_dir, os.path.basename(txt_file))
            open(visdrone_txt_file, 'w').close()
        else:
            for line in lines:
                parts = line.strip().split()
                if len(parts) != 6:
                    print(f"Invalid line in {txt_file}: {line}. Skipping.")
                    continue

                cls = int(parts[0]) + 1  # class number +1
                x_center, y_center, w, h, confidence = map(float, parts[1:])
                left, top, width, height = convert_yolo_to_visdrone((img_width, img_height), (x_center, y_center, w, h))
                visdrone_lines.append(f"{left},{top},{width},{height},{confidence},{cls},-1,-1\n")

            # Save to VisDrone format
            visdrone_txt_file = os.path.join(visdrone_dir, os.path.basename(txt_file))
            with open(visdrone_txt_file, 'w') as f:
                f.writelines(visdrone_lines)
                print(f"Converted {txt_file} to VisDrone format.")


    print(count)

# Directories
yolo_dir = Path(r'D:\Desktop\yolov10test\vis2yolotest\yolo')  # YOLO格式的检测结果目录
visdrone_dir = Path(r'D:\Desktop\yolov10test\vis2yolotest\visdrone')  # 输出VisDrone格式的结果目录
image_dir = Path(r'D:\Desktop\yolov10test\vis2yolotest\images')  # 图片目录

# Convert
yolo2visdrone(yolo_dir, visdrone_dir, image_dir, 0)
# print(count)