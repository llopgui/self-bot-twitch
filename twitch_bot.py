"""
Self Bot Twitch - Bot Antiplutoniano
====================================

Bot para Twitch que envía chistes malos automáticamente y responde con
factos científicos cuando alguien menciona a Plutón. Completamente automático,
sin comandos ni interacción manual requerida.

Características:
- Chistes automáticos cada X segundos
- Detección automática de menciones de Plutón
- Respuestas con factos científicos anti-Plutón
- Sistema de logging robusto con soporte UTF-8
- Configuración simple mediante archivo .env

Autor: llopgui https://github.com/llopgui/
Fecha de creación: Junio 2025
Licencia: CC BY-NC-SA 4.0
Repositorio: https://github.com/llopgui/self-bot-twitch
"""

import asyncio
import logging
import random
import re
import sys
from datetime import datetime

from twitchio.ext import commands

from config import BotConfig

# Configurar encoding para Windows
if sys.platform.startswith("win"):
    # Configurar consola para UTF-8 en Windows
    import codecs

    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer)


def safe_log_text(text: str, max_length: int = 50) -> str:
    """
    Convierte texto con emojis a un formato seguro para logging.

    Args:
        text (str): Texto original que puede contener emojis
        max_length (int): Longitud máxima del texto truncado

    Returns:
        str: Texto seguro para logging sin emojis problemáticos
    """
    try:
        # Truncar texto si es muy largo
        truncated = text[:max_length]
        if len(text) > max_length:
            truncated += "..."

        # Intentar codificar y decodificar para verificar compatibilidad
        truncated.encode("utf-8").decode("utf-8")
        return truncated
    except UnicodeError:
        # Si hay problemas de encoding, usar representación ASCII
        safe_text = text.encode("ascii", errors="replace").decode("ascii")
        result = safe_text[:max_length]
        if len(safe_text) > max_length:
            result += "..."
        return result


# Configurar logging con soporte UTF-8
def setup_logging():
    """
    Configura el sistema de logging con soporte para UTF-8.
    """
    # Crear formatador
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Configurar handler para archivo con UTF-8
    try:
        file_handler = logging.FileHandler("bot.log", encoding="utf-8")
        file_handler.setFormatter(formatter)
    except Exception:
        # Fallback sin encoding específico
        file_handler = logging.FileHandler("bot.log")
        file_handler.setFormatter(formatter)

    # Configurar handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Configurar logger principal
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers.clear()  # Limpiar handlers existentes
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return logging.getLogger(__name__)


# Configurar logging
logger = setup_logging()


