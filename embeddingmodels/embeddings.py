from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(
    model = 'text-embedding-3-large',
    dimensions=64
)

texts = [
    "Hello thios is san",
    "Hello your name is youtube",
    "And you all are very beautiful"
]
vector = embeddings.embed_documents(texts)

print(vector)