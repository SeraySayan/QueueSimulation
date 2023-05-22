import random


class Customer:
    def __init__(self, id, arrival_time, service_time, priority):
        self.id = id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.service_start_time = 0.0  # leaving time from queue
        self.departure_time = 0.0  # leaving time from bank
        self.wait_time = 0.0  # time spent in queue
        self.priority = priority  # priority of customer
        self.server_no = 0

    def __repr__(self):
        return f"Customer {self.id}"

    def print_customer_details(self):
        print(f"\n\nCustomer {self.id} details:")
        print(f"Arrival time: {self.arrival_time:.2f}")
        print(f"Service time: {self.service_time:.2f}")
        print(f"Service start time: {self.service_start_time:.2f}")
        print(f"Departure time: {self.departure_time:.2f}")
        print(f"Wait time: {self.wait_time:.2f}")
        print(f"Priority: {self.priority}")
        print(f"Server no: {self.server_no}")
