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
        table_data = session.query(table_name).filter_by(is_deleted=False).all()
        return table_data

    @staticmethod
    def soft_delete_query(table_name, entity_id: int):
        """Perform a soft delete by setting `is_deleted=True`."""
        session = database.get_db_session(engine)
        table_data = (
            session.query(table_name).filter_by(id=entity_id, is_deleted=False).first()
        )
        if table_data:
            table_data.is_deleted = True
            session.commit()
        return table_data

    # #
    @staticmethod
    def get_by_id_query(table_name, entity_id: int):
        """Retrieve an entity by its ID, excluding soft-deleted entities."""
        session = database.get_db_session(engine)
        table_data = (
            session.query(table_name).filter_by(id=entity_id, is_deleted=False).first()
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
