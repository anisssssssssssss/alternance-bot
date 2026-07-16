from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
from flask import render_template

app = Flask(__name__)

import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///criteres.db")

# Render fournit parfois l'URL avec "postgres://", mais SQLAlchemy attend "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL


db = SQLAlchemy(app)


class Critere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mots_cles = db.Column(db.String(500))       # séparés par des virgules
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    radius = db.Column(db.Integer)
    rome_code = db.Column(db.String(10))
    target_diploma_level = db.Column(db.String(10))

@app.route("/criteres", methods=["GET"])
def get_criteres():
    critere = Critere.query.first()  # on ne gère qu'un seul jeu de critères pour l'instant
    
    if critere is None:
        return jsonify({"message": "Aucun critère configuré"}), 404
    
    return jsonify({
        "mots_cles": critere.mots_cles.split(","),
        "latitude": critere.latitude,
        "longitude": critere.longitude,
        "radius": critere.radius,
        "rome_code": critere.rome_code,
        "target_diploma_level": critere.target_diploma_level
    })


@app.route("/criteres", methods=["POST"])
def set_criteres():
    data = request.json  # récupère les données envoyées en JSON
    
    critere = Critere.query.first()
    
    if critere is None:
        critere = Critere()
        db.session.add(critere)
    
    critere.mots_cles = ",".join(data["mots_cles"])
    critere.latitude = data["latitude"]
    critere.longitude = data["longitude"]
    critere.radius = data["radius"]
    critere.rome_code = data["rome_code"]
    critere.target_diploma_level = data["target_diploma_level"]
    
    db.session.commit()
    
    return jsonify({"message": "Critères mis à jour"}), 200

@app.route("/")
def accueil():
    return render_template("index.html")


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)