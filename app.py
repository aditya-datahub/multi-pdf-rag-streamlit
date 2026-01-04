import os
import streamlit as st
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from rag_utility import (
    process_pdfs_to_chroma_db,
    answer_questions
)

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found in .env file")
    st.stop()

# --------------------------------------------------
# Streamlit config
# --------------------------------------------------
st.set_page_config(
    page_title="Multi-PDF RAG",
    layout="wide"
)

st.title("📚 Multi-PDF RAG using Llama-3.3-70B")

# --------------------------------------------------
# Working directory
# --------------------------------------------------
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_DIR = os.path.join(WORKING_DIR, "doc_vectorstore")

# --------------------------------------------------
# Load models ONCE
# --------------------------------------------------
@st.cache_resource
def load_models():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}  # fixes meta tensor issue
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=GROQ_API_KEY
    )

    return embeddings, llm


embeddings, llm = load_models()

# --------------------------------------------------
# Upload multiple PDFs
# --------------------------------------------------
st.subheader("📄 Upload PDFs")

uploaded_files = st.file_uploader(
    "Upload 2–3 PDFs (or more)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    with st.spinner("Processing PDFs..."):
        process_pdfs_to_chroma_db(
            uploaded_files=uploaded_files,
            working_dir=WORKING_DIR,
            embedding=embeddings
        )

    st.success("✅ PDFs indexed successfully!")

# --------------------------------------------------
# Ask multiple questions
# --------------------------------------------------
st.divider()
st.subheader("❓ Ask questions across all uploaded PDFs")

questions_text = st.text_area(
    "Enter one or more questions (each on a new line):",
    height=150
)

if st.button("Answer"):
    if not questions_text.strip():
        st.warning("Please enter at least one question.")
    else:
        questions = [
            q.strip() for q in questions_text.split("\n") if q.strip()
        ]

        with st.spinner("Thinking..."):
            answers = answer_questions(
                questions=questions,
                working_dir=WORKING_DIR,
                embedding=embeddings,
                llm=llm
            )

        # --------------------------------------------------
        # Display Answers (FIXED UI)
        # --------------------------------------------------
        st.subheader("🧠 Answers")

        for idx, (q, ans) in enumerate(zip(questions, answers), start=1):
            st.markdown(f"### ❓ Question {idx}")
            st.markdown(q)

            st.markdown(f"### 🅰️ Answer {idx}")
            st.markdown(ans)

            st.divider()
