import os
import requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    image_url = req.params.get("image_url")
    if not image_url:
        return func.HttpResponse("Falta 'image_url'", status_code=400)

    base_url = "http://localhost:7071/api"

    # Paso 1: OCR
    ocr_response = requests.get(f"{base_url}/ocr", params={"image_url": image_url})
    if ocr_response.status_code != 200:
        return func.HttpResponse(f"OCR error: {ocr_response.text}", status_code=500)
    extracted_text = ocr_response.text.strip()

    # Paso 2: Translate
    translate_response = requests.post(f"{base_url}/translate", json={"text": extracted_text})
    if translate_response.status_code != 200:
        return func.HttpResponse(f"Translate error: {translate_response.text}", status_code=500)
    translated_text = translate_response.text.strip()

    # Paso 3: Speak
    speak_response = requests.get(f"{base_url}/speak", params={"text": translated_text})
    if speak_response.status_code != 200:
        return func.HttpResponse(f"Speak error: {speak_response.text}", status_code=500)

    return func.HttpResponse(speak_response.content, mimetype="audio/mpeg")