class AntiplotonianoBot(commands.Bot):
    """
    Bot principal de Twitch que hereda de twitchio.ext.commands.Bot.

    Características:
    - Conexión a canal específico
    - Chistes malos automáticos
    - Respuestas anti-Plutón cuando detecta menciones
    - Logging de eventos
    """

    def __init__(self, config: BotConfig):
        """
        Inicializa el bot con la configuración proporcionada.

        Args:
            config (BotConfig): Configuración del bot
        """
        # Inicializar el bot padre (sin prefijo ya que no usamos comandos)
        super().__init__(
            token=config.token,
            prefix="$",  # Prefijo que nadie usará
            initial_channels=config.get_channels(),
        )

        self.config = config
        self.start_time = datetime.now()
        self.joke_count = 0
        self.pluto_fact_count = 0
        self.is_running = False

        # Lista de chistes cortos malos
        self.bad_jokes = [
            ("¿Por qué Plutón no puede ser DJ? " "¡Porque le quitaron el título! 🎵"),
            ("Plutón llamó al servicio técnico: " "'Me degradaron a planeta enano' 😂"),
            ("¿Qué le dice un planeta a Plutón? " "'Ya no eres de los nuestros' 🪐"),
            "Plutón en terapia: 'Doctora, siento que ya no importo' 💔",
            ("¿Por qué Plutón no va a fiestas? " "Porque siempre lo dejan fuera 🎉"),
            (
                "Plutón pidiendo trabajo: 'Tengo experiencia como planeta...' "
                "'Teníamos' 💼"
            ),
            ("¿Cuál es el planeta más triste? " "¡Plutón, porque lo expulsaron! 😢"),
            "Plutón: 'Antes era cool' Neptuno: 'Antes eras planeta' 🔥",
            (
                "¿Por qué Plutón no usa redes sociales? "
                "Porque le quitaron la verificación azul ✅"
            ),
            "Plutón en el curriculum: 'Ex-planeta (2006-presente)' 📄",
        ]

        # Lista de factos anti-Plutón
        self.anti_pluto_facts = [
            (
                "FACTO 🧠: Plutón es más pequeño que nuestra Luna. "
                "¡Incluso 7 lunas son más grandes!"
            ),
            (
                "FACTO 🔬: Plutón no ha limpiado su órbita de otros objetos, "
                "por eso NO es planeta"
            ),
            (
                "FACTO 🌌: Hay al menos 5 objetos similares a Plutón "
                "en el cinturón de Kuiper"
            ),
            (
                "FACTO ⚖️: Plutón tiene solo 0.07 veces la masa "
                "de todos los objetos en su órbita"
            ),
            (
                "FACTO 🌍: Si Plutón fuera planeta, "
                "tendríamos que clasificar 100+ planetas más"
            ),
            (
                "FACTO 📏: Plutón es 5 veces más pequeño que la Tierra. "
                "¡Es minúsculo!"
            ),
            (
                "FACTO 🎯: La decisión de 2006 fue CORRECTA: "
                "Plutón no cumple los 3 criterios planetarios"
            ),
            (
                "FACTO 🚀: Incluso New Horizons confirmó: "
                "Plutón es un planeta enano, no un planeta"
            ),
            (
                "FACTO 🧮: Matemáticamente, Plutón no domina "
                "gravitacionalmente su región orbital"
            ),
            (
                "FACTO 🌟: Plutón orbita con Caronte casi como sistema binario. "
                "¡Qué raro para un 'planeta'!"
            ),
            (
                "FACTO 📚: Los libros de texto MEJORARON "
                "cuando sacaron a Plutón de la lista de planetas"
            ),
            ("FACTO 🏆: Ser planeta enano es genial, " "¡pero NO es ser planeta!"),
        ]

        logger.info(f"Bot inicializado para el canal: {config.channel}")
        logger.info(f"Chistes cargados: {len(self.bad_jokes)}")
        logger.info(f"Factos anti-Plutón cargados: {len(self.anti_pluto_facts)}")

    async def event_ready(self):
        """
        Evento que se ejecuta cuando el bot se conecta exitosamente.
        """
        self.is_running = True
        logger.info(f"Bot {self.nick} conectado exitosamente!")
        logger.info(f"Conectado a los canales: {self.connected_channels}")

        # Iniciar el bucle de chistes automáticos
        asyncio.create_task(self.automatic_joke_loop())

    async def event_message(self, message):
        """
        Evento que se ejecuta cuando se recibe un mensaje en el chat.
        Detecta menciones de Plutón y responde con factos.

        Args:
            message: Mensaje recibido del chat
        """
        # Evitar que el bot responda a sus propios mensajes
        if message.echo:
            return

        # Log del mensaje recibido
        author_name = message.author.name
        content = message.content
        if not content:
            return
        content = content.lower()
        logger.debug(f"Mensaje de {author_name}: {content}")

        # Detectar menciones de Plutón (variaciones comunes)
        pluto_patterns = [
            r"\bplut[oó]n\b",
            r"\bpluto\b",
            r"\bplanet\w*\s+plut[oó]n\b",
            r"\bplut[oó]n\s+planet\w*\b",
        ]

        if any(re.search(pattern, content) for pattern in pluto_patterns):
            await self.respond_anti_pluto(message.channel)

    async def automatic_joke_loop(self):
        """
        Bucle principal para enviar chistes automáticos.
        """
        logger.info("Iniciando bucle de chistes automáticos...")

        while self.is_running:
            try:
                # Esperar el intervalo configurado
                await asyncio.sleep(self.config.message_interval)

                # Enviar un chiste aleatorio
                joke = random.choice(self.bad_jokes)
                await self.send_automatic_joke(joke)

            except Exception as e:
                logger.error(f"Error en bucle de chistes: {e}")
                # Esperar un minuto antes de reintentar
                await asyncio.sleep(60)

    async def send_automatic_joke(self, joke: str):
        """
        Envía un chiste automático al canal.

        Args:
            joke (str): Chiste a enviar
        """
        try:
            channel = self.get_channel(self.config.channel)
            if channel:
                await channel.send(joke)
                self.joke_count += 1
                safe_joke = safe_log_text(joke)
                logger.info(f"Chiste automático enviado: {safe_joke}")
            else:
                channel_name = self.config.channel
                logger.warning(f"No se pudo encontrar el canal: {channel_name}")

        except Exception as e:
            logger.error(f"Error enviando chiste automático: {e}")

    async def respond_anti_pluto(self, channel):
        """
        Responde con un facto anti-Plutón cuando alguien menciona Plutón.

        Args:
            channel: Canal donde enviar la respuesta
        """
        try:
            fact = random.choice(self.anti_pluto_facts)
            await channel.send(fact)
            self.pluto_fact_count += 1
            safe_fact = safe_log_text(fact)
            logger.info(f"Facto anti-Plutón enviado: {safe_fact}")
        except Exception as e:
            logger.error(f"Error enviando facto anti-Plutón: {e}")

    def stop_bot(self):
        """
        Detiene el bucle de chistes automáticos.
        """
        self.is_running = False
        logger.info("Bot detenido por el usuario")
        stats_msg = (
            f"Estadísticas finales - Chistes: {self.joke_count}, "
            f"Factos: {self.pluto_fact_count}"
        )
        logger.info(stats_msg)


async def main():
    """
    Función principal que inicializa y ejecuta el bot.
    """
    try:
        # Cargar configuración
        config = BotConfig()
        logger.info("Configuración cargada exitosamente")

        # Crear y ejecutar el bot
        bot = AntiplotonianoBot(config)
        logger.info("Iniciando bot...")

        await bot.start()

    except ValueError as e:
        logger.error(f"Error de configuración: {e}")
        print(f"\n❌ Error de configuración: {e}")
        print("Por favor, revisa tu archivo .env")

    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        print(f"\n❌ Error inesperado: {e}")

    finally:
        logger.info("Bot terminado")


if __name__ == "__main__":
    """
    Punto de entrada principal del programa.
    """
    print("🚀 Iniciando Self Bot Twitch...")
    print("Presiona Ctrl+C para detener el bot")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot detenido por el usuario")
        logger.info("Bot detenido por KeyboardInterrupt")
    except Exception as e:
        print(f"\n💥 Error fatal: {e}")
        logger.critical(f"Error fatal: {e}")
