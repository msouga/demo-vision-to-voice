import os
import requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    text = req.params.get("text")
    if not text:
        try:
            req_body = req.get_json()
            text = req_body.get("text")
        except:
            return func.HttpResponse("Falta el texto para convertir a voz.", status_code=400)

    if not text:
        return func.HttpResponse("Texto vacío.", status_code=400)

    api_key = os.environ["ELEVENLABS_API_KEY"]
    voice_id = os.environ["ELEVENLABS_VOICE_ID"]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    body = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.9,
            "style": 0.9,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code != 200:
        return func.HttpResponse(
            f"Error de ElevenLabs: {response.status_code} - {response.text}",
            status_code=500
        )

    return func.HttpResponse(
        response.content,
        mimetype="audio/mpeg",
        status_code=200
    )
