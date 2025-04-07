from base.client.mysql_common.mysql_common_query import MysqlCommonQuery
from base.vo.login_vo import LoginVO


class LoginDAO:
    @staticmethod
    def insert_login_user(login_vo):
        """Insert a new login user record."""
        get_data = MysqlCommonQuery.insert_query(login_vo)
        return get_data

    @staticmethod
    def get_user_by_username(username):
        get_data = MysqlCommonQuery.get_record_by_field(LoginVO,
                                                        "login_username",
                                                        username)
        print("get_user_by_username", get_data)
        return get_data

    @staticmethod
    def update_login_status(user):
        print("Calling MysqlCommonQuery to update login status...")
        MysqlCommonQuery.update_login_status(LoginVO, user)
