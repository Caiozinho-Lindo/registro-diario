"""
Registro Diário – Backend Flask
Preenche o template Word com docxtpl e serve o .docx para download.
"""

import io
import os
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from docxtpl import DocxTemplate

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "..", "templates", "RegistroDiario_Template.docx")

app = Flask(__name__)
CORS(app)   # permite chamadas do frontend (GitHub Pages ou localhost)


# ── Helpers ────────────────────────────────────────────────────────────────

def fmt_date(iso_str: str) -> str:
    """Converte 'YYYY-MM-DD' → 'DD/MM/YYYY'. Retorna a string original se falhar."""
    try:
        return datetime.strptime(iso_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return iso_str or ""


def safe_filename(paciente: str, data: str) -> str:
    """Gera nome de arquivo seguro: RegistroDiario_PacienteNome_DD-MM-YYYY.docx"""
    nome  = "".join(c if c.isalnum() or c in " _-" else "" for c in paciente).strip().replace(" ", "_")
    data2 = data.replace("/", "-")
    return f"RegistroDiario_{nome}_{data2}.docx"


# ── Rota principal ─────────────────────────────────────────────────────────

@app.route("/gerar", methods=["POST"])
def gerar():
    """
    Recebe JSON com os campos do formulário,
    preenche o template Word e devolve o .docx como download.
    """
    data = request.get_json(force=True)

    # Campos obrigatórios
    campos = ["paciente", "estagiario", "dataAtend", "dataEntrega",
              "objetivos", "estrategias", "desenvolvimento", "planejamento"]
    faltando = [c for c in campos if not data.get(c, "").strip()]
    if faltando:
        return jsonify({"erro": f"Campos obrigatórios ausentes: {', '.join(faltando)}"}), 400

    # Formata datas
    data_atend   = fmt_date(data["dataAtend"])
    data_entrega = fmt_date(data["dataEntrega"])

    # Contexto para docxtpl
    # ⚠️  O template usa {{dataAtendimento}} e {{dataEntrega}}
    contexto = {
        "paciente":        data["paciente"].strip(),
        "estagiario":      data["estagiario"].strip(),
        "dataAtendimento": data_atend,          # nome do placeholder no .docx
        "dataEntrega":     data_entrega,
        "objetivos":       data["objetivos"].strip(),
        "estrategias":     data["estrategias"].strip(),
        "desenvolvimento": data["desenvolvimento"].strip(),
        "planejamento":    data["planejamento"].strip(),
    }

    # Preenche o template
    tpl = DocxTemplate(TEMPLATE_PATH)
    tpl.render(contexto)

    # Salva em memória e devolve
    buf = io.BytesIO()
    tpl.save(buf)
    buf.seek(0)

    filename = safe_filename(contexto["paciente"], data_atend)

    return send_file(
        buf,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})


# ── Entrypoint ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
