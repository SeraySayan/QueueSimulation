from customer import Customer


class Server:
    def __init__(self, id):
        self.id = id
        self.customers = []
        self.is_busy = False
        self.current_departure_time = float('inf')
        self.last_departure_time = float('inf')

    def is_busy(self):
        return self.is_busy

    def append_customer(self, customer):
        self.customers.append(customer)
        self.last_departure_time = customer.departure_time

    def pop_customer(self):
        if not self.customers:
            return None

        customer = self.customers.pop(0)  # FIFO

    def change_busy_status(self):
        self.is_busy = not self.is_busy

    def print_server_details(self):
        print(f"Server {self.id} details:")
        print(f"Customers: {self.customers}")
        print(f"Is busy: {self.is_busy}")
        print(f"Current departure time: {self.current_departure_time}")
        print(f"Last departure time: {self.last_departure_time}")

    def serve_customer(self, customer):
        self.customers.append(customer)
        self.is_busy = True
        self.current_departure_time = customer.departure_time
        self.last_departure_time = customer.departure_time
