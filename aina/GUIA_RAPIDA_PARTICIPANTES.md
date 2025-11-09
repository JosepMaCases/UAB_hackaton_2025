# Guia Ràpida - Models d'IA del BSC per UAB THE HACK! 2025

**📅 8-9 de novembre de 2025**

---

## 🚀 Inici Ràpid (10 minuts)

### Pas 1: Obtenir la teva API Key de PublicAI

Els models del BSC estan disponibles a través de **PublicAI**:

1. **Registra't:** Ves a https://platform.publicai.co
2. **Crea un compte** amb el teu email
3. **Genera una API key** des del teu dashboard
4. **Guarda la key** en un lloc segur

**Documentació completa:** https://platform.publicai.co/docs

### Pas 2: Instal·lar dependències
```bash
pip install requests
```

### Pas 3: Primer codi funcional
```python
import requests

# La teva API key (obtinguda de PublicAI)
API_KEY = "la_teva_api_key_aqui"

# Configuració
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "UAB-THE-HACK/1.0"
}

# Fer una pregunta al model
payload = {
    "model": "BSC-LT/salamandra-7b-instruct-tools-16k",
    "messages": [
        {"role": "user", "content": "Hola! Com puc crear un chatbot?"}
    ],
    "max_tokens": 500,
    "temperature": 0.7
}

response = requests.post(
    "https://api.publicai.co/v1/chat/completions",
    headers=headers,
    json=payload
)

print(response.json()["choices"][0]["message"]["content"])
```

**🎉 Ja està! Ja estàs utilitzant IA del Barcelona Supercomputing Center!**

---

## 🧠 Models Disponibles

### Salamandra-7B ⚡ (Recomanat per començar)
- **Model:** `BSC-LT/salamandra-7b-instruct-tools-16k`
- **Velocitat:** ~1 segon per resposta
- **Millor per:** Chatbots, prototips ràpids, codi senzill
- **Llengües:** Català, Castellà, 33 idiomes europeus més

### ALIA-40B 🧩 (Per casos avançats)
- **Model:** `BSC-LT/ALIA-40b-instruct_Q8_0`
- **Velocitat:** ~3-6 segons per resposta
- **Millor per:** Raonament complex, explicacions detallades
- **Llengües:** Català, Castellà, 33 idiomes europeus més

---

## 💡 Exemples Pràctics

### Exemple 1: Chatbot bàsic en Català
```python
import requests

def preguntar(missatge):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "UAB-THE-HACK/1.0"
    }

    payload = {
        "model": "BSC-LT/salamandra-7b-instruct-tools-16k",
        "messages": [
            {"role": "system", "content": "Ets un assistent útil en català."},
            {"role": "user", "content": missatge}
        ],
        "max_tokens": 300
    }

    response = requests.post(
        "https://api.publicai.co/v1/chat/completions",
        headers=headers,
        json=payload
    )

    return response.json()["choices"][0]["message"]["content"]

# Ús
resposta = preguntar("Com funciona un algoritme de cerca binària?")
print(resposta)
```

### Exemple 2: Generador de codi
```python
def generar_codi(descripcio):
    payload = {
        "model": "BSC-LT/salamandra-7b-instruct-tools-16k",
        "messages": [
            {"role": "system", "content": "Ets un expert en Python."},
            {"role": "user", "content": f"Escriu codi Python per: {descripcio}"}
        ],
        "max_tokens": 500,
        "temperature": 0.5  # Menys creativitat = codi més predictible
    }

    response = requests.post(URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

# Ús
codi = generar_codi("ordenar una llista d'estudiants per nota")
print(codi)
```

### Exemple 3: Conversa multi-torn
```python
conversacio = [
    {"role": "system", "content": "Ets un tutor de programació."}
]

def conversar(missatge):
    conversacio.append({"role": "user", "content": missatge})

    payload = {
        "model": "BSC-LT/salamandra-7b-instruct-tools-16k",
        "messages": conversacio,
        "max_tokens": 400
    }

    response = requests.post(URL, headers=headers, json=payload)
    resposta = response.json()["choices"][0]["message"]["content"]

    conversacio.append({"role": "assistant", "content": resposta})
    return resposta

# Ús
print(conversar("Què és una API?"))
print(conversar("Com puc crear-ne una amb Flask?"))
print(conversar("Dona'm un exemple de codi"))
```

### Exemple 4: Traductor multilingüe
```python
def traduir(text, idioma_origen, idioma_desti):
    prompt = f"Tradueix aquest text de {idioma_origen} a {idioma_desti}: {text}"

    payload = {
        "model": "BSC-LT/salamandra-7b-instruct-tools-16k",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": len(text) * 2  # Aproximació
    }

    response = requests.post(URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

# Ús
text_catala = "Bon dia, com estàs?"
text_angles = traduir(text_catala, "català", "anglès")
print(text_angles)
```

