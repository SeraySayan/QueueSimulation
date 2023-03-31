import random
import numpy as np
import matplotlib.pyplot as plt


class Customer:
    def __init__(self, id):
        self.id = id
        self.arrival_time = 0.0
        self.service_time = 0.0
        self.service_start_time = 0.0
        self.departure_time = 0.0  # leaving time from bank
        self.wait_time = 0.0  # time spent in queue

    def __repr__(self):
        return f"Customer {self.id}"


class Queue:
    def __init__(self):
        self.customers = []

    def enqueue(self, customer):
        self.customers.append(customer)
        # print customer details for debugging
        print(f"Customer {customer.id} details:")
        print(f"Arrival time: {customer.arrival_time:.2f}")
        print(f"Service time: {customer.service_time:.2f}")
        print(f"Service start time: {customer.service_start_time:.2f}")
        print(f"Departure time: {customer.departure_time:.2f}")
        print(f"Wait time: {customer.wait_time:.2f}")

    def dequeue(self):
        if not self.customers:
            return None

        customer = self.customers.pop(0)  # FIFO
        print("Dequeue method called. CUSTOMER SHOULD BE SERVED. (DEQUEUE)")
        print(f"Customer {customer.id} details:")
        print(f"Arrival time: {customer.arrival_time:.2f}")
        print(f"Service time: {customer.service_time:.2f}")
        print(f"Service start time: {customer.service_start_time:.2f}")
        print(f"Departure time: {customer.departure_time:.2f}")
        print(f"Wait time: {customer.wait_time:.2f}")
        return customer


def simulate_MMn(sim_time, arrival_rate, service_rate, num_servers):

    print(f"MMC queue simulation started.")
    queue = Queue()
    servers_busy = [False] * num_servers
    next_departure_time = [float('inf')] * num_servers
    arrival_interval = 1 / arrival_rate
    service_interval = 1 / service_rate
    next_arrival_time = random.expovariate(arrival_interval)
    time = 0  # current time
    queue_history = []  # queue length history
    total_customers = 0  # total number of customers in the system
    total_wait_time = 0  # total wait time
    total_customers_waiting = 0  # total number of customers waiting in queue
    next_service_start_time = [float('inf')] * num_servers
    service_time = 0.0  # total service time
    while time < sim_time:

        print(f"TIME: {time:.2f}")
        print(f"\nNEXT ARRIVAL TIME: {next_arrival_time:.2f}")
        print(f"NEXT DEPARTURE TIME: {next_departure_time}")

        # handle arrival event
        if time >= next_arrival_time:

            customer = Customer(total_customers + 1)
            customer.service_time = random.expovariate(service_interval) + 0.3
            service_time = service_time + customer.service_time
            customer.arrival_time = time

            served = False
            # check if any server is free
            for i in range(num_servers):
                if not servers_busy[i]:
                    servers_busy[i] = True
                    customer.service_start_time = customer.arrival_time
                    customer.departure_time = customer.service_start_time + customer.service_time
                    next_departure_time[i] = customer.departure_time
                    customer.wait_time = 0.0
                    next_service_start_time[i] = customer.departure_time

                    served = True
                    print(
                        "\n\nServer is not busy. CUSTOMER SHOULD BE SERVED immediately.")
                    print(
                        f"Next departure time for server {i}: {next_departure_time[i]:.2f}")

                    # print customer details for debugging
                    print(f"\n\nCustomer {customer.id} details:")
                    print(f"Arrival time: {customer.arrival_time:.2f}")
                    print(f"Service time: {customer.service_time:.2f}")
                    print(
                        f"Service start time: {customer.service_start_time:.2f}")
                    print(f"Departure time: {customer.departure_time:.2f}")
                    print(f"Wait time: {customer.wait_time:.2f}")
                    break
            # if all servers are busy
            if not served:

                if len(queue.customers) >= 1:
                    # print last customer in queue departure time
                    print(
                        f"Last customer in queue departure time: {queue.customers[-1].departure_time:.2f}")

                    for i in range(num_servers):
                        if (next_service_start_time[i] == queue.customers[-1].service_start_time):
                            next_service_start_time[i] = queue.customers[-1].departure_time
                            customer.service_start_time = min(
                                next_service_start_time)
                            break
                else:  # if queue is empty
                    customer.service_start_time = min(next_departure_time)

                customer.departure_time = customer.service_start_time + customer.service_time
                customer.wait_time = customer.service_start_time - customer.arrival_time
                print("Servers are busy. CUSTOMER SHOULD WAIT IN QUEUE. (ENQUEUE)")
                queue.enqueue(customer)

                total_customers_waiting += 1  # increment total number of customers waiting in queue
                total_wait_time += customer.wait_time   # increment total wait time
                print(
                    f"Total customers waiting: {total_customers_waiting}, total wait time: {total_wait_time:.2f}")

            total_customers += 1
            print(f"\n\nTotal customers in the system: {total_customers}")
            next_arrival_time = time + random.expovariate(arrival_rate)
            print(f"NEXT ARRIVAL TIME: {next_arrival_time:.2f}")

        # handle departure event
        for i in range(num_servers):
            if time >= next_departure_time[i]:
                customer = queue.dequeue()
                if customer is not None:  # if queue is not empty

                    next_departure_time[i] = customer.departure_time
                    print(
                        f"Next departure time for server {i}: {next_departure_time[i]:.2f}")

                else:  # if queue is empty
                    servers_busy[i] = False
                    next_departure_time[i] = float('inf')
                    print(f"Server {i} is now idle.")

        # append queue length to history
        queue_history.append(len(queue.customers))
        # print queue length history
        print(f"\n\nQUEUE HISTORY: {queue_history}")
        print(f"QUEUE LENGTH: {len(queue.customers)}")  # print queue length
        print(f"QUEUE CUSTOMERS: {queue.customers}")  # print queue customers
        time += 0.1
        print("*************************************************************************")

    avg_wait_time = total_wait_time / total_customers
    print(f"Average wait time: {avg_wait_time:.2f}")
    print("MMn queue simulation ended.")

    # calculate performance metrics
    avg_queue_length = np.mean(len(queue.customers))
    avg_service_time = np.mean(service_time)
    avg_wait_time = avg_queue_length / \
        (arrival_rate * num_servers - service_rate)
    avg_system_time = avg_service_time + avg_wait_time
    utilization = arrival_rate / (service_rate * num_servers)

    # print results
    print("Simulation results:")
    print(f"  Average queue length: {avg_queue_length:.2f}")

    # plot the queue length over time
    plt.plot(queue_history)
    plt.title("Queue length over time")
    plt.xlabel("Time (min)")
    plt.ylabel("Queue length")
    plt.show()


simulate_MMn(10, 5, 2, 3)
