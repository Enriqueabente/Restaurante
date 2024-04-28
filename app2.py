from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Código de tu aplicación Flask...


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)
    personas = db.Column(db.Integer)
    nombre_cliente = db.Column(db.String(100))


CAPACIDAD_RESTAURANTE = 20  # Capacidad total de mesas del restaurante

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        fecha_str = request.form['fecha']
        print("Fecha recibida del formulario:", fecha_str)  # Agrega esta línea para verificar fecha_str
        fecha = request.form["fecha"]
        hora = request.form["hora"]
        personas = int(request.form["personas"])
        nombre_cliente = request.form["nombre"]

        # Convertir la cadena de fecha en un objeto de fecha
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora_str = request.form['hora']

        # Convertir la cadena de hora en un objeto de tiempo de Python
        hora = datetime.strptime(hora_str, '%H:%M').time()

        # Verificar la disponibilidad de mesas
        reservas = Reserva.query.filter_by(fecha=fecha, hora=hora).all()
        total_personas_reservadas = sum(reserva.personas for reserva in reservas)
        mesas_disponibles = CAPACIDAD_RESTAURANTE - total_personas_reservadas

        
        # Hacer reserva
        if personas <= mesas_disponibles:
            nueva_reserva = Reserva(fecha=fecha, hora=hora, personas=personas, nombre_cliente=nombre_cliente)
            db.session.add(nueva_reserva)
            db.session.commit()

            return redirect(url_for("reserva_exitosa"))
        else:
            # Mostrar un mensaje de error si no hay mesas disponibles
            error_message = f"No hay suficientes mesas disponibles para {personas} personas en esa fecha y hora."
            return redirect(url_for("error_reserva"))
    return render_template("index.html")

@app.route("/ver_reservas")
def ver_reservas():
    reservas = Reserva.query.all()
    return render_template("ver_reservas.html", reservas=reservas)

@app.route('/agregar_reserva', methods=['POST'])
def agregar_reserva():
    if request.method == 'POST':
        # Obtener los datos del formulario
        fecha_str = request.form['fecha']
        hora_str = request.form['hora']
        personas = request.form['personas']
        nombre_cliente = request.form['nombre']

        # Convertir las cadenas de fecha y hora en objetos de Python
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora_obj = datetime.strptime(hora_str, '%H:%M').time()

        # Crear una nueva reserva y agregarla a la base de datos
        nueva_reserva = Reserva(fecha=fecha_obj, hora=hora_obj, personas=personas, nombre_cliente=nombre_cliente)
        db.session.add(nueva_reserva)
        db.session.commit()

        # Redirigir a la página de ver reservas después de agregar la reserva
        return redirect(url_for('ver_reservas'))


@app.route("/reserva_exitosa")
def reserva_exitosa():
    return render_template("reserva_exitosa.html")

@app.route("/error_reserva")
def error_reserva():
    return render_template("error_reserva.html")

# Crear una ruta para modificar una reserva

@app.route("/modificar_reserva/<int:id>", methods=["GET", "POST"])
def modificar_reserva(id):
    reserva = Reserva.query.get_or_404(id)

    if request.method == "POST":
        reserva.fecha = request.form["fecha"]
        reserva.hora = request.form["hora"]
        reserva.personas = request.form["personas"]
        reserva.nombre_cliente = request.form["nombre"]

        db.session.commit()

        return redirect(url_for("ver_reservas"))

    return render_template("modificar_reserva.html", reserva=reserva)

@app.route("/cancelar_reserva/<int:id>", methods=["GET", "POST"])
def cancelar_reserva(id):
    reserva = Reserva.query.get_or_404(id)

    if request.method == "POST":
        db.session.delete(reserva)
        db.session.commit()

        return redirect(url_for("ver_reservas"))

    return render_template("cancelar_reserva.html", reserva=reserva)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)