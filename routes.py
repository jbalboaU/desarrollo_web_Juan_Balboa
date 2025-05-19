from flask import render_template, request, url_for, redirect, flash, current_app
import re
from models import *
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import uuid
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def register_routes(app, db):
    
    @app.route('/')
    def index():
        actividades = (
            Actividad.query.order_by(Actividad.dia_hora_inicio.desc()).limit(5).all()
        )
        return render_template('index.html', actividades = actividades)
    
    @app.route('/agregar', methods=['GET', 'POST'])
    def agregar():
        if request.method == 'GET':
            regiones=Region.query.all()
            comunas=Comuna.query.all()
            return render_template('add.html', regiones=regiones, comunas=comunas)
        elif request.method == 'POST':
            print('hola')
            try:
                region = int(request.form.get("region"))
                comuna = int(request.form.get("comuna"))
                nombre = request.form.get("nombre")
                email = request.form.get("email")
                celular = request.form.get("celular")
                contactar_por = request.form.getlist("contactar_por[]")
                contacto_id = request.form.get("contacto_id")
                inicio = request.form.get("inicio")
                termino = request.form.get("termino")
                descripcion = request.form.get("descripcion")
                tema = request.form.getlist("tema[]")
                descripcion_tema = request.form.get("descripcion_tema", "").strip()
                sector = request.form.get("sector")
                fotos = request.files.getlist("fotos[]")

                errors = []

                if not region or not comuna or not nombre or not email or not inicio or not tema:
                    errors.append("Faltan campos obligatorios.")
                if sector and len(sector) > 100:
                    errors.append("El atributo sector tiene demasiados carácteres.")
                if len(nombre) > 200:
                    errors.append("Nombre demasiado largo.")
                if len(email)>100:
                    errors.append("El email es demasiado largo.")
                email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
                if not re.match(email_regex, email):
                    errors.append("El formato del email no es válido.")
                celular_regex =r'^\+\d{7,15}$'
                if not re.match(celular_regex, celular):
                    errors.append("El formato del número no es válido.")
                if contactar_por and (not contacto_id or len(contacto_id) < 4 or len(contacto_id) > 50):
                    errors.append("EL campo ID/URL de contacto no es válido.")
                if "otro" in tema and (not descripcion_tema or len(descripcion_tema)<3 or len(descripcion_tema)>15):
                    errors.append("Debe ingresar una descripción válida para el tema.")
                try:
                    inicio_dt = datetime.strptime(inicio.strip(), "%Y-%m-%dT%H:%M")
                except (ValueError, AttributeError):
                    errors.append("El campo 'inicio' debe tener el formato año-mes-día hora:minuto.")

                if termino:
                    try:
                        termino_dt = datetime.strptime(termino.strip(), "%Y-%m-%dT%H:%M")
                        if 'inicio_dt' in locals() and termino_dt <= inicio_dt:
                            errors.append("La fecha de término debe ser posterior a la de inicio.")
                    except (ValueError, AttributeError):
                        errors.append("El campo 'término' debe tener el formato año-mes-día hora:minuto.")
                
                if len(fotos) == 0 or len(fotos) > 5:
                    errors.append("Debe subir entre 1 y 5 fotos.")
                else:
                    for foto in fotos:
                        if foto.filename=="":
                            errors.append("Una de las fotos no tiene nombre de archivo")
                        elif not allowed_file(foto.filename):
                            errors.append(f"Archivo no permitido: {foto.filename}")
                
                if errors:
                    regiones = Region.query.all()
                    comunas = Comuna.query.all()
                    return render_template('add.html', regiones=regiones, comunas=comunas, errors=errors)
                
                nueva_actividad = Actividad(
                    comuna_id=comuna,
                    sector=sector,
                    nombre=nombre,
                    email=email,
                    celular=celular,
                    dia_hora_inicio=inicio_dt,
                    dia_hora_termino=termino_dt if termino else None,
                    descripcion=descripcion
                )
                db.session.add(nueva_actividad)
                db.session.commit()
                

                for medio in contactar_por:
                    nuevo_contacto = ContactarPor(
                        actividad_id=nueva_actividad.id,
                        nombre=medio,
                        identificador=contacto_id
                    )
                    db.session.add(nuevo_contacto)


                for t in tema:
                    nuevo_tema = ActividadTema(
                        actividad_id=nueva_actividad.id,
                        tema=t,
                        glosa_otro=descripcion_tema if t == 'otro' else None
                    )
                    db.session.add(nuevo_tema)

                for foto in fotos:
                    filename=secure_filename(foto.filename)
                    relative_folder = 'uploads'
                    filepath=os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    foto.save(filepath)
                    ruta_relativa = f"uploads/{filename}"
                    
                    nueva_foto=Foto(
                        actividad_id=nueva_actividad.id,
                        ruta_archivo=ruta_relativa,
                        nombre_archivo=filename
                    )  
                    db.session.add(nueva_foto)

                db.session.commit()

                flash("Hemos recibido su información, muchas gracias y suerte en su actividad", "success")
                return redirect(url_for('index'))             
                
            
            except Exception as e:
                db.session.rollback()
                regiones=Region.query.all()
                comunas =Comuna.query.all()
                return render_template('add.html', regiones=regiones, comunas=comunas, errors=[str(e)])
        
    @app.route('/listado')
    def listado():
        page = request.args.get('page', 1, type=int)
        per_page=5

        pagination = Actividad.query.order_by(Actividad.dia_hora_inicio.desc()).paginate(page=page, per_page=per_page)
        actividades = pagination.items

        return render_template('list.html', actividades=actividades, pagination = pagination)
    
    @app.route('/estadistica')
    def estadistica():
        return render_template('stats.html')
    
    @app.route('/actividad/<int:actividad_id>')
    def detalle_actividad(actividad_id):
        actividad = Actividad.query.get_or_404(actividad_id)
        return render_template('details.html', actividad=actividad)