from langchain_community.document_loaders import PyPDFLoader

data=PyPDFLoader("C:/Users/pantas/Desktop/StudyMate AI/document loaders/ArtificialIntelligenceforCyberThreatDetection.pdf")

docs=data.load()

print(len(docs))