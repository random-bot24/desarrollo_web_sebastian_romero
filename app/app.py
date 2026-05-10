from flask import Flask, request, render_template
from database.db import SessionLocal
from models.models import *

UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main2.html')

#@app.route("/registro", methods=["GET", "POST"])
#def registro():
#    if request.method == "POST":
#        pass

@app.route("/listado_miembros", methods=["GET"])
def listado_miembros():
    miembros = get_members()
    return render_template("list_members2.html", miembros=miembros)


@app.route("/estadisticas", methods=["GET"])
def estadisticas():
    return render_template("statistics2.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000)


