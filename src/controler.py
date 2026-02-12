from service import Get_Midia


def Controler(midia_type: int, url: str):
    """
    Docstring for Controler
    Data validation
    """
    if not midia_type in (0, 1):
        return False, 'midia_type invalida'

    if not url.startswith(("http://", "https://")):
        return False, "URL inválida"

    if "youtube.com" not in url and "youtu.be" not in url:
      return False, "Somente links do YouTube são permitidos"

    if '&' in url:
        url = url.split('&')[0]
    
    if 'list=' in url:
        return False, "Não é permitido baixar playlist!"

    return Get_Midia(midia_type, url)
