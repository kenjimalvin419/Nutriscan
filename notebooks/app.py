import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from flask import send_from_directory


from inference import predict_muac_from_path
from calculator import classify_nutrition_status

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)
app.config["UPLOAD_FOLDER"] = UPLOAD_DIR
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXT = {"jpg", "jpeg", "png", "webp"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/assess")
def assess():
    age_years = float(request.form.get("age", 0))
    weight_kg = float(request.form.get("weight", 0))
    height_cm = float(request.form.get("height", 0))
    gender = request.form.get("gender", "")

    age_months = age_years * 12.0

    file = request.files.get("photo")
    if not file or file.filename == "":
        return "Foto wajib diupload.", 400
    if not allowed_file(file.filename):
        return "Format foto tidak didukung.", 400

    filename = secure_filename(file.filename) 
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    muac_pred = predict_muac_from_path(save_path)

    status, explanation, advice = classify_nutrition_status(
        age_months=age_months,
        weight_kg=weight_kg,
        height_cm=height_cm,
        gender=gender,
        muac_cm=muac_pred
    )

    return render_template(
        "result.html",
        gender=gender,
        age_years=age_years,
        age_months=age_months,
        weight_kg=weight_kg,
        height_cm=height_cm,
        muac_pred=float(muac_pred),
        status=status,
        explanation=explanation,
        advice=advice,
        filename=filename
    )

@app.get("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
