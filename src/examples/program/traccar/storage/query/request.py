class Request:
    def __init__(self, columns=None, condition=None, order=None):
        self.columns = columns
        self.condition = condition
        self.order = order

    def get_columns(self):
        return self.columns

    def get_condition(self):
        return self.condition

    def get_order(self):
        return self.order

