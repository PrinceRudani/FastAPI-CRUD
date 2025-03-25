from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.subcategory_vo import SubcategoryVO


class SubcategoryDAO:
    @staticmethod
    def insert_subcategory_dao(subcategory_vo):
        """Call common insert method for subcategory."""
        subcategory_data = MysqlCommonQuery.insert_query(subcategory_vo)
        return subcategory_data

    @staticmethod
    def get_all_subcategories_dao():
        """Call common get_all method for subcategory."""
        subcategory_data = MysqlCommonQuery.get_all_query(SubcategoryVO)
        return subcategory_data

    @staticmethod
    def delete_subcategory_dao(id):
        """Call common delete method for subcategory."""
        subcategory_data = MysqlCommonQuery.soft_delete_query(SubcategoryVO,id)
        return subcategory_data

    @staticmethod
    def get_subcategory_by_id_dao(id):
        """Fetch a single subcategory by ID (excluding soft-deleted records)."""
        subcategory_data = MysqlCommonQuery.get_by_id_query(SubcategoryVO, id)
        if subcategory_data.subcategory_category_id == 1:
            return None
        return subcategory_data

    @staticmethod
    def update_subcategory_dao(subcategory):
        """Update an existing subcategory."""
        subcategory_data = MysqlCommonQuery.update_query(subcategory)
        return subcategory_data
