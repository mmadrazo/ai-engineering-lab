import certifi

from openai import OpenAI
from app.config import settings
from app.context.examples import ESTIMATION_EXAMPLES

def build_system_prompt(examples: str) -> str:
    return f"""
Eres un estimador de software experto.

Tu tarea es analizar la transcripción de una reunión con un cliente o equipo de producto y generar una estimación de software clara, razonada y útil.

Debes basarte en los ejemplos previos de estimaciones incluidos a continuación para mantener el mismo estilo, nivel de detalle y estructura.

Ejemplos previos:
{examples}

Genera una estimación bien estructurada a partir de la nueva transcripción que recibirás del usuario.
"""


def generate_estimate(transcript: str) -> str:
    #import certifi
    #import ssl

    #print("CERTIFI:", certifi.where())
    #print("SSL:", ssl.get_default_verify_paths())
    #import truststore

    #print("TRUSTSTORE LOADED")

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    system_prompt = build_system_prompt(ESTIMATION_EXAMPLES)

    response = client.responses.create(
        model=settings.LLM_MODEL,
        input=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": transcript,
            },
        ],
    )

    return response.output_text