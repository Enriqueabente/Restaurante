from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Definición de la clase Reserva
class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)
    personas = db.Column(db.Integer)
    nombre_cliente = db.Column(db.String(100))
