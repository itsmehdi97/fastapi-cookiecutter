from datetime import datetime

from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    DateTime, String, Integer, Boolean, Text,
    ForeignKey
)


mapper_registry = registry()
Base = mapper_registry.generate_base()


class BaseModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, nullable=True, onupdate=lambda: datetime.now())


class User(BaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(length=64), nullable=False, unique=True)
    password = Column(String(length=64), nullable=False)
    is_active = Column(Boolean, default=True)


class Task(BaseModel):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    title = Column(String(length=128), nullable=True)
    desc = Column(Text(), nullable=True)
    project_id = Column(ForeignKey("project.id"), nullable=False)
