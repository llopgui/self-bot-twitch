# 🤖 Self Bot Twitch - Bot Antiplutoniano

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Twitch](https://img.shields.io/badge/Platform-Twitch-purple.svg)](https://www.twitch.tv/)
[![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Bot automático para Twitch que envía chistes malos sobre Plutón y responde con factos científicos cuando alguien menciona que Plutón es un planeta. **¡Porque la ciencia importa!** 🚀

## 🌟 Características

### 🎭 **Chistes Automáticos**

- 📅 Envía chistes malos sobre Plutón cada X segundos (configurable)
- 😂 10 chistes únicos y divertidos
- ⏱️ Intervalo mínimo de 30 segundos entre chistes

### 🧠 **Detector Anti-Plutón Inteligente**

- 🔍 Detecta automáticamente menciones de "Plutón", "pluto", "planeta plutón", etc.
- 📚 Responde inmediatamente con factos científicos educativos
- 🎯 12 factos diferentes sobre por qué Plutón NO es un planeta

### 🛠️ **Características Técnicas**

- 🔄 **Completamente automático** - NO tiene comandos, solo respuestas automáticas
- 🤖 **Filtrado inteligente de bots** - Ignora automáticamente otros bots comunes (StreamElements, Streamlabs, Nightbot, etc.)
- 📝 Sistema de logging robusto con soporte UTF-8
- 🌐 Configuración simple mediante archivo `.env`
- 🐛 Manejo de errores y reconexión automática
- 🪟 Compatible con Windows, Linux y macOS

## 🚀 Instalación Rápida

### 1️⃣ **Prerrequisitos**

- Python 3.11 o superior
- Cuenta de Twitch (para el bot)
- Token OAuth de Twitch

### 2️⃣ **Clonar el Repositorio**

```bash
git clone https://github.com/llopgui/self-bot-twitch.git
cd self-bot-twitch
```

### 3️⃣ **Instalar Dependencias**

```bash
pip install -r requirements.txt
```

### 4️⃣ **Configuración Interactiva**

```bash
python start.py
```

El script te guiará paso a paso para:

- 🔑 Obtener tu token OAuth
- 🤖 Configurar el nombre del bot
- 📺 Especificar el canal de Twitch
- ⏰ Establecer el intervalo entre chistes

### 5️⃣ **¡Listo para usar!**

```bash
python twitch_bot.py
```

## ⚙️ Configuración Manual

Si prefieres configurar manualmente, crea un archivo `.env`:

```env
# Token OAuth del bot
BOT_TOKEN=oauth:tu_token_aqui

# Nombre del bot en Twitch
BOT_NICK=tu_bot_name

# Canal de Twitch (sin #)
TWITCH_CHANNEL=nombre_del_canal

# Intervalo entre chistes (segundos, mínimo 30)
MESSAGE_INTERVAL=100

# Bots adicionales a ignorar (opcional)
IGNORED_BOTS=mi_bot_personalizado,otro_bot
```

## 🎯 Obtener Token OAuth

1. Ve a [Twitch Token Generator](https://twitchtokengenerator.com/)
2. Selecciona "Bot Chat Token"
3. Autoriza con tu cuenta de bot
4. Copia el token (debe empezar con `oauth:`)

## 📋 Ejemplos de Contenido

### 😂 **Chistes Automáticos**
>
> "¿Por qué Plutón no puede ser DJ? ¡Porque le quitaron el título! 🎵"

> "Plutón en terapia: 'Doctora, siento que ya no importo' 💔"

### 🧠 **Factos Científicos**
>
> "FACTO 🧠: Plutón es más pequeño que nuestra Luna. ¡Incluso 7 lunas son más grandes!"

> "FACTO 🔬: Plutón no ha limpiado su órbita de otros objetos, por eso NO es planeta"

## 📂 Estructura del Proyecto

```
self-bot-twitch/
├── 📄 twitch_bot.py          # Bot principal
├── 📄 start.py               # Script de configuración
├── 📄 config.py              # Gestión de configuración
├── 📄 requirements.txt       # Dependencias
├── 📄 README.md              # Este archivo
├── 📄 LICENSE                # Licencia del proyecto
├── 📄 .gitignore            # Archivos ignorados por Git
└── 📄 .env                   # Configuración (se crea automáticamente)
```

## 🔧 Personalización

### Agregar Más Chistes

Edita `twitch_bot.py` y modifica la lista `self.bad_jokes`:

```python
self.bad_jokes = [
    "Tu nuevo chiste aquí 😂",
    # ... más chistes
]
```

### Agregar Más Factos

Modifica la lista `self.anti_pluto_facts`:

```python
self.anti_pluto_facts = [
    "FACTO 🌟: Tu nuevo facto científico aquí",
    # ... más factos
]
```

### Cambiar Patrones de Detección

Modifica `pluto_patterns` en el método `event_message`:

```python
pluto_patterns = [
    r'\bplut[oó]n\b',
    r'\btu_patron_aqui\b',
    # ... más patrones
]
```

## 📊 Logging y Monitoreo

El bot genera logs detallados en `bot.log`:

- ✅ Conexiones exitosas
- 📤 Chistes enviados
- 🎯 Factos activados
- ❌ Errores y reconexiones

## 🛠️ Solución de Problemas

### Error de Conexión

- ✅ Verifica que el token OAuth sea correcto
- ✅ Asegúrate de que el canal existe
- ✅ Revisa tu conexión a internet

### Error de Encoding

- ✅ El bot incluye manejo automático de UTF-8
- ✅ Compatible con emojis y caracteres especiales

### Bot No Responde

- ✅ Verifica que el bot tenga permisos de chat
- ✅ Revisa los logs en `bot.log`

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. 🍴 Fork el proyecto
2. 🌿 Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. 💾 Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. 📤 Push a la rama (`git push origin feature/nueva-caracteristica`)
5. 🔄 Abre un Pull Request

## 📜 Licencia

Este proyecto está bajo la licencia [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

**Esto significa que puedes:**

- ✅ Compartir - copiar y redistribuir
- ✅ Adaptar - remezclar, transformar y construir sobre el material

**Bajo las siguientes condiciones:**

- 📝 **Atribución** - Debes dar crédito apropiado
- 🚫 **No Comercial** - No puedes usar para propósitos comerciales
- 🔄 **Compartir Igual** - Si remezclas, debes distribuir bajo la misma licencia

## 👨‍💻 Autor

**llopgui**

- 🌐 GitHub: [@llopgui](https://github.com/llopgui/)
- 📅 Fecha de creación: Junio 2025

## ⭐ Agradecimientos

- 🚀 [TwitchIO](https://github.com/TwitchIO/TwitchIO) - Librería para conexión con Twitch
- 🌍 La comunidad de Python
- 🪐 Los defensores de la clasificación planetaria correcta

---

<div align="center">

**¿Te gustó el proyecto? ¡Dale una ⭐ estrella!**

*Mantengamos la ciencia correcta, un chiste a la vez* 🚀

</div>

## 🤖 Filtrado de Bots

El bot incluye **filtrado inteligente** que evita responder a otros bots comunes de Twitch, previniendo spam y bucles infinitos.

### 🔧 **Bots Ignorados Automáticamente**

El bot ignora por defecto estos bots populares:

- **StreamElements**: streamelements, streamelementsonline
- **Streamlabs**: streamlabs, streamlabsbot
- **Nightbot**: nightbot, nightbot2
- **Moobot**: moobot, moo_bot
- **Otros**: fossabot, wizebot, coebot, y muchos más...

### ➕ **Añadir Bots Personalizados**

Para ignorar bots adicionales, añade al archivo `.env`:

```env
# Separar múltiples bots con comas
IGNORED_BOTS=mi_bot_personalizado,otro_bot,bot_especial
```

### 📊 **Verificar Bots Ignorados**

El bot registra en los logs cuántos bots está ignorando:

```
INFO - Bots ignorados: 45
DEBUG - Lista de bots ignorados: ['streamelements', 'nightbot', ...]

```

## ⚠️ **Importante: Sin Comandos**

Este bot **NO tiene comandos**. Es completamente automático y funciona mediante:

- ✅ **Chistes automáticos** cada X segundos configurables
- ✅ **Respuestas automáticas** cuando detecta menciones de "Plutón"
- ✅ **Filtrado automático** de otros bots
- ❌ **NO responde a !comandos** - No es un bot tradicional de chat

Si buscas un bot con comandos (!hola, !clima, etc.), este no es el bot que necesitas.

---

## �� Filtrado de Bots
