from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings


def create_vector_db(chunks):

    embeddings = MistralAIEmbeddings(
        model="mistral-embed"
    )


    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./vector_store/chroma_db"
    )


    return vector_db

