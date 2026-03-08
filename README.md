# ytdl

Descargador interactivo de YouTube en terminal. Descarga videos en **MP4 con video + audio** usando `yt-dlp` y muestra una barra de progreso con `rich`.

## Instalación

### Homebrew (recomendado)

```bash
brew tap tu-usuario/ytdl
brew install ytdl
```

### pip

```bash
pip install ytdl
```

## Uso

```bash
ytdl
```

El programa pedirá:
1. La URL del video
2. La carpeta destino (por defecto, la carpeta actual)

Luego mostrará información del video y confirmará antes de descargar.

## Requisitos

- Python 3.9+
- **FFmpeg** instalado y en el PATH

### Instalar FFmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows
winget install Gyan.FFmpeg
```

## Licencia

MIT
