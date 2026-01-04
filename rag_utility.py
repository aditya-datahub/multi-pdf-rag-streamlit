import os
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA


def process_pdfs_to_chroma_db(uploaded_files, working_dir, embedding):
    """
    Load multiple PDFs, split text, and store embeddings in Chroma.
    """

    vectorstore_dir = os.path.join(working_dir, "doc_vectorstore")
    all_documents = []

    # Save & load PDFs
    for file in uploaded_files:
        pdf_path = os.path.join(working_dir, file.name)
        with open(pdf_path, "wb") as f:
            f.write(file.getbuffer())

        loader = UnstructuredPDFLoader(pdf_path)
        docs = loader.load()
        all_documents.extend(docs)

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(all_documents)

    # Create / overwrite Chroma DB
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=vectorstore_dir
    )


def answer_questions(questions, working_dir, embedding, llm):
    """
    Answer multiple questions from the same vector store.
    """

    vectorstore_dir = os.path.join(working_dir, "doc_vectorstore")

    vectordb = Chroma(
        persist_directory=vectorstore_dir,
        embedding_function=embedding
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )

    answers = []
    for q in questions:
        result = qa_chain.invoke({"query": q})
        answers.append(result["result"])

    return answers
