from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.category_vo import CategoryVO

class CategoryDAO:
    @staticmethod
    def insert_category_dao(category_vo: CategoryVO, session):
        """Call common insert method for category."""
        return MysqlCommonQuery.insert_query(category_vo, session)

    @staticmethod
    def get_all_categories_dao(session):
        """Call common get_all method for category."""
        return MysqlCommonQuery.get_all_query(CategoryVO, session)

    @staticmethod
    def delete_category_dao(session, id: int):
        """Call common delete method for category."""
        return MysqlCommonQuery.soft_delete_query(CategoryVO, id, session)

    @staticmethod
    def get_category_by_id_dao(session, id: int):
        """Fetch a single category by ID (excluding soft-deleted records)."""
        return MysqlCommonQuery.get_by_id_query(CategoryVO, id, session)

    @staticmethod
    def update_category_dao(category: CategoryVO, session):
        """Update an existing category."""
        return MysqlCommonQuery.update_query(category, session)