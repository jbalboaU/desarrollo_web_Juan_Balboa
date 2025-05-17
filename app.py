from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import os
import pymysql.cursors
from werkzeug.utils import secure_filename
from datetime import datetime
from database.db import get_connection

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.secret_key = 'ZGVzYXJyb2xsb19fd2Vi'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.resplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT a.dia_hora_inicio, a.dia_hora_termino, c.nombre AS comuna, sector,
                t.tema,
                (
                    SELECT ruta_archivo
                    FROM foto
                    WHERE actividad_id = a.id
                    ORDER BY id ASC
                    LIMIT 1
                ) AS ruta_foto
        FROM actividad a
        JOIN comuna c ON a.comuna_id = c.id
        LEFT JOIN actividad_tema t ON a.id = t.actividad_id
        ORDER BY a.dia_hora_inicio DESC
        LIMIT 5
    """)

    actividades = cursor.fetchall()
    conn.close()
    return render_template('html/index.html', actividades = actividades)


@app.route('/agregar', methods = ['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        errores = []

        region = request.form.get('region')
        comuna = request.form.get('comuna')
        sector = request.form.get('sector')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular', '')
        inicio = request.form.get('inicio')
        termino = request.form.get('termino')
        descripcion = request.form.get('descripcion')
        tema = request.form.get('tema')
        descripcion_tema = request.form.get('descripcion_tema')
        medio = request.form.get('contactar_por')
        identificador = request.form.get('contacto_id')
        archivos = request.files.getlist('fotos')

        if not region or not comuna or not nombre or not email or not inicio:
            errores.append("Faltan campos obligatorios.")
        if not tema:
            errores.append("Debe seleccionar un tema.")
        if not archivos or archivos[0].filename == '':
            errores.append("Debe seleccionar al menos un tema.")
        if len(archivos) > 5:
            errores.append("Máximo 5 fotos permitidas.")

        for f in archivos:
            if not allowed_file(f.filename):
                errores.append("Formato de archivo no permitido: " + f.filename)
        
        if errores:
            flash(', '.join(errores))
            return render_template('html/add.html')
        
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO actividad (comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (comuna, sector, nombre, email, celular, inicio, termino, descripcion))
        actividad_id = cursor.lastrowid

        cursor.execute("INSERT INTO actividad_tema (actividad_id, tema) VALUES (%s, %s)", (actividad_id, tema))

        if medio and identificador:
            cursor.execute(
                "INSERT INTO contactar_por (actividad_id, medio, identificador) VALUES(%s, %s, %s)",
                (actividad_id, medio, identificador)
            )
        
    
        for f in archivos:
            filename = secure_filename(f.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(path)
            cursor.execute(
                "INSERT INTO archivo (actividad_id, archivo_url) VALUES (%s, %s)", 
                (actividad_id, f"uploads/{filename}")
            )

        conn.commit()
        conn.close()
        flash("¡Actividad registrada con éxito!")
        return redirect(url_for('index'))
    
    return render_template('html/add.html')


@app.route('/actividades')
def actividades():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM actividad")
    actividades_raw = cursor.fetchall()

    actividades = []
    for act in actividades_raw:
        act_id = act["id"]
        cursor.execute("SELECT tema FROM actividad_tema WHERE actividad_id = %s", (act_id,))
        temas = [t["tema"] for t in cursor.fetchall()]
        cursor.execute("SELECT archivo_url FROM archivo WHERE actividad_id = %s", (act_id,))
        fotos = [os.path.basename(f["archivo_url"]) for f in cursor.fetchall()]

        actividades.append({
            "inicio": act["inicio"],
            "termino": act["termino"],
            "comuna": act["comuna"],
            "sector": act["sector"],
            "nombre": act["nombre_organizador"],
            "temas": temas,
            "fotos": fotos
        })

    conn.close()
    return render_template('view.html', actividades=actividades)

@app.route('/actividad <int:id>')
def detalle_actividad(id):
    conn = get_connection
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM actividad WHERE id = %s", (id,))
    actividad = cursor.fetchone

    cursor.execute("SELECT tema FROM actividad_tema WHERE actividad_id = %s", (id,))
    temas = [row['tema'] for row in cursor.fetchall()]

    cursor.execute("SELECT medio, identificador FROM contactar_por WHERE actividad_id = %s", (id,))
    contactos = cursor.fetchall()

    cursor.execute("SELECT archivo_url FROM archivo WHERE actividad_id = %s", (id,))
    archivos = cursor.fetchall()

    conn.close()

    return render_template('detalle.html', actividad=actividad, temas=temas, contactos=contactos, archivos=archivos)



@app.route('/estadisticas')
def estadisticas():
    return

if __name__ == '__main__':
    app.run(debug=True)

