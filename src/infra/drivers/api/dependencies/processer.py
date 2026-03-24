from core.ports.processer.rulebook_processer import IRulebookProcesser
from infra.adapters.processer.langchain_processer import LangChainProcesser


async def get_rulebook_processer():
    processer = LangChainProcesser()
    yield processer
