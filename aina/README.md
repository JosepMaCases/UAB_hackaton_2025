# 🚀 UAB THE HACK! 2025 - Projecte Aina Starter Kit

Paquet per entendre com fer servir els models d'IA del Projecte AINA del Barcelona Supercomputing Center (BSC)!

## 📦 Contingut del Kit

Aquest kit conté tot el necessari per començar a desenvolupar amb els models Aina:

- **README.md** (aquest fitxer) - Instruccions de inici ràpid
- **setup_aina.py** - Script automàtic de configuració
- **GUIA_RAPIDA_PARTICIPANTES.md** - Documentació completa amb exemples
- **exemple_chatbot.py** - Exemple funcional d'un chatbot bàsic
- **uab-the-hack-recursos-aina.pdf** - Presentació visual del projecte

## ⚡ Inici Ràpid (10 minuts)

### Pas 1: Obtenir la teva API Key de PublicAI

1. **Registra't a PublicAI:** https://platform.publicai.co
2. **Crea un compte** amb el teu email
3. **Genera una API key** des del teu dashboard
4. **Guarda la key** en un lloc segur

**Important:** Els models del BSC (Salamandra i ALIA) estan allotjats a PublicAI. Necessites un compte per accedir-hi.

**Tens problemes?**
- Consulta la documentació: https://platform.publicai.co/docs
- Pregunta als mentors del BSCo consulta via Discord.
- Canal de Discord: #bsc-llms-tool

### Pas 2: Executar el Setup
```bash
python setup_aina.py
```

Aquest script farà automàticament:
- ✅ Instal·lar les dependències necessàries (`requests`)
- ✅ Demanar-te la teva API key de PublicAI
- ✅ Provar la connexió amb els models del BSC
- ✅ Verificar que Salamandra-7B i ALIA-40B funcionen
- ✅ Crear un fitxer d'exemple (`exemple_aina.py`)

### Pas 3: Provar el primer exemple

```bash
python exemple_aina.py
```

## 🧠 Models Disponibles

### 1️⃣ Salamandra-7B ⚡ (Recomanat per començar)
```python
model = "BSC-LT/salamandra-7b-instruct-tools-16k"
```
- **Velocitat:** ~1 segon per resposta
- **Ideal per:** Chatbots, prototips ràpids, generació de codi
- **Llengües:** Català, castellà, i 33 idiomes europeus més

### 2️⃣ ALIA-40B 🧠 (Per casos avançats)
```python
model = "BSC-LT/ALIA-40b-instruct_Q8_0"
```
- **Velocitat:** ~3-6 segons per resposta
- **Ideal per:** Raonament complex, explicacions detallades
- **Llengües:** Català, castellà, i 33 idiomes europeus més

## 💻 Exemple de Codi Mínim

```python
import requests

API_KEY = "la_teva_api_key"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "User-Agent": "UAB-THE-HACK/1.0"
}

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

## 🎯 Ideas de Projectes

### Nivell Bàsic
- Chatbot d'informació sobre la UAB
- Traductor multilingüe (35 idiomes)
- Generador de text creatiu
- Assistent de debugging de codi

### Nivell Intermedi
- Tutor interactiu per aprendre programació
- Analitzador de sentiment en català
- Sistema de FAQ automàtic
- Assistent de correcció gramatical

### Nivell Avançat
- IDE amb IA integrada (autocompletat + explicacions)
- Sistema de recomanacions personalitzat
- Generador de documentació tècnica
- Plataforma de peer-learning amb IA

## 📚 Recursos i Documentació

### Documentació Completa
Consulta **GUIA_RAPIDA_PARTICIPANTES.md** per:
- Exemples pràctics de codi
- Explicació de paràmetres (temperature, max_tokens, etc.)
- Gestió d'errors i retry logic
- Troubleshooting comú
- Consells per optimitzar els prompts

### Links Útils
- **PublicAI Docs:** https://platform.publicai.co/docs
- **Salamandra-7B:** https://huggingface.co/BSC-LT/salamandra-7b-instruct
- **ALIA-40B:** https://huggingface.co/BSC-LT/ALIA-40b
- **Aina Challenge:** https://ainachallenge.cat

## ⚠️ Límits i Bones Pràctiques

### Rate Limits
- Aproximadament **20 peticions/minut** per API key
- Si arribes al límit, espera uns segons i torna a intentar

### Consells
✅ **Fer:**
- Implementar retry logic per errors temporals
- Guardar respostes en cache per preguntes comunes
- Començar amb Salamandra-7B per prototips ràpids
- Experimentar amb diferents prompts

❌ **No fer:**
- Fer moltes peticions simultànies
- Enviar prompts molt llargs sense necessitat
- Compartir la teva API key amb altres equips