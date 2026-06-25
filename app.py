import io
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from docxtpl import DocxTemplate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "RegistroDiario_Template.docx")

app = Flask(__name__)
CORS(app)

def fmt_date(iso_str):
    try:
        return datetime.strptime(iso_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    except:
        return iso_str or ""

@app.route("/gerar", methods=["POST"])
def gerar():
    data = request.get_json(force=True)
    campos = ["paciente","estagiario","dataAtend","dataEntrega",
              "objetivos","estrategias","desenvolvimento","planejamento"]
    faltando = [c for c in campos if not data.get(c,"").strip()]
    if faltando:
        return jsonify({"erro": f"Campos ausentes: {', '.join(faltando)}"}), 400

    contexto = {
        "paciente":        data["paciente"].strip(),
        "estagiario":      data["estagiario"].strip(),
        "dataAtendimento": fmt_date(data["dataAtend"]),
        "dataEntrega":     fmt_date(data["dataEntrega"]),
        "objetivos":       data["objetivos"].strip(),
        "estrategias":     data["estrategias"].strip(),
        "desenvolvimento": data["desenvolvimento"].strip(),
        "planejamento":    data["planejamento"].strip(),
    }

    tpl = DocxTemplate(TEMPLATE_PATH)
    tpl.render(contexto)
    buf = io.BytesIO()
    tpl.save(buf)
    buf.seek(0)

    nome = f"RegistroDiario_{contexto['paciente'].replace(' ','_')}.docx"
    return send_file(buf, as_attachment=True, download_name=nome,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
