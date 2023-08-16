from django.contrib.auth.models import User


class MyUser(User):

    def __str__(self):
        return " ".join((self.first_name, self.last_name))
