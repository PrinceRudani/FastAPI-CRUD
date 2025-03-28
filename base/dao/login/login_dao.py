from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.login_vo import LoginVO


class LoginDAO:
    @staticmethod
    def get_login_id(login_username):
        """Get user details by username."""
        get_data = MysqlCommonQuery.get_user_by_username(LoginVO, login_username)
        return get_data
