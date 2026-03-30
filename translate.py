
from deep_translator import GoogleTranslator

def translate(texts, trans):
    if len(texts) == 0:
        return []
    results = trans.translate_batch(texts)
    return results