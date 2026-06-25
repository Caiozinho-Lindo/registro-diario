# Registro Diário – Clínica de Fonoaudiologia UTP

Sistema web para geração de Registros Diários clínicos baseado em template Word oficial.

---

## 📂 Estrutura do Projeto

```
registro-diario/
├── frontend/
│   └── index.html          ← Interface web (mobile-first)
├── backend/
│   ├── app.py              ← Flask API
│   └── requirements.txt    ← Dependências Python
├── templates/
│   └── RegistroDiario_Template.docx   ← Template Word OFICIAL (não editar estrutura)
├── outputs/                ← Pasta de saída local (ignorada pelo git)
├── Procfile                ← Deploy Render/Heroku
├── render.yaml             ← Config Render (deploy automático)
└── README.md
```

---

## 🚀 Rodando Localmente

### Pré-requisitos
- Python 3.10+
- pip

### 1. Instalar dependências
```bash
cd backend
pip install -r requirements.txt
```

### 2. Iniciar o servidor
```bash
python app.py
# Servidor rodando em http://localhost:5000
```

### 3. Abrir o frontend
Abra `frontend/index.html` diretamente no navegador.
> O frontend já aponta para `http://localhost:5000` automaticamente quando rodando localmente.

---

## 🌐 Deploy em Produção (Render.com — Gratuito)

### Backend (Flask)

1. Faça push do projeto para um repositório GitHub
2. Acesse [render.com](https://render.com) → **New Web Service**
3. Conecte o repositório
4. Configure:
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `gunicorn --chdir backend app:app --bind 0.0.0.0:$PORT`
   - **Environment:** Python 3

> O `render.yaml` já faz isso automaticamente se usar "Blueprint".

### Frontend (GitHub Pages)

1. Vá em `frontend/index.html`
2. Edite a linha com `BACKEND_URL`:
   ```javascript
   return 'https://SEU-BACKEND.onrender.com';
   ```
   Substitua pela URL real do seu serviço no Render.
3. Faça push do repositório
4. Ative GitHub Pages → Settings → Pages → Branch: main → `/frontend`

---

## 📋 Placeholders no Template Word

O arquivo `RegistroDiario_Template.docx` usa estes placeholders (docxtpl):

| Placeholder         | Campo do Formulário        |
|---------------------|----------------------------|
| `{{paciente}}`      | Nome do(a) Paciente        |
| `{{estagiario}}`    | Nome do(a) Estagiário(a)   |
| `{{dataAtendimento}}` | Data do Atendimento       |
| `{{dataEntrega}}`   | Data da Entrega do Registro |
| `{{objetivos}}`     | Objetivos Gerais e Específicos |
| `{{estrategias}}`   | Estratégia(s)              |
| `{{desenvolvimento}}` | Desenvolvimento           |
| `{{planejamento}}`  | Planejamento / Conduta     |

> Para editar o template, abra no Word, modifique o layout mantendo os `{{placeholders}}` exatamente como estão, e salve sobre o arquivo existente.

---

## 🔧 Melhorias Futuras (Sugestões)

- **Histórico de registros** — salvar em SQLite com `flask-sqlalchemy`
- **Edição de registros anteriores** — listar e reabrir registros salvos
- **Exportação em PDF** — adicionar `libreoffice --headless --convert-to pdf` no backend
- **Autenticação simples** — senha única com `flask-httpauth`
- **Banco de dados** — SQLite (leve, sem servidor) ou PostgreSQL (Render oferece gratuito)

---

## 💚 Nota

Após cada documento gerado, o sistema exibe: **"Faço tudo por você, eu te amo"**
