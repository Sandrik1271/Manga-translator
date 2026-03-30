from PIL import Image, ImageDraw, ImageFont

def render(image, detections, texts):
    draw = ImageDraw.Draw(image)
    font_path = "Roboto/Roboto-VariableFont_wdth,wght.ttf"

    for detection, text in zip(detections, texts):
        x1, y1, x2, y2 = detection["box"]
        region = image.crop((x1, y1, x2, y2))
        avg_brightness = sum(region.convert("L").getdata()) / (region.width * region.height)
        text_color = "white" if avg_brightness < 128 else "black"
        box_width = x2 - x1
        box_height = y2 - y1

        font_size = 20

        while font_size > 6:
            font = ImageFont.truetype(font_path, font_size)

            lines = []
            for line in text.split("\n"):
                words = line.split()
                current_line = ""

                for word in words:
                    test_line = current_line + (" " if current_line else "") + word
                    bbox = draw.textbbox((0, 0), test_line, font=font)
                    text_width = bbox[2] - bbox[0]

                    if text_width <= box_width:
                        current_line = test_line
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word

                if current_line:
                    lines.append(current_line)


            line_heights = []
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                line_heights.append(bbox[3] - bbox[1])

            total_text_height = sum(line_heights)

            max_width = max(
                draw.textbbox((0, 0), line, font=font)[2]
                for line in lines
            )

            if max_width <= box_width and total_text_height <= box_height:
                break

            font_size -= 1


        y_text = y1 + (box_height - total_text_height) // 2

        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            x_text = x1 + (box_width - text_width) // 2

            draw.text((x_text, y_text), line, fill=text_color, font=font)

            y_text += text_height

    return image