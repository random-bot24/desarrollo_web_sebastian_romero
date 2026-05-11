from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from database.db import SessionLocal
from models.models import *
from sqlalchemy import DateTime
from datetime import datetime

UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    session = SessionLocal()
    miembros = session.query(Miembro).limit(5).all()

    return render_template('main2.html', miembros=miembros)

@app.route("/registro_miembro", methods=["GET", "POST"])
def registro_miembro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        telefono = request.form["phone"]
        comuna_id = request.form["Comuna"]
        errores = []

        if not nombre or not email:
            errores.append("Todos los campos son obligatorios.")
        if errores:
            return render_template("register_members.html", errores=errores, nombre=nombre, email=email)
        
        session = SessionLocal()
        nuevo_miembro = Miembro(nombre=nombre, email=email, telefono=telefono, fecha_registro=datetime.now().date(), comuna_id=comuna_id)
        session.add(nuevo_miembro)
        session.commit()
        session.close()
        return redirect(url_for("index"))
    return render_template("register_members.html")

@app.route("/registro-actividades/<int:id_miembro>", methods=["GET","POST"])
def registro_actividades(id_miembro):
    if request.method == "POST":
        actividad = request.form["actividad"]
        fecha = request.form["fecha"]
        errores = []

        if not actividad or not fecha:
            errores.append("Todos los campos son obligatorios.")
        if errores:
            return render_template("register_activities.html", errores=errores, actividad=actividad, fecha=fecha)
        
        session = SessionLocal()
        nueva_actividad = Actividad(id_miembro=id_miembro, actividad=actividad, fecha=fecha)
        session.add(nueva_actividad)
        session.commit()
        session.close()
        return redirect(url_for("index"))


@app.route("/listado_miembros", methods=["GET"])
def listado_miembros():
    miembros = get_members()
    return render_template("list_members2.html", miembros=miembros)


@app.route("/estadisticas", methods=["GET"])
def estadisticas():
    return render_template("statistics2.html")


"""
#posible validacion con ajax en el futuro, lo dejo comentado por ahora
@app.route("/validate-registration",methods=["POST"])
def validate_registration():
    if request.method == "POST":
        data = request.get_json()
        member = Miembro.query.filter_by(email=data["email"]).first()

        if member:
            return jsonify({"status": "success", "message": "Validación exitosa"})
        else:
            return jsonify({"status": "error", "message": "Validación fallida"})
"""
            
if __name__ == '__main__':
    app.run(debug=True, port=5000)


