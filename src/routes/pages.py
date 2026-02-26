from flask import Blueprint, request, render_template, redirect, send_file, current_app, make_response
from service import CookieService
from utils import process_form
from controllers import controller
from pathlib import Path


app_routes = Blueprint("app_routes", __name__, static_folder="static", template_folder="templates")

# Pagina Inicial
@app_routes.route("/", methods=['GET', 'POST'])
def pg_inicial():
    if request.method == 'GET':
        response = make_response(render_template("pg_inicial.html"))
        response = CookieService().clear_all(response)
        return response

    elif request.method == 'POST':
        ok, data = process_form()

        if not ok:
            return render_template("pg_resposta.html", resp={
                "error_msg": data,
                "status": False
            })
    
        url, midia = data
        request_result = controller(midia, url)

        if not request_result.status:
            return render_template("pg_resposta.html", resp={
                "error_msg": request_result.error_msg,
                "status": request_result.status
            })
        
        return CookieService().set({
            "status": request_result.status,
            "name": request_result.name,
            "midia_format": request_result.midia_format,
            "error_msg": request_result.error_msg
        })        
        
    else:
        return "{ Only 'GET' and 'POST methods are allowed ! }"

# Pagina resposta
@app_routes.route("/resp", methods=['GET', 'POST'])
def pg_resp():
    cookies = CookieService().get_all()
    if not cookies['status']:
        return redirect("/")

    if request.method == 'GET':
        return render_template("pg_resposta.html", resp=cookies)
    
    elif request.method == 'POST':
        if cookies['midia_format'] == "mp4":
            destiny_dir = current_app.config.get("DESTINY_DIR_VIDEO")
        else:
            destiny_dir = current_app.config.get("DESTINY_DIR_MUSIC")

        destiny_dir = Path(destiny_dir) / f"{cookies['name']}"
        return send_file(destiny_dir, as_attachment=True)

    else:
        return "{ Only 'GET' and 'POST methods are allowed ! }"
