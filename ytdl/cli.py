import os
import shutil
import sys
from pathlib import Path

import yt_dlp
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)

console = Console()


def ffmpeg_instalado() -> bool:
    return shutil.which("ffmpeg") is not None


def pedir_url() -> str:
    console.print(
        Panel.fit(
            "[bold cyan]Descargador de YouTube[/bold cyan]\n"
            "[white]Descarga en MP4 con video + audio[/white]",
            border_style="cyan",
        )
    )

    while True:
        url = Prompt.ask("[bold green]Pega la URL[/bold green]").strip()
        if url.startswith("http://") or url.startswith("https://"):
            return url
        console.print("[bold red]URL no válida.[/bold red]")


def pedir_destino() -> str:
    actual = str(Path.cwd())
    usar_actual = Confirm.ask(
        f"[bold yellow]¿Guardar en la carpeta actual?[/bold yellow]\n[white]{actual}[/white]",
        default=True,
    )
    if usar_actual:
        return actual

    while True:
        ruta = Prompt.ask("[bold green]Escribe la carpeta destino[/bold green]").strip()
        if os.path.isdir(ruta):
            return ruta
        console.print("[bold red]Esa carpeta no existe.[/bold red]")


def obtener_info(url: str) -> dict:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        return ydl.extract_info(url, download=False)


def descargar(url: str, destino: str) -> None:
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TextColumn("[bold yellow]{task.percentage:>5.1f}%"),
        TimeRemainingColumn(),
        console=console,
    )

    task_id = None

    def hook(d):
        nonlocal task_id

        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            done = d.get("downloaded_bytes", 0)

            if task_id is None:
                task_id = progress.add_task("Descargando", total=total if total > 0 else 100)

            if total > 0:
                progress.update(task_id, completed=done, total=total)
            else:
                progress.update(task_id, completed=min(done, 100), total=100)

        elif d["status"] == "finished" and task_id is not None:
            progress.update(task_id, description="Uniendo video y audio")

    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(destino, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [hook],
    }

    with progress:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


def main():
    try:
        if not ffmpeg_instalado():
            console.print(
                Panel(
                    "[bold red]FFmpeg no está instalado o no está en el PATH.[/bold red]\n\n"
                    "[white]Sin FFmpeg, YouTube muchas veces solo descarga una parte o no puede unir video y audio.[/white]\n\n"
                    "[bold yellow]En macOS:[/bold yellow] brew install ffmpeg\n"
                    "[bold yellow]En Windows:[/bold yellow] winget install Gyan.FFmpeg",
                    title="Falta FFmpeg",
                    border_style="red",
                )
            )
            sys.exit(1)

        url = pedir_url()
        destino = pedir_destino()

        console.print("\n[bold blue]Obteniendo información...[/bold blue]")
        info = obtener_info(url)

        titulo = info.get("title", "Desconocido")
        canal = info.get("uploader", "Desconocido")
        dur = info.get("duration")
        dur_txt = f"{dur // 60}:{dur % 60:02d}" if isinstance(dur, int) else "Desconocida"

        console.print(
            Panel(
                f"[bold white]Título:[/bold white] {titulo}\n"
                f"[bold white]Canal:[/bold white] {canal}\n"
                f"[bold white]Duración:[/bold white] {dur_txt}\n"
                f"[bold white]Destino:[/bold white] {destino}",
                title="[bold green]Video encontrado[/bold green]",
                border_style="green",
            )
        )

        if not Confirm.ask("[bold yellow]¿Descargar este video?[/bold yellow]", default=True):
            console.print("[bold red]Cancelado.[/bold red]")
            return

        descargar(url, destino)

        console.print(
            Panel.fit(
                "[bold green]Descarga completada.[/bold green]\n"
                "[white]Se guardó como MP4 con video + audio.[/white]",
                border_style="green",
            )
        )

    except KeyboardInterrupt:
        console.print("\n[bold red]Cancelado por el usuario.[/bold red]")
    except Exception as e:
        console.print(Panel.fit(f"[bold red]Error:[/bold red] {e}", border_style="red"))
