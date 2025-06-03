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
            ("🎧 ¿Por qué Plutón no puede ser DJ? " "¡Porque le quitaron el título!"),
            ("📞 ¿Cómo llama Plutón a sus amigos? " "¡Planetarios perdidos!"),
            ("📝 ¿Por qué Plutón reprobó el examen? " "¡Porque no clasificó!"),
            ("🌍 ¿Qué le dijo Plutón a la Tierra? " "«Eres un planeta insoportable»."),
            (
                "⚽ ¿Por qué Plutón no juega fútbol? "
                "¡Porque siempre lo sacan por falta de categoría!"
            ),
            (
                "🛡️ ¿Cómo se defiende Plutón en el espacio? "
                "«¡Soy enano, pero con clase!»."
            ),
            ("🪐 ¿Qué le dijo Júpiter a Plutón? " "«Deja de orbitar mis problemas»."),
            (
                "🎉 ¿Por qué Plutón no entra en la lista de invitados? "
                "¡Porque lo degradaron a plus-one!"
            ),
            ("🎵 ¿Qué música escucha Plutón? " "¡Coldplay-to!"),
            (
                "💪 ¿Por qué Plutón no va al gimnasio? "
                "¡Por más que entrena, sigue siendo enano!"
            ),
            (
                "😢 ¿Qué hace Plutón cuando está triste? "
                "¡Se pone a planetar su soledad!"
            ),
            (
                "🕵️ ¿Por qué Plutón es el mejor espía? "
                "¡Porque todos pasan sin notarlo!"
            ),
            (
                "🔭 ¿Qué le dijo un telescopio a Plutón? "
                "«Eres pequeño, pero brillas en la oscuridad»."
            ),
            ("⭐ ¿Cómo pide Plutón un deseo? " "«¡Que la IAU me reclasifique!»"),
            ("🗺️ ¿Por qué Plutón no usa GPS? " "¡Porque siempre está fuera del mapa!"),
            (
                "☀️ ¿Qué le dijo el Sol a Plutón? "
                "«Deja de darme vueltas, ¡que me mareas!»."
            ),
            ("📖 ¿Por qué Plutón es buen poeta? " "¡Porque escribe versos enanos!"),
            ("🎓 ¿Qué estudia Plutón en la universidad? " "¡Astrología dwarf!"),
            ("👋 ¿Cómo se despiden en Plutón? " "«¡Nos orbitamos pronto!»."),
            (
                "🌙 ¿Qué le dijo la Luna a Plutón? "
                "«No te sientas mal... ¡yo tampoco soy planeta!»"
            ),
            (
                "🍕 ¿Por qué Plutón no puede pedir pizza? "
                "¡Porque no está en el área de entrega!"
            ),
            (
                "💼 ¿Qué pone Plutón en su CV? "
                "«Ex-planeta con experiencia en el espacio»."
            ),
            (
                "🎮 ¿Por qué Plutón no juega videojuegos? "
                "¡Porque siempre lo sacan del lobby!"
            ),
            (
                "☎️ ¿Qué dice Plutón cuando contesta el teléfono? "
                "«¿Aló? ¿Siguen ahí mis derechos planetarios?»"
            ),
            (
                "🎭 ¿Por qué Plutón es buen actor? "
                "¡Porque domina el papel de marginado!"
            ),
            ("🏠 ¿Dónde vive Plutón? " "¡En el barrio de los planetas enanos!"),
            (
                "🎪 ¿Por qué Plutón no va al circo? "
                "¡Porque él ya es el show de los enanos!"
            ),
            (
                "🧠 ¿Qué piensa Plutón antes de dormir? "
                "«Mañana seré planeta... ¡otra vez!»"
            ),
            ("🎂 ¿Cómo celebra Plutón su cumpleaños? " "¡Cada 248 años terrestres!"),
            ("🚗 ¿Por qué Plutón no maneja? " "¡Porque su órbita es muy excéntrica!"),
        ]

        # Lista de factos anti-Plutón
        self.anti_pluto_facts = [
            (
                "🌌 FACTO: Plutón no ha limpiado su órbita de otros objetos. "
                "¡Su vecindario está lleno de cuerpos del Cinturón de Kuiper!"
            ),
            (
                "📊 FACTO: La IAU reclasificó Plutón como planeta enano "
                "en 2006. ¡Una decisión que causó controversia mundial!"
            ),
            (
                "🛸 FACTO: Plutón comparte órbita con otros objetos celestes. "
                "¡Los planetas dominan solitarios sus órbitas!"
            ),
            (
                "📏 FACTO: Es más pequeño que nuestra Luna. "
                "¡Solo tiene 2,370 km de diámetro!"
            ),
            (
                "⚖️ FACTO: Su masa es apenas el 0.2% de la masa terrestre. "
                "¡Ni siquiera es el más masivo de los planetas enanos!"
            ),
            (
                "🔢 FACTO: Existen 5 planetas enanos reconocidos: "
                "Plutón, Eris, Ceres, Makemake y Haumea. ¡Plutón es uno más!"
            ),
            (
                "🌊 FACTO: La gravedad de Neptuno influye en Plutón. "
                "¡Su órbita es caótica por esta interacción!"
            ),
            (
                "⚡ FACTO: Eris es más masivo que Plutón. "
                "¡Su descubrimiento impulsó la reclasificación!"
            ),
            (
                "📐 FACTO: Órbita inclinada 17° sobre la eclíptica. "
                "¡Los planetas tienen órbitas casi planas!"
            ),
            (
                "🎯 FACTO: Su órbita es excéntrica y elíptica. "
                "¡Cruza la órbita de Neptuno!"
            ),
            (
                "🔍 FACTO: Forma parte del Cinturón de Kuiper. "
                "¡Es uno de sus objetos más brillantes!"
            ),
            (
                "📋 FACTO: No cumple el tercer criterio planetario. "
                "'Limpiar su órbita' es clave según la IAU."
            ),
            (
                "🎱 FACTO: Solo 8 cuerpos cumplen todos los criterios: "
                "De Mercurio a Neptuno, según la IAU."
            ),
            (
                "🚧 FACTO: Comparte zona con otros objetos transneptunianos. "
                "¡Su 'barrio' orbital está congestionado!"
            ),
            (
                "📦 FACTO: Su tamaño es inferior a 7 lunas del sistema solar. "
                "¡Ganímedes, Titán y otras son mayores!"
            ),
            (
                "🚀 FACTO: La sonda New Horizons reveló su complejidad. "
                "¡Pero su geología no cambió su estatus!"
            ),
            (
                "🔄 FACTO: Ceres fue reclasificado igual en 2006: "
                "¡De asteroide a planeta enano!"
            ),
            (
                "🌙 FACTO: Plutón tiene 5 lunas conocidas. "
                "¡Caronte es casi tan grande como él!"
            ),
            (
                "🎪 FACTO: La definición excluye cuerpos en discos densos. "
                "¡El Cinturón de Kuiper califica como tal!"
            ),
            (
                "🔬 FACTO: Alan Stern propuso definición geofísica. "
                "¡Pero la IAU mantiene criterios dinámicos!"
            ),
            (
                "🗳️ FACTO: Solo 1% de astrónomos votó en 2006. "
                "¡424 expertos decidieron su destino!"
            ),
            (
                "⏰ FACTO: Su órbita tarda 248 años terrestres. "
                "¡Y nunca completó una desde su descubrimiento!"
            ),
            (
                "👑 FACTO: No es el objeto más grande del Cinturón. "
                "¡Eris y Plutón son casi gemelos!"
            ),
            (
                "💪 FACTO: Planetas dominan gravitacionalmente su zona. "
                "¡Plutón es influenciado por Neptuno!"
            ),
            (
                "🌬️ FACTO: Su atmósfera colapsa y revive estacionalmente. "
                "¡Pero esto no afecta su clasificación!"
            ),
            (
                "🏔️ FACTO: Tiene montañas de hielo de agua. "
                "¡Complejidad ≠ definición planetaria!"
            ),
            (
                "⚙️ FACTO: La IAU usa criterios dinámicos, no geológicos. "
                "¡Importa su interacción orbital!"
            ),
            (
                "☄️ FACTO: Si estuviera cerca del Sol, sería cometa. "
                "¡Sus hielos se sublimarían!"
            ),
            (
                "📊 FACTO: Existen +1,200 objetos similares en el Cinturón. "
                "¡Clasificarlos como planetas sería caótico!"
            ),
            (
                "📅 FACTO: Descubierto en 1930, fue planeta 76 años. "
                "¡El más breve de la historia!"
            ),
            (
                "📚 FACTO: Su nombre ya no está en listas planetarias. "
                "¡Los libros de texto se actualizaron!"
            ),
            (
                "🤔 FACTO: Algunos científicos rechazan la definición. "
                "¡El debate continúa hoy!"
            ),
            (
                "🪶 FACTO: La gravedad plutoniana es muy débil. "
                "¡6 veces menor que la lunar!"
            ),
            (
                "🌘 FACTO: Planetas enanos pueden tener lunas y atmósfera. "
                "¡Pero no son planetas según la IAU!"
            ),
            (
                "⏳ FACTO: Si limpiara su órbita, sería planeta. "
                "¡Pero le tomaría billones de años!"
            ),
            (
                "🧊 FACTO: Está compuesto principalmente de hielo y roca. "
                "¡Densidad de solo 1.9 g/cm³!"
            ),
            (
                "🌡️ FACTO: Temperatura superficial de -230°C. "
                "¡Demasiado frío para actividad geológica activa!"
            ),
            (
                "🔭 FACTO: Tomó 76 años descubrir que tenía lunas. "
                "¡Caronte fue encontrada en 1978!"
            ),
            (
                "🎭 FACTO: Plutón y Caronte forman sistema binario. "
                "¡Ambos orbitan un punto común!"
            ),
            (
                "💫 FACTO: Su brillo varía por rotación y composición. "
                "¡6.4 días terrestres por rotación!"
            ),
            (
                "🎪 FACTO: Pertenece a la familia de plutinos. "
                "¡Objetos en resonancia 2:3 con Neptuno!"
            ),
            (
                "🌀 FACTO: Su órbita es resonante con Neptuno. "
                "¡2 órbitas de Plutón = 3 de Neptuno!"
            ),
            (
                "📡 FACTO: New Horizons tardó 9 años en llegar. "
                "¡Y solo pudo estudiarlo por horas!"
            ),
            (
                "🎨 FACTO: Su superficie tiene variaciones de color. "
                "¡Desde beige hasta rojizo por metano!"
            ),
            (
                "⚗️ FACTO: Atmósfera de nitrógeno, metano y CO. "
                "¡Pero 100,000 veces más tenue que la terrestre!"
            ),
            (
                "🏁 FACTO: Es el último 'planeta' descubierto. "
                "¡Después solo se han encontrado planetas enanos!"
            ),
            (
                "🎯 FACTO: Su órbita lo acerca más que Neptuno al Sol. "
                "¡Entre 1979-1999 fue el octavo!"
            ),
            (
                "🔄 FACTO: Acoplamiento de marea con Caronte. "
                "¡Siempre muestran la misma cara!"
            ),
            (
                "⭐ FACTO: Walt Disney lo nombró como su perro. "
                "¡Mismo año del descubrimiento: 1930!"
            ),
            (
                "🧮 FACTO: Su masa es 6 veces menor que la Luna. "
                "¡Y 400 veces menor que la Tierra!"
            ),
            (
                "🔍 FACTO: Se necesitó el telescopio Hubble. "
                "¡Para resolver sus lunas más pequeñas!"
            ),
            (
                "🌪️ FACTO: No tiene campo magnético detectable. "
                "¡A diferencia de los planetas rocosos!"
            ),
            (
                "🎲 FACTO: Fue descubierto por accidente. "
                "¡Buscando el hipotético Planeta X!"
            ),
            (
                "📐 FACTO: Su eje de rotación está inclinado 122°. "
                "¡Rota casi de costado como Urano!"
            ),
            (
                "🌊 FACTO: Podría tener océano subsuperficial. "
                "¡Pero eso no lo hace planeta!"
            ),
            (
                "🎪 FACTO: Es miembro del club de los KBO. "
                "¡Kuiper Belt Objects, no planetas!"
            ),
            (
                "⚖️ FACTO: La decisión de la IAU fue democrática. "
                "¡Votación científica, no política!"
            ),
            (
                "🏆 FACTO: Mantiene récord de excentricidad orbital. "
                "¡Entre todos los explanetas del sistema!"
            ),
            (
                "🔬 FACTO: Su estudio ayudó a definir 'planeta'. "
                "¡Ironía: contribuyó a su propia reclasificación!"
            ),
            (
                "🎯 FACTO: Es el prototipo de planeta enano. "
                "¡Definió toda una nueva categoría!"
            ),
            (
                "📊 FACTO: Solo 0.07% del tamaño de la Tierra. "
                "¡Más pequeño que Australia!"
            ),
            (
                "🌌 FACTO: Está en la frontera del sistema solar. "
                "¡Donde comienza el espacio interestelar!"
            ),
            (
                "🎪 FACTO: Representa la transición histórica. "
                "¡De 9 a 8 planetas oficiales!"
            ),
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
