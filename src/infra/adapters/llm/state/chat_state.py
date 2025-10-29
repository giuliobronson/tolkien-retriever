from typing import List, TypedDict
from langchain_core.messages import BaseMessage


class ChatState(TypedDict):
   messages: List[BaseMessage] 