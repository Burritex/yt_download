from service import DownloadService
from models import MidiaFormat, Midia
from urllib.parse import urlparse


def controller(midia_type: int, url: str) -> Midia:
    """
    Docstring for controller
    Data validation
    """
    if midia_type not in (0, 1):
        return Midia(status=False, error_msg='midia_type invalida!')
    
    if not isinstance(url, str) or not url:
        return Midia(status=False, error_msg="URL inválida")

    host = urlparse(url).netloc.lower()
    if host not in ("youtube.com", "www.youtube.com", "youtu.be"):
        return Midia(status=False, error_msg="Somente links do YouTube são permitidos")

    if "youtube.com" not in url and "youtu.be" not in url:
        return Midia(status=False, error_msg="Somente links do YouTube são permitidos")

    if '&' in url:
        url = url.split('&')[0]
    
    if 'list=' in url:
        return Midia(status=False, error_msg="Não é permitido baixar playlist!")

    if midia_type == 0:
        return DownloadService().get_midia(MidiaFormat.VIDEO, url)
    else:
        return DownloadService().get_midia(MidiaFormat.MUSIC, url)
