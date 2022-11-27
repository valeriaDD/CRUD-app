import itertools

from database.users import users


class User:
    id_iter = itertools.count()

    def __init__(self, name, surname, age):
        super(User, self).__init__()
        self.id = next(User.id_iter) + 1
        self.name = name
        self.surname = surname
        self.age = age

    def save(self):
        users.append(self.get())

    def get(self):
        return {'id': self.id, 'name': self.name, 'surname': self.surname, 'age': self.age}
