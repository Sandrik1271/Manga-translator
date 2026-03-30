from manga_ocr import MangaOcr
from PIL import Image

def ocr(image, box, mocr):
    image_pil = Image.open(image)
    x1, y1, x2, y2 = box["box"]
    crop = image_pil.crop(( x1, y1, x2, y2))
    text = mocr(crop)
    return text
    