class FIRSession:

    def __init__(self):

        self.data = {}

    def update(self, new_data):

        if isinstance(new_data, dict):

            self.data.update(new_data)

    def get_data(self):

        return self.data


if __name__ == "__main__":

    session = FIRSession()

    session.update({
        "accused_name": "Ravi"
    })

    session.update({
        "victim_name": "Arjun"
    })

    print(
        session.get_data()
    )