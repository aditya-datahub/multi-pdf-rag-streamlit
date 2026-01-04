# 📚 Multi-PDF RAG Streamlit App

A **Streamlit-based multi-PDF document Question & Answer system** using  
**Retrieval-Augmented Generation (RAG)** powered by **Llama-3 via Groq** and **ChromaDB**.

---

## 🚀 Features

- 📄 Upload **multiple PDFs**
- 🔍 Semantic search using **HuggingFace embeddings**
- 🧠 Accurate answers using **Llama-3.3-70B (Groq)**
- 🧩 Vector storage with **ChromaDB**
- ❓ Ask **multiple questions at once**
- 🧠 Clean **Question → Answer** UI
- ⚡ Fast inference via **Groq API**

---

## 🏗️ Project Structure

```
├── app.py # Streamlit app
├── rag_utility.py # PDF processing + RAG logic
├── requirements.txt # Dependencies
├── env_template.txt # Environment variable template
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🧠 How It Works (RAG Pipeline)

1. Upload PDFs using Streamlit
2. PDFs are:
   - Loaded using `UnstructuredPDFLoader`
   - Split into chunks
   - Converted into embeddings
3. Embeddings are stored in **ChromaDB**
4. User questions are:
   - Retrieved via similarity search
   - Passed to **Llama-3** with context
5. Model returns **grounded answers**

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/multi-pdf-rag-streamlit.git
cd multi-pdf-rag-streamlit
```
### 2️⃣ Create a virtual environment (recommended)
```
conda create -n rag python=3.10
conda activate rag
```
### 3️⃣ Install dependencies
```
pip install -r requirements.txt
(or copy env_template.txt → .env)
```
---

## 🔐 Environment Variables
Create a .env file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```
You can refer to env_template.txt for guidance.

---

## ▶️ Run the Application
```
streamlit run app.py
```
---

## 🧪 Example Usage

1. Upload one or more PDFs
2. Enter questions (one per line), for example:
```
What is an ecosystem?
What are the types of ecosystems?
Forerunners of Evo-Devo?
```
3. Click Answer
4. Get structured Question → Answer results

---

## 🧩 Tech Stack

1. Frontend: Streamlit
2. LLM: Llama-3.3-70B (Groq)
3. Embeddings: all-MiniLM-L6-v2
4. Vector Database: ChromaDB
5. Framework: LangChain
5. Language: Python

---

## 🌍 Deployment

This application is ready to deploy on:
1. Streamlit Cloud
2. Docker
3. Any cloud VM (AWS / GCP / Azure)

---

## 📜 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute it.

---

## 🙌 Acknowledgements

1. Groq
2. LangChain
3. HuggingFace
4. Streamlit

---
