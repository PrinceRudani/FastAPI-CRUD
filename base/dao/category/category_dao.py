from sqlalchemy.orm import Session

from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.category_vo import CategoryVO


class CategoryDAO:
    @staticmethod
    def insert_category(session: Session, category: CategoryVO):
        """Call common insert method for category."""
        return MysqlCommonQuery.insert(session, category)

    @staticmethod
    def get_all_categories(session: Session):
        """Call common get_all method for category."""
        return MysqlCommonQuery.get_all(session, CategoryVO)

    @staticmethod
    def delete_category(db: Session, id: int):
        """Call common delete method for category."""
        return MysqlCommonQuery.soft_delete(db, CategoryVO, id)

    @staticmethod
    def get_category_by_id(session: Session, id: int):
        """Fetch a single category by ID (excluding soft-deleted records)."""
        return MysqlCommonQuery.get_by_id(session, CategoryVO, id)

    @staticmethod
    def update_category(session: Session, category: CategoryVO):
        """Update an existing category."""
        return MysqlCommonQuery.update(session, category)
