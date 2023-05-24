from src.examples.program.traccar.model.user import User

class ServiceAccountUser(User):

    ID = 9000000000000000000

    def __init__(self):
        User.setId(ServiceAccountUser.ID)
        User.setName("Service Account")
        User.setEmail("none")
        User.setAdministrator(True)
