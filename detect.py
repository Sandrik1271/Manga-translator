from ultralytics import YOLO
import numpy

def detect(image_path, model, confidence_treshold=0.4):
    results = model(image_path)
    boxes =  results[0].boxes
    
    
    if boxes is None or len(boxes) == 0:
        return []
    
    xyxy = boxes.xyxy.cpu().numpy()
    confidence = boxes.conf.cpu().numpy()
    classes = boxes.cls.cpu().numpy()
    
    mask = confidence > confidence_treshold
    
    filtered_boxes = xyxy[mask].astype(int).tolist()
    filtered_confidence = confidence[mask].tolist()
    filtered_classes = classes[mask].astype(int).tolist()
    
    total_boxes = [
        {"box": box, "conf": conf, "class": cls}
        for box, conf, cls  in zip(filtered_boxes, filtered_confidence, filtered_classes)
    ]
 
    return total_boxes 