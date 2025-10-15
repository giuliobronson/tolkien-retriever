from core.application.message_service import MessageService


def get_message_service() -> MessageService:
    return MessageService()