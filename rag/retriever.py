"""Retrieval utilities using vectorstore."""

from rag.vectorstore import vectorstore


def retrieve_documents(query: str, category: str = None, k: int = 5):
    """Retrieve documents with optional category filtering."""
    search_kwargs = {"k": k}
    if category:
        search_kwargs["filter"] = {"category": category}

    retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)
    results = retriever.invoke(query)
    return results
