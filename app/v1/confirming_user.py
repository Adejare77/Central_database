#!/usr/bin/python3
from app.models import User
from app import app
app.app_context().push()


class UserConfirmation:
    @staticmethod
    def confirm_user_info(username, email):
        # Query the database to confirm user info
        user = User.query.filter_by(username=username, email=email).first()
        if user:
            # User info is confirmed
            return True
        else:
            # User info is not found or does not match
            return False

print("=============================")
x = UserConfirmation()
print(x.confirm_user_info("Rashisky", "ade@gmail.com"))
print("=============================")
