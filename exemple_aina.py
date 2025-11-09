#!/usr/bin/env python3
"""
Exemple d'ús dels models Projecte Aina
UAB THE HACK! 2025
"""

import requests

# Configuració
API_KEY = "zpka_5e913d5ac22249c18c6ee3fcb5316c23_14c83edf"
API_URL = "https://api.publicai.co/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "UAB-THE-HACK/1.0"
}

def preguntar(missatge, model="salamandra"):
    """
    Fa una pregunta al model Aina

    Args:
        missatge: La teva pregunta o instrucció
        model: "salamandra" (ràpid) o "alia" (avançat)
    """

    # Seleccionar model
    if model == "alia":
        model_id = "BSC-LT/ALIA-40b-instruct_Q8_0"
    else:
        model_id = "BSC-LT/salamandra-7b-instruct-tools-16k"

    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": "Ets un assistent útil en català."},
            {"role": "user", "content": missatge}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"Error: {str(e)}"


# Exemples d'ús
if __name__ == "__main__":
    print("=" * 60)
    print("EXEMPLE 1: Pregunta simple amb Salamandra-7B")
    print("=" * 60)

    resposta = preguntar("Què és la intel·ligència artificial?", model="salamandra")
    print(resposta)

    print("\n" + "=" * 60)
    print("EXEMPLE 2: Generació de codi")
    print("=" * 60)

    resposta = preguntar("Escriu una funció Python per calcular el factorial", model="salamandra")
    print(resposta)

    print("\n" + "=" * 60)
    print("EXEMPLE 3: Raonament complex amb ALIA-40B")
    print("=" * 60)

    resposta = preguntar("Explica la diferència entre algoritmes greedy i programació dinàmica", model="alia")
    print(resposta)

    print("\n" + "=" * 60)
    print("Ara és el teu torn! Modifica aquest codi i crea alguna cosa genial!")
    print("=" * 60)
