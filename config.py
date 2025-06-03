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
from typing import List

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

        # Validar configuración
        self._validate_config()

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
