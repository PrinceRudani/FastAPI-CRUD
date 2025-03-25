from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.subcategory_vo import SubcategoryVO


class SubcategoryDAO:
    @staticmethod
    def insert_subcategory_dao(subcategory_vo: SubcategoryVO, session):
        """Call common insert method for subcategory."""
        return MysqlCommonQuery.insert_query(subcategory_vo, session)

    @staticmethod
    def get_all_subcategories_dao(session):
        """Call common get_all method for subcategory."""
        return MysqlCommonQuery.get_all_query(SubcategoryVO, session)

    @staticmethod
    # def delete_subcategory_dao(id: int, session):
    #     """Call common delete method for subcategory."""
    #     return MysqlCommonQuery.soft_delete_query(SubcategoryVO, id, session)

    @staticmethod
    def get_subcategory_by_id_dao(id: int):
        """Fetch a single subcategory by ID (excluding soft-deleted records)."""
        return MysqlCommonQuery.get_by_id_query(SubcategoryVO, id)

    @staticmethod
    def update_subcategory_dao(subcategory: SubcategoryVO):
        """Update an existing subcategory."""
        return MysqlCommonQuery.update_query(subcategory)
