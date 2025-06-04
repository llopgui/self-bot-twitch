"""
Configuración del Self Bot Twitch
==================================

Este módulo maneja la configuración del bot usando variables de entorno.
Incluye validación de configuración y valores por defecto.

Autor: llopgui https://github.com/llopgui/
Fecha de creación: Junio 2025
Licencia: CC BY-NC-SA 4.0
Repositorio: https://github.com/llopgui/self-bot-twitch
"""

import os
from typing import List, Set

from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()


class BotConfig:
    """
    Clase para manejar la configuración del bot de Twitch.

    Attributes:
        token (str): Token OAuth del bot
        nick (str): Nombre del bot
        channel (str): Canal de Twitch al que se conecta
        message_interval (int): Intervalo entre chistes automáticos
        automatic_messages (List[str]): Lista de mensajes (obsoleta)
        ignored_bots (Set[str]): Set de nombres de bots a ignorar
    """

    def __init__(self):
        """Inicializa la configuración del bot."""
        self.token: str = os.getenv("BOT_TOKEN", "")
        self.nick: str = os.getenv("BOT_NICK", "antiplutoniano_bot")
        self.channel: str = os.getenv("TWITCH_CHANNEL", "")
        interval = os.getenv("MESSAGE_INTERVAL", "300")
        self.message_interval: int = int(interval)

        # Mensajes automáticos por defecto (ya no se usan)
        self.automatic_messages: List[str] = []

        # Lista de bots a ignorar (nombres en minúsculas para comparación)
        self.ignored_bots: Set[str] = self._load_ignored_bots()

        # Validar configuración
        self._validate_config()

    def _load_ignored_bots(self) -> Set[str]:
        """
        Carga la lista de bots a ignorar desde las variables de entorno
        y añade los bots más comunes de Twitch.

        Returns:
            Set[str]: Set de nombres de usuario de bots a ignorar
        """
        # Bots comunes de Twitch (en minúsculas)
        default_ignored_bots = {
            # StreamElements
            "streamelements",
            "streamelementsonline",
            "streamelements_bot",
            # Streamlabs
            "streamlabs",
            "streamlabsbot",
            "streamlabsio",
            # Nightbot
            "nightbot",
            "nightbot2",
            # Moobot
            "moobot",
            "moo_bot",
            # Wizebot
            "wizebot",
            # Fossabot
            "fossabot",
            # Chatbots populares
            "coebot",
            "ankhbot",
            "xanaxbot",
            "twitchplaysbot",
            "commanderroot",
            "buttsbot",
            "roflgator",
            "mikubot",
            "supibot",
            "virgoproz",
            "bananasplit_bot",
            "dinu",
            "botrix",
            "logviewer",
            "pretzelrocks",
            "vivbot",
            "blerp",
            "songlistbot",
            "restreambot",
            "soundalerts",
            "monstercat",
            "twitchplayspokemon",
            "gamewisp",
            "revlobot",
            "deepbot",
            # Otros bots de servicios
            "discord",
            "youtube",
            "mixer",
            "facebook",
            "instagram",
            "twitter",
        }

        # Cargar bots adicionales desde variables de entorno
        custom_ignored = os.getenv("IGNORED_BOTS", "")
        if custom_ignored:
            # Separar por comas y convertir a minúsculas
            custom_bots = {
                bot.strip().lower() for bot in custom_ignored.split(",") if bot.strip()
            }
            default_ignored_bots.update(custom_bots)

        return default_ignored_bots

    def is_ignored_user(self, username: str) -> bool:
        """
        Verifica si un usuario debe ser ignorado por el bot.

        Args:
            username (str): Nombre de usuario a verificar

        Returns:
            bool: True si el usuario debe ser ignorado, False en caso
            contrario
        """
        if not username:
            return False

        # Convertir a minúsculas para comparación insensible a mayúsculas
        username_lower = username.lower()
        return username_lower in self.ignored_bots

    def add_ignored_bot(self, username: str) -> bool:
        """
        Añade un bot a la lista de ignorados.

        Args:
            username (str): Nombre del bot a ignorar

        Returns:
            bool: True si se añadió, False si ya existía
        """
        if not username:
            return False

        username_lower = username.strip().lower()
        if username_lower not in self.ignored_bots:
            self.ignored_bots.add(username_lower)
            return True
        return False

    def remove_ignored_bot(self, username: str) -> bool:
        """
        Elimina un bot de la lista de ignorados.

        Args:
            username (str): Nombre del bot a dejar de ignorar

        Returns:
            bool: True si se eliminó, False si no existía
        """
        if not username:
            return False

        username_lower = username.strip().lower()
        if username_lower in self.ignored_bots:
            self.ignored_bots.remove(username_lower)
            return True
        return False

    def get_ignored_bots_list(self) -> List[str]:
        """
        Obtiene la lista de bots ignorados como una lista ordenada.

        Returns:
            List[str]: Lista ordenada de nombres de bots ignorados
        """
        return sorted(list(self.ignored_bots))

    def _validate_config(self) -> None:
        """
        Valida que la configuración sea correcta.

        Raises:
            ValueError: Si falta configuración esencial
        """
        if not self.token:
            msg = (
                "BOT_TOKEN es requerido. "
                "Obténlo desde https://twitchtokengenerator.com/"
            )
            raise ValueError(msg)

        if not self.channel:
            raise ValueError(
                "TWITCH_CHANNEL es requerido. " "Especifica el canal sin #"
            )

        if not self.token.startswith("oauth:"):
            raise ValueError("BOT_TOKEN debe comenzar con 'oauth:'")

        if self.message_interval < 30:
            raise ValueError("MESSAGE_INTERVAL debe ser de al menos 30 segundos")

    def get_channels(self) -> List[str]:
        """
        Obtiene la lista de canales formateados para twitchio.

        Returns:
            List[str]: Lista de canales con formato correcto
        """
        return [self.channel]

    def add_automatic_message(self, message: str) -> None:
        """
        Añade un mensaje automático a la lista.

        Args:
            message (str): Mensaje a añadir
        """
        if message and message not in self.automatic_messages:
            self.automatic_messages.append(message)

    def remove_automatic_message(self, index: int) -> bool:
        """
        Elimina un mensaje automático por índice.

        Args:
            index (int): Índice del mensaje a eliminar

        Returns:
            bool: True si se eliminó, False en caso contrario
        """
        try:
            if 0 <= index < len(self.automatic_messages):
                self.automatic_messages.pop(index)
                return True
            return False
        except IndexError:
            return False
