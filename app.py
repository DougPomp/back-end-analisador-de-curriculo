from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def info():
    return jsonify({
        "projeto": "Analisador de Currículo com IA",
        "hackathon": "Zeronauta 2025",
        "descricao": "Este projeto utiliza inteligência artificial para analisar currículos em PDF ou Word e fornecer resumos com insights para recrutadores.",
        "funcionalidades": [
            "Upload de currículo (PDF ou DOCX)",
            "Extração e leitura do texto",
            "Análise com modelo de IA",
            "Resumo das competências, experiências e habilidades"
        ],
        "tecnologias": {
            "front-end": "React.js",
            "back-end": "Flask",
            "IA": "OpenAI API",
            "deploy": "Vercel + Render/Fly.io"
        },
        "status": "Em desenvolvimento",
    })

if __name__ == '__main__':
    app.run(debug=True)
