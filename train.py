from ultralytics import YOLO


if __name__ == '__main__':
    model = YOLO("yolov8m.pt")
    model.train(
        data="dataset/manga.yaml",
        epochs=100,
        imgsz=640,
        device="cpu"
    )
