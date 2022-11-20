from typing import Callable, Type

from fastapi import Depends

from services.base import BaseService
from adapters.repository import BaseRepository
from api.deps.db import get_repository


def get_service(*,
    repo_type: Type[BaseRepository],
    service_type: Type[BaseService],
) -> Callable:
    def _get_service(
        repo: BaseRepository = Depends(get_repository(repo_type)),
    ) -> Type[BaseService]:
        return service_type(repo)

    return _get_service
