from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

import schemas
from services import exceptions as exc
from api.deps.service import get_service
from api.deps.auth import current_user



router = APIRouter(tags=[])
