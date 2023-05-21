class LookupContext:
    pass

class Global(LookupContext):
    pass

class User(LookupContext):
    def __init__(self, user_id):
        self.user_id = user_id

    def get_user_id(self):
        return self.user_id

class Device(LookupContext):
    def __init__(self, device_id):
        self.device_id = device_id

    def get_device_id(self):
        return self.device_id
