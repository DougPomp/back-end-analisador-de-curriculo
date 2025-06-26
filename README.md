# Analisador de Currículos com IA 📄🤖

Este é um projeto de código aberto desenvolvido pela **Comunidade Zeronauta** com o objetivo de criar uma ferramenta prática e inteligente para análise de currículos, utilizando Python e Inteligência Artificial.

## 🚀 Sobre o Projeto

O **Analisador de Currículos Inteligente** é uma API que recebe um currículo em formato PDF e utiliza um modelo de linguagem avançado (LLM) para extrair informações estruturadas, como dados de contato, habilidades técnicas e experiência profissional.

Este projeto nasceu como um desafio colaborativo para que os membros da comunidade pudessem aplicar seus conhecimentos em um problema do mundo real, além de criar um portfólio robusto e relevante para o mercado de tecnologia.

### ✨ Funcionalidades Principais

  * **Extração Automática de Texto:** Leitura de arquivos PDF para extrair o conteúdo textual completo.
  * **Análise com Inteligência Artificial:** Uso de um modelo de linguagem para interpretar o texto e identificar entidades-chave.
  * **Saída de Dados Estruturada:** Devolução das informações extraídas em um formato JSON limpo e previsível.
  * **API Simples:** Um endpoint único para facilitar a integração e o uso da ferramenta.

### 🛠️ Tecnologias Utilizadas

| Tecnologia | Descrição |
| :--- | :--- |
| **Python** | Linguagem principal para o desenvolvimento do back-end. |
| **Flask** | Micro-framework web para a criação da nossa API. |
| **OpenAI API** | Plataforma de IA utilizada para processar e analisar o texto do currículo. |
| **PyMuPDF** | Biblioteca de alta performance para extração de texto de arquivos PDF. |
| **Git & GitHub** | Para controle de versão e colaboração em equipe. |

## 🏁 Começando

Siga os passos abaixo para configurar e executar o projeto em sua máquina local.

### Pré-requisitos

  * **Python 3.9+**
  * **Git**
  * Uma chave de API da [OpenAI](https://platform.openai.com/signup)

### ⚙️ Instalação

1.  **Clone o repositório para sua máquina local:**

    ```bash
    git clone https://github.com/seu-usuario-mentor/analisador-curriculo-zeronauta.git
    cd analisador-curriculo-zeronauta
    ```

2.  **Crie e ative um ambiente virtual:**

      * No Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
      * No macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Instale as dependências do projeto:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure suas variáveis de ambiente:**

      * Renomeie o arquivo `.env.example` para `.env`.
        ```bash
        # No Windows (PowerShell)
        Rename-Item .env.example .env

        # No macOS/Linux
        mv .env.example .env
        ```
      * Abra o arquivo `.env` e insira sua chave da API da OpenAI:
        ```
        OPENAI_API_KEY="sk-SUA-CHAVE-SECRETA-AQUI"
        ```

    ***Importante:** O arquivo `.env` nunca deve ser enviado para o GitHub.*

### 🏃 Executando a Aplicação

1.  **Inicie o servidor Flask:**
    ```bash
    flask run
    ```
2.  O servidor estará rodando em `http://127.0.0.1:5000`.

## 🕹️ Como Usar a API

Para analisar um currículo, envie uma requisição `POST` para o endpoint `/analisar-curriculo` com o arquivo PDF.

Você pode usar uma ferramenta como [Postman](https://www.postman.com/) ou o comando `curl` no terminal.

**Exemplo com `curl`:**

```bash
curl -X POST \
  -F "curriculo=@/caminho/para/seu/curriculo.pdf" \
  http://127.0.0.1:5000/analisar-curriculo
```

*(Substitua `/caminho/para/seu/curriculo.pdf` pelo caminho real do arquivo em sua máquina).*

### ✅ Exemplo de Resposta de Sucesso (JSON)

```json
{
  "nome_completo": "Ana Silva",
  "email": "ana.silva@email.com",
  "telefone": "(11) 99999-8888",
  "habilidades_tecnicas": [
    "Python",
    "Flask",
    "JavaScript",
    "React",
    "SQL",
    "Git",
    "Docker"
  ],
  "experiencia_profissional": [
    {
      "cargo": "Desenvolvedora de Software Jr",
      "empresa": "Tech Solutions",
      "periodo": "Jan 2023 - Presente",
      "descricao": "Desenvolvimento e manutenção de APIs REST com Python e Flask..."
    }
  ]
}
```

## 🤝 Como Contribuir

Este é um projeto feito pela comunidade e para a comunidade. Toda contribuição é bem-vinda\!

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo para mais detalhes.

-----

Feito com ❤️ pela **Comunidade Zeronauta**. Vamos construir coisas incríveis juntos\!