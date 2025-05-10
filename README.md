# Demo: De la Imagen a la Voz con IA en Azure

Este repositorio contiene el código de la demo presentada en el **Azure Global Event – Lima**, el día **10 de mayo de 2025**.

## 🎯 Objetivo

Mostrar cómo una imagen puede ser transformada en una voz humana utilizando inteligencia artificial, sin necesidad de escribir código manualmente durante la ejecución. Todo fue orquestado desde un entorno ligero con VS Code y desplegado en Azure.

## 🧠 ¿Qué tecnologías usamos?

- **Azure Functions (Python)** – Orquestación serverless
- **Azure Computer Vision** – Detección de texto en imágenes
- **Azure OpenAI (GPT-4o)** – Traducción con contexto y estilo
- **ElevenLabs** – Generación de voz natural
- **VS Code + Azure CLI (macOS)** – Entorno de desarrollo

## 📂 Estructura del proyecto

- `/ocr` – Extrae texto de una imagen
- `/translate` – Traduce el texto con contexto
- `/speak` – Convierte el texto en audio
- `/fullchain` – Orquesta todo el flujo: Imagen → Texto → Traducción → Voz

> Todas las funciones fueron creadas y desplegadas en vivo durante la charla. El código fuente de cada una fue generado asistido por IA.

## ⚠️ Importante

Las claves de API y endpoints han sido removidos del archivo `local.settings.json`.  
Cada campo contiene una descripción para que puedas completar tu propia configuración con servicios activos en tu suscripción de Azure y ElevenLabs.

## 🧪 Prueba en local

1. Clona el repositorio
2. Llena `local.settings.json` con tus claves
3. Ejecuta `func start`
4. Usa `curl` para llamar a `fullchain`:

```bash
curl "http://localhost:7071/api/fullchain?image_url=https://i.imgur.com/Pv3nFlH.jpeg" --output demo.mp3
open demo.mp3
```

## ✨ Autor

Demo presentada por **Mauricio Sougarret**  
[linkedin.com/in/msouga](https://linkedin.com/in/msouga)