from ultralytics import YOLO

# Load a model
#model = YOLO('yolov10z.pt')  # load a pretrained model (recommended for training)
model = YOLO(model='yolov10z.yaml')


results = model.train(data='VisDrone.yaml', epochs=30, imgsz=640, device='cpu', workers=0,batch=2,amp=False)
