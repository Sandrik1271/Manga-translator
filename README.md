# Manga Translator 🇯🇵➡️🇷🇺

Сервис для автоматического перевода страниц манги с японского на русский язык.

## Демо
![result](result.jpg)

## Как работает
1. **YOLOv8** детектирует текстовые облачки, текст и звуковые эффекты
2. **Manga OCR** распознаёт японский текст внутри регионов
3. **Google Translate** переводит на русский язык
4. **LaMa** удаляет оригинальный текст восстанавливая фон
5. **Pillow** вставляет переведённый текст обратно

## Стек
- YOLOv8 — детекция текстовых регионов (3 класса: bubble, text, sfx)
- Manga OCR — распознавание японского текста
- LaMa — inpainting (восстановление фона)
- Google Translate — перевод
- Streamlit — веб-интерфейс

## Установка
pip install -r requirements.txt

## Запуск
streamlit run app.py

## Веса модели
Скачай best.pt и положи в корень проекта рядом с app.py

[Скачать best.pt](https://huggingface.co/sandrik1271/manga-translator-yolov8/resolve/main/best.pt)

## Структура проекта
- detect.py — детекция bbox через YOLOv8
- ocr.py — распознавание текста через Manga OCR
- translate.py — перевод через Google Translate
- inpaint.py — удаление текста через LaMa
- render.py — вставка переведённого текста
- pipeline.py — склейка всех модулей
- app.py — веб-интерфейс на Streamlit
- train.py — обучение модели
- prepare_dataset.py — подготовка датасета
