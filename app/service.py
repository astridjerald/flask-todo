from models import ToDoModel, UserModel


class ToDoService:
    def __init__(self):
        self.model = ToDoModel()

    def create(self, params):
        return self.model.create(params)

    def update(self, item_id, params):
        return self.model.update(item_id, params)

    def delete(self, item_id):
        return self.model.delete(item_id)

    def list(self, params):
        response = self.model.list_items(f"AND UserId={params['UserId']}")
        return response


class UserService:
    def __init__(self):
        self.model = UserModel()

    def create(self, params):
        return self.model.create(params)

    def login(self, params):
        return self.model.login(params)
