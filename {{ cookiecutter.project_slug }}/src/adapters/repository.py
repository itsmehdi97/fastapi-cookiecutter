import abc
from typing import List, Optional

from sqlalchemy import select

import models
import schemas
from db import Session


class BaseRepository(abc.ABC):
    def __init__(self, db: Session):
        self.db = db


class UserRepository(BaseRepository):
    model = models.User

    async def create(self, user: models.User) -> models.User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_username(self, username: str) -> models.User:
        result = await self.db.execute(select(models.User) \
            .where(models.User.username == username))
        return result.scalar()


class TaskRepository(BaseRepository):
    async def get_project_tasks(self, project_id: int, user_id: Optional[int] = None) -> List[models.Task]:
        q = select(models.Task) \
            .where(models.Task.project_id == project_id)
        if user_id:
            q = q.join(models.UsersTasks, onclause=models.UsersTasks.task_id==models.Task.id) \
                .where(models.UsersTasks.user_id == user_id)

        result = await self.db.execute(q)
        return result.scalars().all()

    async def get_task_by_id(self, id: int) -> models.Task:
        result = await self.db.execute(select(models.Task).where(models.Task.id == id))
        return result.scalar()

    async def create_task(self, task: schemas.TaskCreate) -> models.Task:
        db_task = models.Task(**task.dict())
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task
