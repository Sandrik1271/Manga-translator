from PIL import Image
from detect import detect
from inpaint import inpaint
from ocr import ocr
from translate import translate
from render import render
from ultralytics import YOLO
from manga_ocr import MangaOcr
from simple_lama_inpainting import SimpleLama
from deep_translator import GoogleTranslator
from deep_translator import GoogleTranslator



trans = GoogleTranslator(source="ja", target="ru")
model = YOLO("best.pt")
mocr = MangaOcr()
lama = SimpleLama()

def find_bubble(text_det, bubbles):
    tx1, ty1, tx2, ty2 = text_det["box"]
    for bubble in bubbles:
        bx1, by1, bx2, by2 = bubble["box"]
        if bx1 < tx1 and by1 < ty1 and bx2 > tx2 and by2 > ty2:
            return bubble
    return None

def process_image(image_path, model, mocr, lama, trans):
    
    detections = detect(image_path, model)
    bubbles = [d for d in detections if d["class"] == 0]
    texts   = [d for d in detections if d["class"] == 2]
    sfx     = [d for d in detections if d["class"] == 1]
    
    text_sfx = texts + sfx
    
    cleaned = inpaint(image_path, text_sfx, lama)
    
    raw_texts  = []
    for det in text_sfx:
        text = ocr(image_path, det, mocr)
        raw_texts .append(text)
    
    
    translated = translate(raw_texts, trans)
    text_ru = translated
    
    for det, translation in zip(text_sfx, text_ru):
        if det["class"] == 2:  # text
            bubble = find_bubble(det, bubbles)
            if bubble:
                cleaned = render(cleaned, [bubble], [translation])
            else:
                cleaned = render(cleaned, [det], [translation])
        elif det["class"] == 1:  # sfx
            cleaned = render(cleaned, [det], [translation])
            
    return cleaned

if __name__ == "__main__":
    result = process_image("dataset/train/images/c46004cb-006.jpg", model, mocr, lama, trans)
    result.save("result.png")
