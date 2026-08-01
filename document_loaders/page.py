from langchain_community.document_loaders import WebBaseLoader

urls = [

"https://medium.com/@pantasuman6/linear-regression-9d51f9713770"
"https://medium.com/@pantasuman6/how-large-language-models-llms-work-c7b68bf49868"
"https://medium.com/@pantasuman6/implementing-the-least-privilege-principle-in-cloud-security-a-useful-manual-for-contemporary-a3cae551c59e"
"https://medium.com/@pantasuman6/the-growing-risk-of-ransomware-as-a-service-raas-why-its-a-national-security-issue-e71b44fbb1c3"
"https://medium.com/@pantasuman6/sql-injection-how-it-works-and-how-to-prevent-it-9344a6f75969"
"https://medium.com/@pantasuman6/why-endpoint-hardening-has-become-critical-in-2026-ffe34ef5577f"
"https://medium.com/@pantasuman6/claude-code-security-how-ais-revolution-is-changing-contemporary-software-defense-173772670b61"
]

data=WebBaseLoader(urls)
docs=data.load()

print(docs)