---

## ⚙️ Paràmetres Importants

### `temperature` (0.0 - 2.0)
- **0.0-0.3**: Respostes deterministes i precises (ideal per codi)
- **0.7-0.9**: Equilibri entre creativitat i coherència (per defecte)
- **1.0-2.0**: Molt creatiu però menys predictible

### `max_tokens`
- Límit de tokens generats
- **50-100**: Respostes curtes
- **300-500**: Respostes mitjanes (recomanat)
- **800-1000**: Respostes llargues

### `top_p` (0.0 - 1.0)
- **0.9**: Bona varietat (recomanat)
- **0.5**: Més conservador
---

## ⚠️ Límits i Bones Pràctiques

### Rate Limits
- **~20 peticions/minut** per API key
- Si arribes al límit, espera uns segons i torna a intentar-ho

### Consells
✅ **Fer:**
- Implementar retry logic (tornar a intentar si falla)
- Guardar respostes en cache per preguntes comunes
- Usar Salamandra-7B per prototips
- Provar amb prompts diferents per optimitzar resultats

❌ **No fer:**
- Fer moltes peticions simultànies
- Enviar prompts molt llargs sense necessitat
- Confiar 100% en les respostes sense validar-les
- Compartir la teva API key

### Gestió d'Errors
```python
import time

def preguntar_amb_retry(missatge, max_intents=3):
    for intent in range(max_intents):
        try:
            response = requests.post(URL, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            elif response.status_code == 429:  # Rate limit
                print(f"Rate limit. Esperant {2**intent} segons...")
                time.sleep(2 ** intent)
            else:
                print(f"Error {response.status_code}")
                return None

        except Exception as e:
            print(f"Error: {e}")
            if intent < max_intents - 1:
                time.sleep(1)

    return "Error: S'han esgotat els intents"
```

---

## 🔧 Troubleshooting

### Error 400: "Invalid model name"
```python
# ❌ Incorrecte
"model": "salamandra"

# ✅ Correcte
"model": "BSC-LT/salamandra-7b-instruct-tools-16k"
```

### Error 401: "Unauthorized"
Verifica que la teva API key és correcta i l'has creat des de la secció correcte:
```python
print(f"API Key: {API_KEY[:10]}...")  # Només mostra els primers caràcters
```

### Resposta buida o molt curta
Augmenta `max_tokens`:
```python
"max_tokens": 800  # En lloc de 100
```

### Timeout
Augmenta el timeout per ALIA-40B:
```python
response = requests.post(URL, headers=headers, json=payload, timeout=60)
```
---

## 📚 Recursos Addicionals

### Documentació
- **PublicAI**: https://platform.publicai.co/docs
- **Salamandra**: https://huggingface.co/BSC-LT/salamandra-7b-instruct
- **ALIA**: https://huggingface.co/BSC-LT/ALIA-40b

### Durant el Hackathon
- **Slack/Discord del hackathon**: Canal #ajuda-ia
- **Mentors BSC**: Disponibles per consultes
- **Documentació offline**: Disponible al repositori local

---

## 🎮 Exemple Complet: Mini Chatbot

```python
#!/usr/bin/env python3
"""
Mini Chatbot per UAB THE HACK! 2025
Usant Salamandra-7B del BSC
"""

import requests
import sys

API_KEY = "la_teva_api_key"
URL = "https://api.publicai.co/v1/chat/completions"

conversacio = [
    {"role": "system", "content": "Ets un assistent amigable en català."}
]

def enviar_missatge(text):
    conversacio.append({"role": "user", "content": text})

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "UAB-THE-HACK/1.0"
    }

    payload = {
        "model": "BSC-LT/salamandra-7b-instruct-tools-16k",
        "messages": conversacio,
        "max_tokens": 400,
        "temperature": 0.7
    }

    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            resposta = response.json()["choices"][0]["message"]["content"]
            conversacio.append({"role": "assistant", "content": resposta})
            return resposta
        else:
            return f"Error {response.status_code}: {response.text}"

    except Exception as e:
        return f"Error: {str(e)}"

def main():
    print("=" * 50)
    print("🤖 CHATBOT UAB THE HACK! 2025")
    print("🧠 Model: Salamandra-7B (BSC)")
    print("=" * 50)
    print("Escriu 'sortir' per acabar\n")

    while True:
        try:
            user_input = input("Tu: ")

            if user_input.lower() in ['sortir', 'exit', 'quit']:
                print("Adéu! 👋")
                break

            if not user_input.strip():
                continue

            print("🤖 Pensant...", end="\r")
            resposta = enviar_missatge(user_input)
            print(f"Bot: {resposta}\n")

        except KeyboardInterrupt:
            print("\n\nAdéu! 👋")
            break

if __name__ == "__main__":
    main()
```

**Per executar:**
```bash
python chatbot.py
```