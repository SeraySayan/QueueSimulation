class Queue:
    def __init__(self):
        self.customers = []

    def isEmpty(self):
        return self.customers == []

    def enqueue(self, customer):
        # adding customer with priority
        if self.isEmpty():
            self.customers.append(customer)
        else:
            for i in range(len(self.customers)):
                if customer.priority < self.customers[i].priority:
                    self.customers.insert(i, customer)
                    print("Enqueue priority ")
                    priorities = []
                    for i in range(len(self.customers)):
                        priorities.append(self.customers[i].priority)
                    print(priorities)

                    for i in range(len(self.customers)):
                        self.customers[i].print_customer_details()
                    return
            self.customers.append(customer)
            print("Enqueue normal")

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
