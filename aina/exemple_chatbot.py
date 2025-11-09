#!/usr/bin/env python3
"""
Exemple de Chatbot Bàsic amb Salamandra-7B
UAB THE HACK! 2025
Barcelona Supercomputing Center (BSC)

Aquest és un exemple simple per començar. Modifica'l per crear el teu propi projecte!
"""

import requests
import sys
import os

# Fix encoding per Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# =============================================================================
# CONFIGURACIÓ - Modifica aquests valors
# =============================================================================

API_KEY = "zpka_5e913d5ac22249c18c6ee3fcb5316c23_14c83edf"  # Substitueix amb la teva API key
API_URL = "https://api.publicai.co/v1/chat/completions"

# Tria el model que vols utilitzar
# Opció 1: Salamandra-7B (ràpid, recomanat per començar)
MODEL = "BSC-LT/salamandra-7b-instruct-tools-16k"

# Opció 2: ALIA-40B (més lent però més avançat)
# MODEL = "BSC-LT/ALIA-40b-instruct_Q8_0"

# Personalitza el comportament del chatbot
SYSTEM_PROMPT = "Ets un assistent amigable i útil en català. Ajudes estudiants de la UAB durant un hackathon."

# =============================================================================
# FUNCIONS
# =============================================================================

def preguntar(missatge, conversacio=None, temperatura=0.7, max_tokens=500):
    """
    Envia un missatge al model Aina i retorna la resposta.

    Args:
        missatge (str): La pregunta o missatge de l'usuari
        conversacio (list): Historial de la conversa (opcional)
        temperatura (float): Creativitat de la resposta (0.0-2.0)
        max_tokens (int): Longitud màxima de la resposta

    Returns:
        str: La resposta del model
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "UAB-THE-HACK/1.0"
    }

    # Construir l'historial de missatges
    if conversacio is None:
        missatges = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": missatge}
        ]
    else:
        missatges = conversacio + [{"role": "user", "content": missatge}]

    payload = {
        "model": MODEL,
        "messages": missatges,
        "max_tokens": max_tokens,
        "temperature": temperatura
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        elif response.status_code == 401:
            return "❌ Error: API key invàlida. Verifica la teva configuració."
        elif response.status_code == 429:
            return "⚠️ Massa peticions. Espera uns segons i torna a intentar-ho."
        else:
            return f"❌ Error {response.status_code}: {response.text[:100]}"

    except requests.exceptions.Timeout:
        return "⏱️ Timeout: El model està trigant massa. Torna a intentar-ho."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def chatbot_interactiu():
    """
    Executa un chatbot interactiu per la consola.
    """
    print("=" * 70)
    print("🤖 CHATBOT AINA - UAB THE HACK! 2025")
    print("=" * 70)
    print(f"📋 Model: {MODEL.split('/')[-1]}")
    print(f"🧠 Comportament: {SYSTEM_PROMPT[:50]}...")
    print("=" * 70)
    print("\n💡 Consells:")
    print("   - Escriu 'sortir' per acabar")
    print("   - Escriu 'reset' per començar una conversa nova")
    print("   - Escriu 'model' per canviar de model")
    print("\n🚀 Comença a conversar!\n")

    conversacio = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            # Llegir input de l'usuari
            user_input = input("🧑 Tu: ")

            # Comandes especials
            if user_input.lower() in ['sortir', 'exit', 'quit']:
                print("\n👋 Adéu! Gràcies per utilitzar el chatbot Aina!")
                break

            if user_input.lower() == 'reset':
                conversacio = [{"role": "system", "content": SYSTEM_PROMPT}]
                print("\n🔄 Conversa reiniciada!\n")
                continue

            if user_input.lower() == 'model':
                print("\n📋 Models disponibles:")
                print("   1. Salamandra-7B (ràpid)")
                print("   2. ALIA-40B (avançat)")
                opcio = input("Tria model (1 o 2): ")
                if opcio == "1":
                    globals()['MODEL'] = "BSC-LT/salamandra-7b-instruct-tools-16k"
                    print("✅ Model canviat a Salamandra-7B")
                elif opcio == "2":
                    globals()['MODEL'] = "BSC-LT/ALIA-40b-instruct_Q8_0"
                    print("✅ Model canviat a ALIA-40B")
                print()
                continue

            if not user_input.strip():
                continue

            # Enviar missatge i obtenir resposta
            print("🤖 Pensant...", end="\r")
            conversacio.append({"role": "user", "content": user_input})

            resposta = preguntar(user_input, conversacio)

            conversacio.append({"role": "assistant", "content": resposta})

            print(f"🤖 Bot: {resposta}\n")

        except KeyboardInterrupt:
            print("\n\n👋 Adéu! Fins aviat!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperat: {e}")
            print("Torna a intentar-ho o demana ajuda als mentors.\n")


def exemple_simple():
    """
    Exemple simple d'una sola pregunta (sense conversa).
    """
    print("🧪 Provant una pregunta simple...\n")

    resposta = preguntar("Què és la intel·ligència artificial?")

    print(f"Pregunta: Què és la intel·ligència artificial?")
    print(f"Resposta: {resposta}\n")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Verificar que la API key està configurada
    if API_KEY == "la_teva_api_key":
        print("⚠️  ATENCIÓ: No has configurat la teva API key!")
        print("\nOpcions:")
        print("1. Modifica aquest fitxer i canvia API_KEY per la teva clau")
        print("2. Executa setup_aina.py per configurar-ho automàticament")
        print("\nSi no tens API key, demana-la als mentors del BSC.\n")
        sys.exit(1)

    # Menú principal
    print("\n" + "=" * 70)
    print("EXEMPLES DE CHATBOT - PROJECTE AINA")
    print("=" * 70)
    print("\nTria una opció:")
    print("   1. Chatbot interactiu (recomanat)")
    print("   2. Exemple simple (una pregunta)")
    print("   3. Sortir")

    try:
        opcio = input("\nOpció (1-3): ").strip()

        if opcio == "1":
            chatbot_interactiu()
        elif opcio == "2":
            exemple_simple()
        elif opcio == "3":
            print("Adéu!")
        else:
            print("Opció no vàlida")

    except KeyboardInterrupt:
        print("\n\nAdéu!")


# =============================================================================
# REPTES PER MILLORAR AQUEST CODI (Ideas per al vostre projecte!)
# =============================================================================
"""
🎯 Nivell Bàsic:
- Afegir colors al text (usa la llibreria 'colorama')
- Guardar la conversa en un fitxer de text
- Afegir un comptador de missatges

🎯 Nivell Intermedi:
- Crear una interfície web amb Flask o Streamlit
- Afegir detecció d'idioma automàtica
- Implementar diferents "personalitats" del bot

🎯 Nivell Avançat:
- Integrar amb Telegram/Discord bot
- Afegir memòria a llarg termini (base de dades)
- Implementar function calling per executar accions
- Crear un assistent de codi amb syntax highlighting
"""
