from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.product_vo import ProductVO


class ProductDAO:
    @staticmethod
    def insert_product_dao(product_vo):
        """Call common insert method for product."""
        product_data = MysqlCommonQuery.insert_query(product_vo)
        return product_data

    @staticmethod
    def get_all_product_dao():
        """Call common get_all method for product."""
        product_data = MysqlCommonQuery.get_all_query(ProductVO)
        return product_data

    @staticmethod
    def delete_product_dao(id):
        """Call common delete method for product."""
        product_data = MysqlCommonQuery.soft_delete_query(ProductVO, id)
        return product_data

    @staticmethod
    def get_product_by_id_dao(id):
        """Fetch a single product by ID (excluding soft-deleted records)."""
        product_data = MysqlCommonQuery.get_by_id_query(ProductVO, id)

        return product_data

    @staticmethod
    def update_product_dao(product):
        """Update an existing product."""
        product_data = MysqlCommonQuery.update_query(product)
        return product_data
