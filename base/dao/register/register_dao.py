from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.login_vo import LoginVO
from base.vo.role_vo import RoleVO


class RegisterDAO:
    @staticmethod
    def check_existing_user(username):
        """Check if the username already exists."""
        return MysqlCommonQuery.get_record_by_field(LoginVO, "login_username", username)

    @staticmethod
    def insert_register_user(register_vo):
        """Insert a new registered user."""
        return MysqlCommonQuery.insert_query(register_vo)

    @staticmethod
    def get_role(role_vo):
        return MysqlCommonQuery.get_record_by_field(
            RoleVO, "role_name", role_vo.role_name
        )
