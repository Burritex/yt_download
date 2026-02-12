from dotenv import load_dotenv
from pathlib import Path
import yt_dlp
import os


load_dotenv()

def Get_Midia(midia_type: int, url: str):
    """
    Baixa vídeo ou áudio do YouTube.

    midia_type:
        0 -> Vídeo (MP4)
        1 -> Música (MP3)
    """

    if midia_type == 0:destiny_dir = os.getenv("DESTINY_DIR_VIDEO")
    else: destiny_dir = os.getenv("DESTINY_DIR_MUSIC")
    if not destiny_dir:
        return False, "❌ DESTINY_DIR não definido no .env"

    destiny_dir = Path(destiny_dir)
    destiny_dir.mkdir(parents=True, exist_ok=True)

    base_opts = {
        'outtmpl': str(destiny_dir / '%(title)s.%(ext)s'),
        'http_headers': {
            'User-Agent': 'Mozilla/5.0'
        }
    }

    if midia_type == 0:
        ydl_opts = {
            **base_opts,
            'format': 'bv*+ba/best',
            'merge_output_format': 'mp4',
        }

    elif midia_type == 1:
        ydl_opts = {
            **base_opts,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    else:
        return False, "⚠️ Tipo de mídia inválido (0 = vídeo, 1 = música)"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

            # se for mp3, ajustar extensão
            if midia_type == 1:
                file_path = file_path.rsplit('.', 1)[0] + '.mp3'

        return True, file_path

    except Exception as err:
        return False, f"❌ Erro ao baixar mídia: {err}"
