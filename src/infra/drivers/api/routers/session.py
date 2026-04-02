from fastapi import APIRouter, Depends

from core.application.services.session_service import SessionService
from infra.drivers.api.dependencies.services import get_session_service
from infra.drivers.api.dto.message_dto import MessageDTO
from infra.drivers.api.dto.session_dto import SessionDTO
from infra.mappers.message_mapper import MessageMapper
from infra.mappers.session_mapper import SessionMapper

router = APIRouter(prefix="/sessions", tags=["session"])
