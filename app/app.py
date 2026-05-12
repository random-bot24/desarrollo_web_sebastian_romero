from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from database.db import SessionLocal
from models.models import *
from sqlalchemy import DateTime
from datetime import datetime
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    session = SessionLocal()
    miembros = session.query(Miembro).limit(5).all()

    return render_template('main2.html', miembros=miembros)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        session.refresh(nuevo_miembro)
        nuevo_id = nuevo_miembro.id
        session.close()
        return redirect(url_for("registro_actividades", id_miembro=nuevo_id))
    return render_template("register_members.html")

@app.route("/registro-actividades/<int:id_miembro>", methods=["GET", "POST"])
def registro_actividades(id_miembro):
    if request.method == "POST":
        # Captura de datos del formulario
        print("DATOS RECIBIDOS DEL FORMULARIO:", request.form)
        nombre_act = request.form.get("nombre")
        dia = request.form.get("dia")
        hora_inicio = request.form.get("hora_inicio")
        duracion = request.form.get("duracion")
        tipo = request.form.get("tipo")
        descripcion = request.form.get("descripcion")
        print("Variables capturadas ->", "Nombre:", nombre_act, "| Día:", dia, "| Hora:", hora_inicio, "| Duración:", duracion, "| Tipo:", tipo)
        # Captura de archivos (input con name="fotos" y atributo multiple)
        archivos = request.files.getlist("files")

        errores = []

        # Validaciones de servidor
        if not all([nombre_act, dia, hora_inicio, duracion, tipo]):
            errores.append("Todos los campos obligatorios deben ser completados.")
        
        if not archivos or archivos[0].filename == '':
            errores.append("Debe subir al menos una foto de la actividad.")

        if errores:
            return render_template("register_activities.html", errores=errores, id_miembro=id_miembro)

        session = SessionLocal()
        try:
            # 1. Inserción en tabla 'actividad' 
            nueva_act = Actividad(
                miembro_id=id_miembro,
                dia=dia,
                hora_inicio=hora_inicio,
                duracion=duracion,
                tipo=tipo,
                nombre=nombre_act,
                descripcion=descripcion
            )
            session.add(nueva_act)
            session.flush()  # Obtenemos el ID de la actividad para las fotos

            # 2. Procesamiento de archivos y tabla 'foto'
            for file in archivos:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Almacenamiento físico (Requisito Tarea: 0.5 punto)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)

                    # Inserción en tabla 'foto'
                    nueva_foto = Foto(
                        actividad_id=nueva_act.id,
                        ruta_archivo=filepath, # Guardamos la ruta completa o relativa según tu preferencia
                        nombre_archivo=filename # Guardamos el nombre o ruta relativa
                    )
                    session.add(nueva_foto)

            session.commit()
            # Al finalizar, volver a portada con mensaje de éxito
            return redirect(url_for("index", msg="Registro completado con éxito"))

        except Exception as e:
            session.rollback()
            errores.append(f"Error en el servidor: {str(e)}")
            return render_template("register_activities.html", errores=errores, id_miembro=id_miembro)
        finally:
            session.close()

    return render_template("register_activities.html", id_miembro=id_miembro)

# Obtener miembros mediante paginacion
@app.route("/listado_miembros/", methods=["GET"])
def listado_miembros(page=1):
    page = request.args.get('page', 1, type=int)
    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    miembros = get_members()
    miembros_paginated = miembros[start:end]
    total_pages = (len(miembros) + per_page - 1) // per_page

    return render_template("list_members2.html", miembros_paginated=miembros_paginated, total_pages=total_pages, page=page)


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


