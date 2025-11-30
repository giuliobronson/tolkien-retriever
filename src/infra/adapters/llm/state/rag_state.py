from typing import List, Optional, TypedDict
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document


class RagState(TypedDict):
   query: Optional[BaseMessage]
   messages: List[BaseMessage]
   documents: List[Document]