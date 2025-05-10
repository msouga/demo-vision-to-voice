

import os
import requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    image_url = req.params.get('image_url')
    if not image_url:
        try:
            req_body = req.get_json()
            image_url = req_body.get('image_url')
        except:
            pass

    if not image_url:
        return func.HttpResponse(
            "Falta el parámetro 'image_url'.",
            status_code=400
        )

    endpoint = os.environ["VISION_ENDPOINT"]
    key = os.environ["VISION_KEY"]

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json"
    }

    body = { "url": image_url }

    response = requests.post(
        f"{endpoint}/vision/v3.2/ocr?language=unk&detectOrientation=true",
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        return func.HttpResponse(
            f"Error en Computer Vision: {response.status_code} - {response.text}",
            status_code=response.status_code
        )

    result = response.json()
    lines = []

    for region in result.get("regions", []):
        for line in region.get("lines", []):
            text_line = " ".join([word["text"] for word in line.get("words", [])])
            lines.append(text_line)

    if not lines:
        return func.HttpResponse("No se encontró texto en la imagen.", status_code=200)

    extracted_text = "\n".join(lines)

    return func.HttpResponse(extracted_text, mimetype="text/plain")