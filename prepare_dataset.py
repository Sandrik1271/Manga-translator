import os, shutil, random
from pathlib import Path

EXPORT_DIR  = "C:/Users/sandrik/Desktop/MangaNLP/project-3-at-2026-03-29-11-07-3e75ac4a"
DATASET_DIR = "C:/Users/sandrik/Desktop/MangaNLP/dataset"
VAL_SPLIT   = 0.2         
RANDOM_SEED = 42

random.seed(RANDOM_SEED)

# Читаем все изображения
images = sorted(Path(EXPORT_DIR, "images").glob("*.*"))
print(f"Найдено изображений: {len(images)}")

# Перемешиваем и делим
random.shuffle(images)
split      = int(len(images) * (1 - VAL_SPLIT))
train_imgs = images[:split]
val_imgs   = images[split:]

# Создаём папки
for s in ["train", "val"]:
    for sub in ["images", "labels"]:
        Path(DATASET_DIR, s, sub).mkdir(parents=True, exist_ok=True)

# Копируем файлы
def copy_pair(img_path, split_name):
    label_path = Path(EXPORT_DIR, "labels", img_path.stem + ".txt")
    shutil.copy(img_path, Path(DATASET_DIR, split_name, "images", img_path.name))
    if label_path.exists():
        shutil.copy(label_path, Path(DATASET_DIR, split_name, "labels", label_path.name))
    else:
        Path(DATASET_DIR, split_name, "labels", img_path.stem + ".txt").touch()

for img in train_imgs:
    copy_pair(img, "train")
for img in val_imgs:
    copy_pair(img, "val")

# Читаем классы
classes = Path(EXPORT_DIR, "classes.txt").read_text().strip().splitlines()

# Создаём manga.yaml
yaml = f"""path: {Path(DATASET_DIR).resolve()}
train: train/images
val:   val/images

nc: {len(classes)}
names: {classes}
"""
Path(DATASET_DIR, "manga.yaml").write_text(yaml)

print(f"Готово!")
print(f"  Train: {len(train_imgs)} изображений")
print(f"  Val:   {len(val_imgs)} изображений")
print(f"  Классы: {classes}")
print(f"  Конфиг: {DATASET_DIR}/manga.yaml")