from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from database.db import SessionLocal
from models.models import *
from sqlalchemy import DateTime, func
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os

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
    actividades = get_activities()

    return render_template("list_members2.html", miembros_paginated=miembros_paginated, total_pages=total_pages, page=page, actividades=actividades)


@app.route("/estadisticas", methods=["GET"])
def estadisticas():
    return render_template("statistics2.html")

@app.route("/actividad/<int:id>", methods=["GET", "POST"])
def ver_actividad_miembro(id):
    miembro =  get_member_by_id(id)
    actividades = get_activities_by_member_id(id)
    return render_template("member_activities.html", actividades=actividades, miembro=miembro)

# Numero de registros por dia para el grafico con AJAX
@app.route("/get-register-per-day", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def get_register_per_day():
    session = SessionLocal()
    results = session.query(Miembro.fecha_registro, func.count(Miembro.id)).group_by(Miembro.fecha_registro).all() 
    data = [{ "fecha": str(fecha), "cantidad": cantidad} for fecha, cantidad in results]
    session.close()
    return jsonify(data)

#Numero de actividades por tipo para el grafico de torta con AJAX
@app.route("/get-activities-per-type", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def get_activities_per_type():
    session = SessionLocal()
    results = session.query(Actividad.tipo, func.count(Actividad.id)).group_by(Actividad.tipo).all()
    data = [{"tipo": tipo, "cantidad": cantidad} for tipo, cantidad in results]
    session.close()
    return jsonify(data)

# enviar comentarios en un json con API 
@app.route("/actividades/<int:actividad_id>", methods=["GET"])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def comments(actividad_id):
    session = SessionLocal()
    try:
        actividad = session.get(Actividad, actividad_id)
        comentarios = session.query(Comentario).filter(Comentario.actividad_id == actividad_id).all()
        if not actividad:
            return jsonify({"error": "Actividad no encontrada"}), 404
        lista_comentarios=[]
        for comentario in comentarios:
            lista_comentarios.append({
                "nombre": comentario.nombre,
                "texto": comentario.texto,
                "fecha": comentario.fecha
            })
        return jsonify(lista_comentarios)
    finally:
        session.close()

#POST del comentario con ajax y json (validacion y creacion comentario) y lo guarda
@app.route("/comentario/<int:actividad_id>", methods=["POST"])
def cargar_comentario(actividad_id):
    get_data= request.get_json()
    nombre = get_data.get('nombre','').strip()
    texto = get_data.get('texto','').strip()
    if not (3 <= len(nombre) <= 50):
        return jsonify({"error": "El nombre debe tener entre 3 y 50 caracteres"}), 400
    if not (5 <= len(texto) <= 500):
        return jsonify({"error": "El comentario debe tener entre 5 y 500 caracteres"}), 400
    session = SessionLocal()
    try:
        new_comment = Comentario(actividad_id=actividad_id, texto=texto, nombre=nombre, fecha=datetime.now())
        session.add(new_comment)
        session.commit()
        return jsonify({"mensaje" :"Comentario agregado exitosamente"}), 201

    except Exception as e:
        session.rollback()
        return jsonify({"error": "Error al agregar comentario"}), 500
    
    finally:
        session.close()
    
    

     
if __name__ == '__main__':
    app.run(debug=True, port=5000)


