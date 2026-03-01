from core.ports.processer.rulebook_processer import IRulebookProcesser
from infra.adapters.processer.docling_loader import DoclingLoader


class LangChainProcesser(IRulebookProcesser):

    async def process(self, content: bytes, filename: str) -> None:
        loader = DoclingLoader(content, filename)
        loader.alazy_load()
