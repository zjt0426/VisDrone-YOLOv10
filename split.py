import os
import shutil
import random

random.seed(0)  # 确保随机操作的可复现性


def split_data(file_path, xml_path, new_file_path, train_rate, val_rate, test_rate):
    # 存储图片和标注文件的列表
    each_class_image = []
    each_class_label = []

    # 将图片文件名添加到列表
    for image in os.listdir(file_path):
        each_class_image.append(image)

    # 将标注文件名添加到列表
    for label in os.listdir(xml_path):
        each_class_label.append(label)

    # 将图片和标注文件打包成元组列表并随机打乱
    data = list(zip(each_class_image, each_class_label))
    total = len(each_class_image)
    random.shuffle(data)

    # 解压元组列表，回到图片和标注文件列表
    each_class_image, each_class_label = zip(*data)

    # 按照指定的比例分配数据到训练集、验证集和测试集
    train_images = each_class_image[0:int(train_rate * total)]
    val_images = each_class_image[int(train_rate * total):int((train_rate + val_rate) * total)]
    test_images = each_class_image[int((train_rate + val_rate) * total):]

    train_labels = each_class_label[0:int(train_rate * total)]
    val_labels = each_class_label[int(train_rate * total):int((train_rate + val_rate) * total)]
    test_labels = each_class_label[int((train_rate + val_rate) * total):]

    # 定义复制文件到新路径的操作
    def copy_files(files, old_path, new_path1):
        # 遍历列表中的每一个文件名
        for file in files:
            # 打印当前处理的文件名，这只是为了在处理过程中输出信息，便于跟踪进度
            print(file)
            # 使用os.path.join连接旧路径和新文件名，形成完整的旧文件路径
            old_file_path = os.path.join(old_path, file)
            # 检查新的路径是否存在，如果不存在则创建新的路径，这可以确保复制操作不会因为路径不存在而出错
            if not os.path.exists(new_path1):
                os.makedirs(new_path1)
            # 使用os.path.join连接新路径和新文件名，形成完整的新文件路径
            new_file_path = os.path.join(new_path1, file)
            # 使用shutil模块的copy函数复制旧文件到新路径，生成与旧文件相同的新的文件
            shutil.copy(old_file_path, new_file_path)

    # 复制训练、验证和测试的图片和标注文件到指定目录
    copy_files(train_images, file_path, os.path.join(new_file_path, 'train', 'images'))
    copy_files(train_labels, xml_path, os.path.join(new_file_path, 'train', 'labels'))
    copy_files(val_images, file_path, os.path.join(new_file_path, 'val', 'images'))
    copy_files(val_labels, xml_path, os.path.join(new_file_path, 'val', 'labels'))
    copy_files(test_images, file_path, os.path.join(new_file_path, 'test', 'images'))
    copy_files(test_labels, xml_path, os.path.join(new_file_path, 'test', 'labels'))


# 判断当前脚本是否为主程序入口，即直接运行该脚本
if __name__ == '__main__':
    # 定义文件路径变量，指向数据集的图像文件所在路径
    file_path = r"D:\Desktop\imgdata\voc_yolo\JPEGImages"
    # 定义xml路径变量，指向数据集的标注文件所在路径
    xml_path = r"D:\Desktop\imgdata\voc_yolo\Annotations"
    # 定义新文件路径变量，指向输出结果文件的新路径
    new_file_path = r"D:\Desktop\yolov10test\ImageSets"
    # 调用split_data函数，分割数据集，并将结果分别存储到指定的路径中
    split_data(file_path, xml_path, new_file_path, train_rate=0.7, val_rate=0.1, test_rate=0.2)
