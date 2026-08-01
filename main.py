import os
from dotenv import load_dotenv

# 1. Load environment variables FIRST to resolve the httpx.LocalProtocolError
load_dotenv()

# Your existing imports
from document_loaders.mainloader import load_document
from vector_store.splitter import split_documents
from vector_store.db import create_vector_db

# New imports for the Retrieval-Augmented Generation (RAG) architecture
from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings, ChatMistralAI
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

def main():
    # --- PHASE 1: DATA INGESTION & VECTOR DB CREATION ---
    from document_loaders.mainloader import (
    load_all_documents,
    load_urls,
    )

    print("Loading documents...")

    documents = []

    documents.extend(load_all_documents())
    documents.extend(load_urls())

    print(f"\nLoaded {len(documents)} document pages.")

    print("Splitting documents...")
    chunks = split_documents(documents)

    print("Creating/Updating Vector Database...")
    db = create_vector_db(chunks)
    print("Vector database created successfully!")

    # --- PHASE 2: RETRIEVER & LLM ARCHITECTURE ---
    print("\nInitializing Retriever and Mistral LLM...")
    
    # Initialize the same embeddings used in db.py
    embeddings = MistralAIEmbeddings(model="mistral-embed")
    
    # Bind to the existing Chroma database directory
    vector_db = Chroma(
        persist_directory="./vector_store/chroma_db",
        embedding_function=embeddings
    )
    
    # Create the retriever (search_kwargs={"k": 3} fetches the 3 most relevant chunks)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    
    # Initialize the Mistral chat model for generation
    llm = ChatMistralAI(model="mistral-large-latest")
    
    # Define the RAG instruction prompt
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, say that you don't know. "
        "Keep the answer concise.\n\n"
        "Conversation History:\n{chat_history}\n\n"
        "Context:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Create the chain that formats the retrieved chunks into the prompt's {context} variable
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    # Create the final chain connecting the retriever to the LLM
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    print("\n--------StudyMate AI--------")
    print("Type 0 to Exit\n")



    chat_history = []


    while True:
        
        user_query = input("User: ").strip()

        # Exit condition
        if user_query==0:
            print("\nThank you for using StudyMate AI!")
            break

        # Ignore empty input
        if not user_query:
            continue

        try:
            # Retrieve relevant documents and generate answer
            response = rag_chain.invoke({
                "input": user_query,
                "chat_history": chat_history

                                         })

            print("\nStudyMate AI:")
            print(response["answer"])
            chat_history.append(
            HumanMessage(content=user_query)
            )

            chat_history.append(
            AIMessage(content=response["answer"])
            )
            print()

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()