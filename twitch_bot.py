#!/usr/bin/env python3
"""
Bot principal de Twitch Anti-Plutoniano
======================================

Un bot de Twitch que responde automáticamente con chistes malos
y datos sobre Plutón cuando detecta menciones del planeta.

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

import twitchio

from config import BotConfig

# Configurar encoding para Windows
if sys.platform.startswith("win"):
    # Configurar consola para UTF-8 en Windows
    import codecs

    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer)

# Configurar logging
logger = logging.getLogger(__name__)


class AntiplotonianoBot(twitchio.Client):
    """
    Bot principal de Twitch que NO usa comandos.

    Características:
    - Conexión a canal específico
    - Chistes malos automáticos
    - Respuestas anti-Plutón cuando detecta menciones
    - Sistema de filtrado de bots
    - Logging de eventos
    """

    def __init__(self, config: BotConfig):
        """
        Inicializa el bot con la configuración proporcionada.

        Args:
            config (BotConfig): Configuración del bot
        """
        # Inicializar el cliente padre (sin funcionalidades de comandos)
        super().__init__(
            token=config.token,
            initial_channels=config.get_channels(),
        )

        # Guardar configuración
        self.config = config

        # Cargar chistes malos desde archivo o usar por defecto
        self.bad_jokes = self._load_bad_jokes()

        # Cargar factos anti-Plutón desde archivo o usar por defecto
        self.anti_pluto_facts = self._load_anti_pluto_facts()

        # Configurar el bucle de chistes automáticos
        self.joke_task = None

        # Log de inicio
        logger.info(f"Bot inicializado para el canal: {config.channel}")
        logger.info(f"Chistes cargados: {len(self.bad_jokes)}")
        anti_pluto_count = len(self.anti_pluto_facts)
        logger.info(f"Factos anti-Plutón cargados: {anti_pluto_count}")
        logger.info(f"Bots ignorados: {len(self.config.ignored_bots)}")
        first_ten = self.config.get_ignored_bots_list()[:10]
        extra = "..." if len(self.config.ignored_bots) > 10 else ""
        logger.debug(f"Lista de bots ignorados: {first_ten}{extra}")

    def _load_bad_jokes(self) -> list:
        """
        Carga chistes malos desde un archivo o usa una lista por defecto.

        Returns:
            list: Lista de chistes malos
        """
        default_jokes = [
            "🎧 ¿Por qué Plutón no puede ser DJ? ¡Porque le quitaron el título!",
            "📞 ¿Cómo llama Plutón a sus amigos? ¡Planetarios perdidos!",
            "📝 ¿Por qué Plutón reprobó el examen? ¡Porque no clasificó!",
            "🌍 ¿Qué le dijo Plutón a la Tierra? «Eres un planeta insoportable».",
            "⚽ ¿Por qué Plutón no juega fútbol? ¡Porque siempre lo sacan por falta de categoría!",
            "🛡️ ¿Cómo se defiende Plutón en el espacio? «¡Soy enano, pero con clase!».",
            "🪐 ¿Qué le dijo Júpiter a Plutón? «Deja de orbitar mis problemas».",
            "🎉 ¿Por qué Plutón no entra en la lista de invitados? ¡Porque lo degradaron a plus-one!",
            "🎵 ¿Qué música escucha Plutón? ¡Coldplay-to!",
            "💪 ¿Por qué Plutón no va al gimnasio? ¡Por más que entrena, sigue siendo enano!",
            "😢 ¿Qué hace Plutón cuando está triste? ¡Se pone a planetar su soledad!",
            "🕵️ ¿Por qué Plutón es el mejor espía? ¡Porque todos pasan sin notarlo!",
            "🔭 ¿Qué le dijo un telescopio a Plutón? «Eres pequeño, pero brillas en la oscuridad».",
            "⭐ ¿Cómo pide Plutón un deseo? «¡Que la IAU me reclasifique!»",
            "🗺️ ¿Por qué Plutón no usa GPS? ¡Porque siempre está fuera del mapa!",
            "☀️ ¿Qué le dijo el Sol a Plutón? «Deja de darme vueltas, ¡que me mareas!».",
            "📖 ¿Por qué Plutón es buen poeta? ¡Porque escribe versos enanos!",
            "🎓 ¿Qué estudia Plutón en la universidad? ¡Astrología dwarf!",
            "👋 ¿Cómo se despiden en Plutón? «¡Nos orbitamos pronto!».",
            "🌙 ¿Qué le dijo la Luna a Plutón? «No te sientas mal... ¡yo tampoco soy planeta!»",
            "🍕 ¿Por qué Plutón no puede pedir pizza? ¡Porque no está en el área de entrega!",
            "💼 ¿Qué pone Plutón en su CV? «Ex-planeta con experiencia en el espacio».",
            "🎮 ¿Por qué Plutón no juega videojuegos? ¡Porque siempre lo sacan del lobby!",
            "☎️ ¿Qué dice Plutón cuando contesta el teléfono? «¿Aló? ¿Siguen ahí mis derechos planetarios?»",
            "🎭 ¿Por qué Plutón es buen actor? ¡Porque domina el papel de marginado!",
            "🏠 ¿Dónde vive Plutón? ¡En el barrio de los planetas enanos!",
            "🎪 ¿Por qué Plutón no va al circo? ¡Porque él ya es el show de los enanos!",
            "🧠 ¿Qué piensa Plutón antes de dormir? «Mañana seré planeta... ¡otra vez!»",
            "🎂 ¿Cómo celebra Plutón su cumpleaños? ¡Cada 248 años terrestres!",
            "🚗 ¿Por qué Plutón no maneja? ¡Porque su órbita es muy excéntrica!",
        ]
        # En el futuro se puede cargar desde un archivo
        return default_jokes

    def _load_anti_pluto_facts(self) -> list:
        """
        Carga datos anti-Plutón desde un archivo o usa una lista por defecto.

        Returns:
            list: Lista de factos científicos contra Plutón
        """
        default_facts = [
            "🌌 FACTO: Plutón no ha limpiado su órbita de otros objetos. ¡Su vecindario está lleno de cuerpos del Cinturón de Kuiper!",
            "📊 FACTO: La IAU reclasificó Plutón como planeta enano en 2006. ¡Una decisión que causó controversia mundial!",
            "🛸 FACTO: Plutón comparte órbita con otros objetos celestes. ¡Los planetas dominan solitarios sus órbitas!",
            "📏 FACTO: Es más pequeño que nuestra Luna. ¡Solo tiene 2,370 km de diámetro!",
            "⚖️ FACTO: Su masa es apenas el 0.2% de la masa terrestre. ¡Ni siquiera es el más masivo de los planetas enanos!",
            "🔢 FACTO: Existen 5 planetas enanos reconocidos: Plutón, Eris, Ceres, Makemake y Haumea. ¡Plutón es uno más!",
            "🌊 FACTO: La gravedad de Neptuno influye en Plutón. ¡Su órbita es caótica por esta interacción!",
            "⚡ FACTO: Eris es más masivo que Plutón. ¡Su descubrimiento impulsó la reclasificación!",
            "📐 FACTO: Órbita inclinada 17° sobre la eclíptica. ¡Los planetas tienen órbitas casi planas!",
            "🎯 FACTO: Su órbita es excéntrica y elíptica. ¡Cruza la órbita de Neptuno!",
            "🔍 FACTO: Forma parte del Cinturón de Kuiper. ¡Es uno de sus objetos más brillantes!",
            "📋 FACTO: No cumple el tercer criterio planetario. 'Limpiar su órbita' es clave según la IAU.",
            "🎱 FACTO: Solo 8 cuerpos cumplen todos los criterios: De Mercurio a Neptuno, según la IAU.",
            "🚧 FACTO: Comparte zona con otros objetos transneptunianos. ¡Su 'barrio' orbital está congestionado!",
            "📦 FACTO: Su tamaño es inferior a 7 lunas del sistema solar. ¡Ganímedes, Titán y otras son mayores!",
            "🚀 FACTO: La sonda New Horizons reveló su complejidad. ¡Pero su geología no cambió su estatus!",
            "🔄 FACTO: Ceres fue reclasificado igual en 2006: ¡De asteroide a planeta enano!",
            "🌙 FACTO: Plutón tiene 5 lunas conocidas. ¡Caronte es casi tan grande como él!",
            "🎪 FACTO: La definición excluye cuerpos en discos densos. ¡El Cinturón de Kuiper califica como tal!",
            "🔬 FACTO: Alan Stern propuso definición geofísica. ¡Pero la IAU mantiene criterios dinámicos!",
            "🗳️ FACTO: Solo 1% de astrónomos votó en 2006. ¡424 expertos decidieron su destino!",
            "⏰ FACTO: Su órbita tarda 248 años terrestres. ¡Y nunca completó una desde su descubrimiento!",
            "👑 FACTO: No es el objeto más grande del Cinturón. ¡Eris y Plutón son casi gemelos!",
            "💪 FACTO: Planetas dominan gravitacionalmente su zona. ¡Plutón es influenciado por Neptuno!",
            "🌬️ FACTO: Su atmósfera colapsa y revive estacionalmente. ¡Pero esto no afecta su clasificación!",
            "🏔️ FACTO: Tiene montañas de hielo de agua. ¡Complejidad ≠ definición planetaria!",
            "⚙️ FACTO: La IAU usa criterios dinámicos, no geológicos. ¡Importa su interacción orbital!",
            "☄️ FACTO: Si estuviera cerca del Sol, sería cometa. ¡Sus hielos se sublimarían!",
            "📊 FACTO: Existen +1,200 objetos similares en el Cinturón. ¡Clasificarlos como planetas sería caótico!",
            "📅 FACTO: Descubierto en 1930, fue planeta 76 años. ¡El más breve de la historia!",
            "📚 FACTO: Su nombre ya no está en listas planetarias. ¡Los libros de texto se actualizaron!",
            "🤔 FACTO: Algunos científicos rechazan la definición. ¡El debate continúa hoy!",
            "🪶 FACTO: La gravedad plutoniana es muy débil. ¡6 veces menor que la lunar!",
            "🌘 FACTO: Planetas enanos pueden tener lunas y atmósfera. ¡Pero no son planetas según la IAU!",
            "⏳ FACTO: Si limpiara su órbita, sería planeta. ¡Pero le tomaría billones de años!",
            "🧊 FACTO: Está compuesto principalmente de hielo y roca. ¡Densidad de solo 1.9 g/cm³!",
            "🌡️ FACTO: Temperatura superficial de -230°C. ¡Demasiado frío para actividad geológica activa!",
            "🔭 FACTO: Tomó 76 años descubrir que tenía lunas. ¡Caronte fue encontrada en 1978!",
            "🎭 FACTO: Plutón y Caronte forman sistema binario. ¡Ambos orbitan un punto común!",
            "💫 FACTO: Su brillo varía por rotación y composición. ¡6.4 días terrestres por rotación!",
            "🎪 FACTO: Pertenece a la familia de plutinos. ¡Objetos en resonancia 2:3 con Neptuno!",
            "🌀 FACTO: Su órbita es resonante con Neptuno. ¡2 órbitas de Plutón = 3 de Neptuno!",
            "📡 FACTO: New Horizons tardó 9 años en llegar. ¡Y solo pudo estudiarlo por horas!",
            "🎨 FACTO: Su superficie tiene variaciones de color. ¡Desde beige hasta rojizo por metano!",
            "⚗️ FACTO: Atmósfera de nitrógeno, metano y CO. ¡Pero 100,000 veces más tenue que la terrestre!",
            "🏁 FACTO: Es el último 'planeta' descubierto. ¡Después solo se han encontrado planetas enanos!",
            "🎯 FACTO: Su órbita lo acerca más que Neptuno al Sol. ¡Entre 1979-1999 fue el octavo!",
            "🔄 FACTO: Acoplamiento de marea con Caronte. ¡Siempre muestran la misma cara!",
            "⭐ FACTO: Walt Disney lo nombró como su perro. ¡Mismo año del descubrimiento: 1930!",
            "🧮 FACTO: Su masa es 6 veces menor que la Luna. ¡Y 400 veces menor que la Tierra!",
            "🔍 FACTO: Se necesitó el telescopio Hubble. ¡Para resolver sus lunas más pequeñas!",
            "🌪️ FACTO: No tiene campo magnético detectable. ¡A diferencia de los planetas rocosos!",
            "🎲 FACTO: Fue descubierto por accidente. ¡Buscando el hipotético Planeta X!",
            "📐 FACTO: Su eje de rotación está inclinado 122°. ¡Rota casi de costado como Urano!",
            "🌊 FACTO: Podría tener océano subsuperficial. ¡Pero eso no lo hace planeta!",
            "🎪 FACTO: Es miembro del club de los KBO. ¡Kuiper Belt Objects, no planetas!",
            "⚖️ FACTO: La decisión de la IAU fue democrática. ¡Votación científica, no política!",
            "🏆 FACTO: Mantiene récord de excentricidad orbital. ¡Entre todos los explanetas del sistema!",
            "🔬 FACTO: Su estudio ayudó a definir 'planeta'. ¡Ironía: contribuyó a su propia reclasificación!",
            "🎯 FACTO: Es el prototipo de planeta enano. ¡Definió toda una nueva categoría!",
            "📊 FACTO: Solo 0.07% del tamaño de la Tierra. ¡Más pequeño que Australia!",
            "🌌 FACTO: Está en la frontera del sistema solar. ¡Donde comienza el espacio interestelar!",
            "🎪 FACTO: Representa la transición histórica. ¡De 9 a 8 planetas oficiales!",
            "🚫 FACTO: Plutón NO es un planeta desde 2006. Es un planeta enano.",
            "🌕 FACTO: La luna de la Tierra es más grande que Plutón.",
            "📏 FACTO: Plutón mide solo 2,374 km de diámetro. ¡Minúsculo!",
        ]
        # En el futuro se puede cargar desde un archivo
        return default_facts

    async def event_ready(self):
        """
        Evento que se ejecuta cuando el bot se conecta exitosamente.
        """
        logger.info(f"Bot conectado como: {self.nick}")

        # Iniciar bucle de chistes automáticos
        if not self.joke_task:
            self.joke_task = self.loop.create_task(self._joke_loop())
            logger.info("Bucle de chistes automáticos iniciado")

    async def event_message(self, message):
        """
        Evento que se ejecuta cuando se recibe un mensaje en el chat.
        Detecta menciones de Plutón y responde con factos.
        Ignora mensajes de otros bots según la configuración.

        Args:
            message: Mensaje recibido del chat
        """
        # Evitar que el bot responda a sus propios mensajes
        if message.echo:
            return

        # Obtener información del autor del mensaje
        author_name = message.author.name
        if not author_name:
            return

        # Verificar si debemos ignorar este usuario (bots, etc.)
        if self.config.is_ignored_user(author_name):
            logger.debug(f"Ignorando mensaje del bot: {author_name}")
            return

        # Obtener contenido del mensaje
        content = message.content
        if not content:
            return

        # Log del mensaje recibido (solo para usuarios no ignorados)
        logger.debug(f"Mensaje de {author_name}: {content}")

        # Detectar menciones de Plutón (case insensitive)
        pluto_patterns = [
            r"\bpluton\b",
            r"\bpluto\b",
            r"\bplanet[ao]?\s+pluton\b",
            r"\bplanet[ao]?\s+pluto\b",
        ]

        mensaje_lower = content.lower()
        pluto_mentioned = any(
            re.search(pattern, mensaje_lower) for pattern in pluto_patterns
        )

        if pluto_mentioned:
            # Seleccionar un facto aleatorio
            facto = random.choice(self.anti_pluto_facts)

            # Responder al usuario
            await message.channel.send(f"@{author_name} {facto}")

            logger.info(f"Respondido a {author_name} con facto anti-Plutón")

    async def _joke_loop(self):
        """
        Bucle asíncrono que envía chistes automáticamente en intervalos.
        """
        try:
            while True:
                # Esperar el intervalo configurado
                await asyncio.sleep(self.config.message_interval)

                # Seleccionar un chiste aleatorio
                joke = random.choice(self.bad_jokes)

                # Enviar al canal
                channel = self.get_channel(self.config.channel)
                if channel:
                    await channel.send(joke)
                    logger.info("Chiste automático enviado")
                else:
                    canal_msg = f"No se pudo encontrar el canal: {self.config.channel}"
                    logger.warning(canal_msg)

        except asyncio.CancelledError:
            logger.info("Bucle de chistes automáticos cancelado")
        except Exception as e:
            logger.error(f"Error en bucle de chistes: {e}")

    async def event_error(self, error, data):
        """
        Maneja errores del bot.

        Args:
            error: Error ocurrido
            data: Datos relacionados con el error
        """
        logger.error(f"Error del bot: {error}")
        logger.debug(f"Datos del error: {data}")


async def main():
    """
    Función principal que inicializa y ejecute el bot.
    """
    try:
        # Cargar configuración
        config = BotConfig()

        # Crear el bot
        bot = AntiplotonianoBot(config)

        # Ejecutar el bot
        logger.info("Iniciando bot...")
        await bot.start()

    except KeyboardInterrupt:
        logger.info("Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"Error al ejecutar el bot: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
