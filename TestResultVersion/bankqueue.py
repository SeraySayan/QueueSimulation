class Queue:
    def __init__(self):
        self.customers = []

    def isEmpty(self):
        return self.customers == []

    def enqueue(self, customer):
        self.customers.append(customer)

    def dequeue(self):
        if not self.customers:
            return None

        customer = self.customers.pop(0)  # FIFO
        print("Dequeue method called. CUSTOMER SHOULD BE SERVED. (DEQUEUE)")
        return customer

    def size(self):
        return len(self.customers)

    def print_queue_details(self):
        print(f"Queue details:")
        print(f"Queue: {self.customers}")
        print(f"Queue size: {self.size()}")
