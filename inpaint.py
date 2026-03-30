from simple_lama_inpainting import SimpleLama
from PIL import Image, ImageDraw

def inpaint(image, detections , lama):
    image_pil = Image.open(image)
    
    w, h = image_pil.size
    
    mask = Image.new("L", (w,h),0)
    
    draw = ImageDraw.Draw(mask)
    
    merge = 0
    for detection in detections:
        
        box = detection["box"]
        x1, y1, x2, y2 = box
        if (x1 + merge) < (x2 - merge) and (y1 + merge) < (y2 - merge):
            draw.rectangle([x1 + merge, y1 + merge, x2 - merge, y2 - merge], fill=255)
        else:
            draw.rectangle([x1, y1, x2, y2], fill=255)
    result = lama(image_pil, mask)
    return result
    
    
    
    
    
    
    

    
    
    