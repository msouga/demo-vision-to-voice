import os
import requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        text_to_translate = req_body.get("text")
    except:
        return func.HttpResponse("Falta el cuerpo JSON con 'text'.", status_code=400)

    if not text_to_translate:
        return func.HttpResponse("El texto a traducir está vacío.", status_code=400)

    openai_endpoint = os.environ["OPENAI_ENDPOINT"]
    api_key = os.environ["OPENAI_API_KEY"]
    deployment = os.environ["OPENAI_DEPLOYMENT_NAME"]
    api_version = os.environ["OPENAI_API_VERSION"]

    url = f"{openai_endpoint}openai/deployments/{deployment}/chat/completions?api-version={api_version}"

    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    data = {
        "messages": [
            {"role": "system", "content": "Eres un traductor profesional. Traduce al español respetando el estilo y contexto del mensaje. Si hay juegos de palabras o referencias culturales, explícalas brevemente."},
            {"role": "user", "content": text_to_translate}
        ],
        "temperature": 0.7,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        return func.HttpResponse(
            f"Error de OpenAI: {response.status_code} - {response.text}",
            status_code=response.status_code
        )

    result = response.json()
    translated_text = result["choices"][0]["message"]["content"]

    return func.HttpResponse(translated_text, mimetype="text/plain")