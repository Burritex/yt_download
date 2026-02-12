from flask import Flask, render_template, request, send_file, abort
from controler import Controler
import os


app = Flask(__name__, template_folder='templates', static_folder='static')
result = ''

@app.route("/", methods=['GET'])
def pg_inicial():
    return render_template("pg_inicial.html")


@app.route("/", methods=['POST'])
def pg_inicial_post():
    ok, data = process_form()

    if not ok:
        return render_template("pg_resposta.html", resp={
            "status": False,
            "msg": data
        })

    url, midia = data
    status, result = Controler(midia, url)

    if not status:
        return render_template("pg_resposta.html", resp={
            "status": False,
            "msg": result
        })

    if not os.path.exists(result):
        abort(404)

    return send_file(result, as_attachment=True)


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


if __name__ == "__main__":
   app.run(host="0.0.0.0", port=2159, debug=True)
