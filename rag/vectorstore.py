"""RAG setup and vectorstore initialization."""

import json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from rag.embed import embeddings


def load_docs():
    with open("synthetic_support_dataset.json") as f:
        data = json.load(f)

    docs = []

    for item in data:
        docs.append(
            Document(
                page_content=item["content"],
                metadata={
                    "category": item["category"],
                    "tags": item["tags"]
                }
            )
        )

    return docs


def setup_vectorstore():
    docs = load_docs()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=64
    )

    chunked_docs = splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=chunked_docs,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    return vectorstore


# Global vectorstore instance
vectorstore = setup_vectorstore()