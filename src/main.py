from config import LANGSMITH_API_URL, MINIO_ENDPOINT_URL, MINIO_ROOT_PASSWORD, MINIO_ROOT_USER
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import S3FileLoader
from langchain import hub
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict

llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0.0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = Chroma(
    collection_name="tolkien-retriever",
    embedding_function=embeddings,
    # persist_directory="./chroma_langchain_db",  
)

loader = S3FileLoader(
    bucket="rulebooks",
    key="lotrlcg/LTR101_Regras_2021-06-04.pdf",
    endpoint_url=MINIO_ENDPOINT_URL,
    aws_access_key_id=MINIO_ROOT_USER,
    aws_secret_access_key=MINIO_ROOT_PASSWORD
)

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

# Index chunks
_ = vector_store.add_documents(documents=all_splits)

# Define prompt for question-answering
# N.B. for non-US LangSmith endpoints, you may need to specify
# api_url="https://api.smith.langchain.com" in hub.pull.
prompt = hub.pull("rlm/rag-prompt", api_url=LANGSMITH_API_URL)


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"], k=10)
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

response = graph.invoke({"question": "Se baseando apenas nas regras do jogo responda a pergunta: Se um jogador fizer um contro opcional, o proximo não quiser fazer, mas o primeiro jogador quiser realizar um segundo confronto opcional, ele pode fazer?"})
print(response["answer"])