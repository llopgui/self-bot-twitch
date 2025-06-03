# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir al **Self Bot Twitch**! Este documento te guiará a través del proceso.

## 🚀 Cómo Contribuir

### 🐛 Reportar Bugs

Si encuentras un bug, por favor:

1. **Verifica** que no haya sido reportado antes en [Issues](https://github.com/llopgui/self-bot-twitch/issues)
2. **Crea un nuevo issue** con:
   - 📝 Descripción detallada del problema
   - 🔄 Pasos para reproducir el bug
   - 💻 Tu sistema operativo y versión de Python
   - 📋 Logs relevantes (si aplica)

### ✨ Sugerir Nuevas Características

Para sugerir mejoras:

1. **Abre un issue** con la etiqueta "enhancement"
2. **Describe claramente** la característica propuesta
3. **Explica por qué** sería útil para el proyecto

### 🔧 Contribuir con Código

#### 1. Fork y Clona

```bash
# Fork el repositorio en GitHub, luego:
git clone https://github.com/tu-usuario/self-bot-twitch.git
cd self-bot-twitch
```

#### 2. Configura el Entorno

```bash
# Crea un entorno virtual
python -m venv venv

# Actívalo
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instala dependencias
pip install -r requirements.txt
```

#### 3. Crea una Rama

```bash
git checkout -b feature/mi-nueva-caracteristica
# o
git checkout -b fix/arreglo-del-bug
```

#### 4. Realiza los Cambios

- ✅ **Sigue el estilo de código** existente
- ✅ **Añade comentarios** y docstrings en español
- ✅ **Actualiza documentación** si es necesario
- ✅ **Prueba tu código** antes de hacer commit

#### 5. Commit y Push

```bash
git add .
git commit -m "feat: descripción clara del cambio"
git push origin feature/mi-nueva-caracteristica
```

#### 6. Crea Pull Request

1. Ve a GitHub y crea un **Pull Request**
2. **Describe los cambios** realizados
3. **Referencia issues** relacionados (si aplica)

## 📋 Estándares de Código

### 🐍 Python

- **Estilo**: Seguir PEP 8
- **Docstrings**: En español, formato Google
- **Nombres**: Variables y funciones en español
- **Comentarios**: Claros y en español

### 📝 Ejemplo de Docstring

```python
def mi_funcion(parametro: str) -> bool:
    """
    Descripción breve de la función.

    Args:
        parametro (str): Descripción del parámetro

    Returns:
        bool: Descripción del valor de retorno

    Raises:
        ValueError: Cuando el parámetro es inválido
    """
    # Implementación aquí
    pass
```

### 🎯 Convenciones de Commit

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva característica
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Formato, espacios en blanco, etc.
- `refactor:` Refactorización de código
- `test:` Añadir o modificar tests
- `chore:` Mantenimiento

### 📁 Estructura de Archivos

```
self-bot-twitch/
├── twitch_bot.py          # Bot principal
├── start.py               # Script de configuración
├── config.py              # Gestión de configuración
├── requirements.txt       # Dependencias
├── README.md              # Documentación principal
├── CONTRIBUTING.md        # Esta guía
├── LICENSE                # Licencia del proyecto
└── .gitignore            # Archivos ignorados
```

## 🧪 Testing

Antes de hacer commit:

1. **Prueba el bot** en un entorno real
2. **Verifica que no hay errores** en los logs
3. **Asegúrate** de que las nuevas características funcionen
4. **Revisa** que no rompas funcionalidades existentes

## 📚 Tipos de Contribuciones Bienvenidas

### 🎭 **Contenido**

- Nuevos chistes sobre Plutón
- Más factos científicos anti-Plutón
- Mejores patrones de detección

### 🛠️ **Características Técnicas**

- Mejoras en el sistema de logging
- Optimizaciones de rendimiento
- Mejor manejo de errores

### 📖 **Documentación**

- Mejoras en el README
- Ejemplos de uso adicionales
- Guías de solución de problemas

### 🎨 **UI/UX**

- Mejoras en la configuración interactiva
- Mejor presentación de mensajes
- Banners más atractivos

## 🤔 ¿Necesitas Ayuda?

- 💬 **Discord/Comunidad**: Próximamente
- 📧 **Email**: Revisa el perfil de [@llopgui](https://github.com/llopgui)
- 🐛 **Issues**: Para preguntas técnicas específicas

## 📄 Licencia

Al contribuir, aceptas que tus contribuciones serán licenciadas bajo la misma licencia [CC BY-NC-SA 4.0](LICENSE) del proyecto.

## 🙏 Reconocimientos

Todos los contribuidores serán mencionados en:

- 📋 Archivo CONTRIBUTORS.md
- 🌟 README principal
- 📦 Releases del proyecto

---

**¡Gracias por hacer que Self Bot Twitch sea aún mejor!** 🚀

*Recuerda: ¡cada contribución cuenta, sin importar cuán pequeña sea!*
