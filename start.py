#!/usr/bin/env python3
"""
Script de Inicio Rápido - Self Bot Twitch
==========================================

Script interactivo para configurar y ejecutar el bot de Twitch
por primera vez. Te guía paso a paso para configurar el bot.

Autor: llopgui https://github.com/llopgui/
Fecha de creación: Junio 2025
Licencia: CC BY-NC-SA 4.0
Repositorio: https://github.com/llopgui/self-bot-twitch
"""

import os
import sys
import webbrowser
from pathlib import Path


def print_banner():
    """Muestra el banner del bot."""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                🤖 Self Bot Twitch                        ║
    ║                                                          ║
    ║           ¡Configuración rápida e interactiva!          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def check_dependencies():
    """
    Verifica que las dependencias estén instaladas.

    Returns:
        bool: True si todas las dependencias están disponibles
    """
    print("🔍 Verificando dependencias...")

    missing_deps = []

    try:
        import twitchio

        print("✅ twitchio - Instalado")
    except ImportError:
        missing_deps.append("twitchio")
        print("❌ twitchio - No encontrado")

    try:
        import dotenv

        print("✅ python-dotenv - Instalado")
    except ImportError:
        missing_deps.append("python-dotenv")
        print("❌ python-dotenv - No encontrado")

    if missing_deps:
        print(f"\n⚠️  Dependencias faltantes: {', '.join(missing_deps)}")
        print("📦 Ejecuta: pip install -r requirements.txt")
        return False

    print("✅ Todas las dependencias están instaladas!")
    return True


def create_env_file():
    """
    Crea interactivamente el archivo .env con la configuración del bot.

    Returns:
        bool: True si la configuración se completó exitosamente
    """
    print("\n⚙️  Configurando el bot...")

    # Verificar si ya existe un archivo .env
    if Path(".env").exists():
        response = input("📁 Ya existe un archivo .env. ¿Sobrescribir? (s/N): ")
        if response.lower() not in ["s", "sí", "si", "y", "yes"]:
            print("✅ Usando configuración existente.")
            return True

    print("\n📝 Necesitamos algunos datos para configurar tu bot:")
    print("=" * 50)

    # Obtener token OAuth
    print("\n1️⃣  TOKEN OAUTH")
    print("Para obtener tu token OAuth:")
    print("   1. Ve a: https://twitchtokengenerator.com/")
    print("   2. Selecciona 'Bot Chat Token'")
    print("   3. Autoriza con tu cuenta de bot")
    print("   4. Copia el token (empieza con 'oauth:')")

    open_browser = input("\n🌐 ¿Abrir la página del token en el navegador? (S/n): ")
    if open_browser.lower() not in ["n", "no"]:
        webbrowser.open("https://twitchtokengenerator.com/")

    while True:
        token = input("\n🔑 Introduce tu token OAuth: ").strip()
        if token.startswith("oauth:"):
            break
        print("❌ El token debe empezar con 'oauth:'. Inténtalo de nuevo.")

    # Obtener nombre del bot
    print("\n2️⃣  NOMBRE DEL BOT")
    bot_nick = input("🤖 Nombre del bot (nombre de usuario de Twitch): ").strip()

    # Obtener canal
    print("\n3️⃣  CANAL DE TWITCH")
    channel = input("📺 Canal al que se conectará (sin #): ").strip()

    # Obtener intervalo de mensajes
    print("\n4️⃣  CONFIGURACIÓN DE MENSAJES")
    while True:
        try:
            interval = int(
                input("⏰ Intervalo entre chistes automáticos (segundos, mínimo 30): ")
            )
            if interval >= 30:
                break
            print("❌ El intervalo debe ser de al menos 30 segundos.")
        except ValueError:
            print("❌ Por favor, introduce un número válido.")

    # Crear archivo .env
    env_content = f"""# Configuración del Self Bot Twitch
# Generado automáticamente por start.py
# Autor: llopgui https://github.com/llopgui/

# Token del bot (OAuth)
BOT_TOKEN={token}

# Nombre del bot
BOT_NICK={bot_nick}

# Canal de Twitch
TWITCH_CHANNEL={channel}

# Intervalo entre chistes automáticos (segundos)
MESSAGE_INTERVAL={interval}
"""

    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("\n✅ Archivo .env creado exitosamente!")
        return True
    except Exception as e:
        print(f"\n❌ Error creando archivo .env: {e}")
        return False


def show_summary():
    """Muestra un resumen de la configuración."""
    print("\n📋 RESUMEN DE LA CONFIGURACIÓN")
    print("=" * 40)

    try:
        from dotenv import load_dotenv

        load_dotenv()

        print(f"🤖 Bot: {os.getenv('BOT_NICK', 'No configurado')}")
        print(f"📺 Canal: {os.getenv('TWITCH_CHANNEL', 'No configurado')}")
        print(
            f"⏰ Intervalo: {os.getenv('MESSAGE_INTERVAL', 'No configurado')} segundos"
        )

    except Exception as e:
        print(f"❌ Error leyendo configuración: {e}")


def start_bot():
    """Inicia el bot de Twitch."""
    print("\n🚀 Iniciando el bot...")
    print("💡 Presiona Ctrl+C para detener el bot cuando quieras")
    print("=" * 50)

    try:
        # Importar y ejecutar el bot
        import asyncio

        from twitch_bot import main

        asyncio.run(main())

    except KeyboardInterrupt:
        print("\n\n👋 Bot detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando el bot: {e}")
        print("💡 Revisa tu configuración en el archivo .env")


def main():
    """Función principal del script de inicio."""
    print_banner()

    # Verificar dependencias
    if not check_dependencies():
        print("\n❌ Instala las dependencias antes de continuar.")
        sys.exit(1)

    # Crear configuración
    if not create_env_file():
        print("\n❌ No se pudo completar la configuración.")
        sys.exit(1)

    # Mostrar resumen
    show_summary()

    # Preguntar si iniciar el bot
    print("\n" + "=" * 50)
    start_now = input("🚀 ¿Iniciar el bot ahora? (S/n): ")

    if start_now.lower() not in ["n", "no"]:
        start_bot()
    else:
        print("\n✅ Configuración completada!")
        print("🎯 Para iniciar el bot más tarde, ejecuta: python twitch_bot.py")
        print("📖 Lee el README.md para más información")


if __name__ == "__main__":
    """Punto de entrada del script."""
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Configuración cancelada por el usuario")
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        print("📞 Si el problema persiste, revisa el README.md")
