

class Server:
    def __init__(self, id):
        self.id = id
        self.is_available = True

    def is_available(self):
        return self.is_available

    def change_busy_status(self):
        self.is_available = not self.is_available

    def print_server_details(self):
        print(f"Server {self.id} details:")
        print(f"Customers: {self.customers}")
        print(f"Is busy: {self.is_busy}")
        print(f"Current departure time: {self.current_departure_time}")
        print(f"Last departure time: {self.last_departure_time}")
