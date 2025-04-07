from base.db.database import Database

database = Database()
engine = database.get_db_connection()


class MysqlCommonQuery:
    """Generic MySQL repository for common database operations."""

    @staticmethod
    def insert_query(create_object):
        """Insert a new entity into the database."""
        session = database.get_db_session(engine)
        session.add(create_object)
        session.commit()
        session.refresh(create_object)
        return create_object

    @staticmethod
    def get_all_query(table_name):
        """Retrieve all non-deleted entities of a given model."""
        session = database.get_db_session(engine)
        table_data = session.query(table_name).filter_by(
            is_deleted=False).all()
        return table_data

    @staticmethod
    def soft_delete_query(table_name, entity_id: int):
        """Perform a soft delete by setting `is_deleted=True`."""
        session = database.get_db_session(engine)
        table_data = (
            session.query(table_name).filter_by(id=entity_id,
                                                is_deleted=False).first()
        )
        print(f"table_data-{table_data}")
        table_data.is_deleted = True
        session.commit()
        return table_data

    # #
    @staticmethod
    def get_by_id_query(table_name, entity_id: int):
        """Retrieve an entity by its ID, excluding soft-deleted entities."""
        session = database.get_db_session(engine)
        table_data = (
            session.query(table_name).filter_by(id=entity_id,
                                                is_deleted=False).first()
        )
        return table_data

    @staticmethod
    def update_query(update_record):
        """Commit updates to an existing entity."""
        session = database.get_db_session(engine)
        session.merge(update_record)
        session.flush()
        session.commit()
        session.close()
        return update_record


    @staticmethod
    def get_record_by_field(model, field_name, value):
        session = database.get_db_session(engine)
        user_data = session.query(model).filter(
                getattr(model, field_name) == value).first()
        print(">>>>user_data", user_data)
        session.close()
        return user_data

    @staticmethod
    def update_login_status(model_class, model):
        print(f"Updating login status for user ID: {model.id}")
        session = database.get_db_session(engine)

        existing_user = session.query(model_class).filter_by(
            id=model.id).first()

        existing_user.login_status = model.login_status
        session.commit()

        session.close()

    @staticmethod
    def logout_query():
        session = database.get_db_session(engine)
