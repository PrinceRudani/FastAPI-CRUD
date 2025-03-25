from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.category_vo import CategoryVO


class CategoryDAO:
    @staticmethod
    def insert_category_dao(category_vo):
        """Call common insert method for category."""
        category_data = MysqlCommonQuery.insert_query(category_vo)
        return category_data

    @staticmethod
    def get_all_categories_dao():
        """Call common get_all method for category."""
        category_data = MysqlCommonQuery.get_all_query(CategoryVO)
        return category_data

    @staticmethod
    def delete_category_dao(id):
        """Call common delete method for category."""
        category_data = MysqlCommonQuery.soft_delete_query(CategoryVO, id)
        return category_data

    @staticmethod
    def get_category_by_id_dao(id):
        """Fetch a single category by ID (excluding soft-deleted records)."""
        category_data = MysqlCommonQuery.get_by_id_query(CategoryVO, id)
        return category_data

    @staticmethod
    def update_category_dao(category_vo):
        """Update an existing category."""
        category_data = MysqlCommonQuery.update_query(category_vo)
        return category_data
