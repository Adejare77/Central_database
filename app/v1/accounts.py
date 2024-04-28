#!/usr/bin/env python3

from app.v1.central_db_tables import Primary_owner, Other_users
from app.v1.filters import Filter

class Account(Filter):
    def __init__(self, username, db, tables, columns=None) -> None:
        super().__init__(username, db)
        self.tables = tables
        self.columns = columns

    @property
    def other_users(self):
        users = self.session.query(Other_users.username).filter_by(owner=self.user)
        users = [user for user in users]
        print(users)

    def add_permissions(self, db):
        pass

    @property
    def permissions(self):
        {
            "READ": self.all_rows(self.tables, self.columns),
            "DELETE": self.all_rows(self.tables, self.columns)
        }
        if self.is_owner == Primary_owner:
            return ['ALL']
        permissions = self.session.query(Other_users.permissions).filter_by(username=self.user).one()
        # permissions[0] converts sqlalchemy instance to dict
        operations = permissions[0][self.db]
        return operations
