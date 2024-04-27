from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.v1.central_db_tables import Primary_owner, Other_users
from app.v1.user_db import CreateClassTable, Database


class Account(Database):
    def __init__(self, username) -> None:
        super().__init__(username)


    @property
    def other_users(self):
        users = self.session.query(Other_users.username).filter_by(owner=self.user)
        users = [user for user in users]
        print(users)

    def add_permissions(self, db):
        pass

    @property
    def get_permissions(self):
        if self.is_owner == Primary_owner:
            return ['ALL']
        permissions = self.session.query(Other_users.permissions).filter_by(username=self.user).one()
        # permissions[0] converts sqlalchemy instance to dict
        operations = permissions[0][self.db]
        return operations
