from typing import Type, Any
from sqlalchemy.orm import Session


class MysqlCommonQuery:
    """Generic MySQL repository for common database operations."""

    @staticmethod
    def insert(session: Session, entity: Any):
        """Insert a new entity into the database."""
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity

    @staticmethod
    def get_all(session: Session, model: Type):
        """Retrieve all non-deleted entities of a given model."""
        return session.query(model).filter_by(is_deleted=False).all()

    @staticmethod
    def get_by_id(session: Session, model: Type, entity_id: int):
        """Retrieve an entity by its ID, excluding soft-deleted entities."""
        return session.query(model).filter_by(id=entity_id, is_deleted=False).first()

    @staticmethod
    def update(session: Session, entity: Any):
        """Commit updates to an existing entity."""
        session.commit()
        session.refresh(entity)
        return entity

    @staticmethod
    def soft_delete(session: Session, model: Type, entity_id: int):
        """Perform a soft delete by setting `is_deleted=True`."""
        entity = session.query(model).filter_by(id=entity_id, is_deleted=False).first()
        if entity:
            entity.is_deleted = True
            session.commit()
        return entity
