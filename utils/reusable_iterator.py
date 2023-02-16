class ReusableIter:
    def __init__(self, get_data):
        self.get_data = get_data

    def __iter__(self):
        return self.get_data()
