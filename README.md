# 🧠 Gerenciador de Tickets com IA (Pydantic-AI + Pydantic-Graph)

Este projeto é um sistema inteligente de gerenciamento de tickets que utiliza agentes de IA para **classificar automaticamente problemas**, **atribuir departamentos responsáveis** e **criar registros no banco de dados**. A interface é construída com **Streamlit**, e toda a lógica é orquestrada via **Pydantic-Graph** com **Pydantic-AI Agents**.

---

## 🚀 Funcionalidades

- 📝 Registro de novo ticket com classificação automática (severidade, departamento, categoria)
- 🔍 Consulta de tickets por ID
- 📂 Listagem e encerramento de tickets abertos
- 📊 Classificação e criação automatizadas com LLMs (Groq + Meta LLaMA)
- 🧱 Banco de dados SQLite com interface singleton thread-safe
- 📜 Registro de logs com rotação automática

---

## 🧩 Estrutura de Diretórios

```
.
├── app.py                  # Interface Streamlit
├── nodes.py                # Nós do grafo Pydantic
├── state.py                # Estado compartilhado entre os nós
├── tickets.py              # Operações de leitura e atualização no banco
├── database.py             # Conexão singleton com SQLite
├── classification.py       # Agente de classificação de tickets
├── creation.py             # Agente de criação de tickets
├── logger.py               # Sistema de logging customizado
```

---

## 🔁 Pipeline

1. **Usuário** envia um resumo via Streamlit
2. **Graph** aciona:
   - Classificação (via `classification.py`)
   - Criação (via `creation.py`)
3. Dados são salvos no SQLite
4. Estado e status são atualizados e exibidos

---

## 🛠️ Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧠 Tecnologias Utilizadas

- [Streamlit](https://streamlit.io/)
- [Pydantic-AI](https://github.com/pydantic/pydantic-ai)
- [Pydantic-Graph](https://github.com/pydantic/pydantic-graph)
- [Groq API](https://console.groq.com/)
- [SQLite](https://www.sqlite.org/index.html)

---

## 📌 Observações

- Os agentes utilizam o modelo `groq:meta-llama/llama-4-scout-17b-16e-instruct`
- Banco criado automaticamente: `tickets_table.db`
- Logs salvos em: `ticket_system.log`

---
