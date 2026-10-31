"""Capa de presentacion: rutas y vistas."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.business import services

bp = Blueprint("main", __name__, template_folder="templates")


@bp.route("/")
def index():
    return render_template("matches.html", matches=services.list_matches())


@bp.route("/predictions", methods=["GET", "POST"])
def predictions():
    if request.method == "POST":
        try:
            services.register_prediction(
                int(request.form["match_id"]),
                request.form["winner"],
                int(request.form["home_score"]),
                int(request.form["away_score"]),
            )
            flash("Prediccion guardada", "ok")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for("main.index"))
    return render_template("predictions.html", predictions=services.list_predictions())
