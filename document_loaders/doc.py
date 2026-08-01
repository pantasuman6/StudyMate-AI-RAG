from langchain_community.document_loaders import Docx2txtLoader

loader = Docx2txtLoader(
    "C:/Users/pantas/Desktop/StudyMate AI/document loaders/Group_4_Research_Paper_ITS536_Final.docx"
)

documents = loader.load()

print(documents[0].page_content)