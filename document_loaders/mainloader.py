from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    WebBaseLoader,
)


def load_document(source, doc_type):

    if doc_type == "pdf":
        loader = PyPDFLoader(source)

    elif doc_type == "txt":
        loader = TextLoader(source)

    elif doc_type == "docx":
        loader = Docx2txtLoader(source)

    elif doc_type == "url":
        loader = WebBaseLoader(source)

    else:
        raise ValueError(f"Unsupported document type: {doc_type}")

    return loader.load()


def load_all_documents(folder_path="document_loaders/documents"):
    """
    Load every PDF, DOCX and TXT file from the documents folder.
    """

    documents = []

    folder = Path(folder_path)

    if not folder.exists():
        print(f"{folder_path} does not exist.")
        return documents

    for file in folder.iterdir():

        suffix = file.suffix.lower()

        try:

            if suffix == ".pdf":
                print(f"Loading {file.name}")
                documents.extend(load_document(str(file), "pdf"))

            elif suffix == ".docx":
                print(f"Loading {file.name}")
                documents.extend(load_document(str(file), "docx"))

            elif suffix == ".txt":
                print(f"Loading {file.name}")
                documents.extend(load_document(str(file), "txt"))

        except Exception as e:
            print(f"Failed to load {file.name}: {e}")

    return documents


def load_urls(url_file="document_loaders/urls.txt"):
    """
    Load every URL listed in urls.txt
    """

    documents = []

    path = Path(url_file)

    if not path.exists():
        return documents

    with open(path, "r", encoding="utf-8") as f:

        for line in f:

            url = line.strip()

            if url:

                try:
                    print(f"Loading {url}")
                    documents.extend(load_document(url, "url"))

                except Exception as e:
                    print(f"Failed to load {url}: {e}")

    return documents