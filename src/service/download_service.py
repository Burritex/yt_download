from pathlib import Path
from models import Midia, MidiaFormat
import yt_dlp
from flask import current_app


class DownloadService:
    def __init__(self):
        self.__format_config = {
            MidiaFormat.VIDEO: {
                "env": "DESTINY_DIR_VIDEO",
                "format": "bv*+ba/best",
                "merge_output_format": "mp4"
            },
            MidiaFormat.MUSIC: {
                "env": "DESTINY_DIR_MUSIC",
                "format": "bestaudio/best",
                "postprocessors": [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': "mp3",
                    'preferredquality': '192',
                }]
            }
        }
    
    @property
    def format_config(self) -> dict:
        return self.__format_config
    

    def _get_opts(self, destiny_dir: str, format: str):
        ydl_opts = {
            "outtmpl": {
                "default": str(destiny_dir / "%(title).200B.%(ext)s")
            },
            "http_headers": {"User-Agent": "Mozilla/5.0"},
            "overwrites": False,
            "windowsfilenames": True,  # sanitização extra
            "format": format,
            "trim_file_name": 200,
        }
        return ydl_opts

    def get_midia(self, midia_format: MidiaFormat, url: str) -> Midia:
        config = self.format_config.get(midia_format)

        if not config:
            return Midia(status=False, error_msg="⚠️ Formato inválido")

        destiny_dir = current_app.config.get(config['env'])
        if not destiny_dir:
            return Midia(
                status=False,
                error_msg=f"❌ Variável {config['env']} não definida no .env"
            )

        destiny_dir = Path(destiny_dir)
        destiny_dir.mkdir(parents=True, exist_ok=True)
        ydl_opts = self._get_opts(destiny_dir, config['format'])

        # adiciona opções específicas dinamicamente
        if "merge_output_format" in config:
            ydl_opts["merge_output_format"] = config["merge_output_format"]

        if "postprocessors" in config:
            ydl_opts["postprocessors"] = config["postprocessors"]

        try:
            midia_exist = self._check_midia(ydl_opts, url, midia_format)
            
            if not midia_exist[0]:
                self._download_midia(url, ydl_opts)

            return Midia(status=True, name=midia_exist[1], midia_format=midia_format) 

        except Exception as err:
            return Midia(
                status=False,
                error_msg=f"❌ Erro ao baixar mídia: {err}"
            )
        
    def _check_midia(self, ydl_opts, url, midia_format):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 🔹 extrai info sem baixar
            info = ydl.extract_info(url, download=False)
            file_path = ydl.prepare_filename(info)

            # se for áudio, ajusta extensão final
            if midia_format == MidiaFormat.MUSIC:
                file_path = file_path.rsplit(".", 1)[0] + f".{midia_format.value}"

            file_path = Path(file_path)
            _midia_name = file_path.name

            # 🔹 verifica se já existe
            if file_path.exists():
                return True, _midia_name
            else:
                return False, _midia_name

    def _download_midia(self, url, ydl_opts):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
