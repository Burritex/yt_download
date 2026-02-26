from flask import request


def process_form():
    url = request.form.get("yt_url", "").strip()
    midia = request.form.get("rd_midia")

    if not url:
        return False, "URL não informada"

    try:
        midia = int(midia)
    except (TypeError, ValueError):
        return False, "Tipo de mídia inválido"

    return True, (url, midia)
