from typing import List
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage


def build_expand_query(history: List[BaseMessage]) -> List[BaseMessage]:
    return [
        SystemMessage(content="Baseado no histórico abaixo, gere uma query breve e específica para busca RAG."),
        *history,
        HumanMessage(content="Resuma o objetivo atual do usuário em uma frase curta, clara e pesquisável.")
    ]

def build_rag_prompt(history: List[BaseMessage], documents):
    return [
        SystemMessage(
            content=f"""
                Você é um assistente que responde ao usuário com base nos documentos recuperados.

                Instruções:
                - Utilize SOMENTE os documentos como fonte principal.
                - Se alguma parte da resposta não existir nos documentos, responda que não pode concluir nada.
                - Não invente fatos específicos.
                - Cite quais trechos dos documentos influenciam sua resposta.

                Documentos recuperados:
                {documents}
            """
        ),
        *history
    ]