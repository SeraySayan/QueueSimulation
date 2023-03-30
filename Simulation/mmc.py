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

    def enqueue(self, customer, time):
        customer.arrival_time = time
        self.customers.append(customer)
        print("Enqueue method called customer should wait in the queue.")
        print(f"Customer {customer.id} arrived at time {time:.2f}.")

    def dequeue(self, time):
        if not self.customers:
            return None

        customer = self.customers.pop(0)
        print("Dequeue method called. CUSTOMER SHOULD BE SERVED.")
        print(
            f"Customer {customer.id} waited {customer.wait_time:.2f} seconds and service start at time {customer.service_start_time:.2f}.")

        return customer


def simulate_MMn(sim_time, arrival_rate, service_rate, num_servers):
    print(f"MMC queue simulation started.")

    queue = Queue()
    servers_busy = [False] * num_servers
    next_departure_time = [float('inf')] * num_servers
    arrival_interval = 1 / arrival_rate
    service_interval = 1 / service_rate
    next_arrival_time = random.expovariate(arrival_interval)
    print(f"Next arrival time: {next_arrival_time:.2f}")
    time = 0
    queue_history = []
    total_customers = 0
    total_wait_time = 0
    total_customers_waiting = 0
    next_service_start_time = [float('inf')] * num_servers
    service_time = 0.0
    while time < sim_time:
        print(f"Time: {time:.2f}")
        print(f"Next arrival time: {next_arrival_time:.2f}")
        print(f"Next departure time: {next_departure_time}")

        # handle arrival event
        if time >= next_arrival_time:
            customer = Customer(total_customers + 1)
            customer.service_time = random.expovariate(service_interval) + 0.3
            service_time = service_time + customer.service_time
            print(
                f"Customer {customer.id} service time: {customer.service_time:.2f}")

            customer.arrival_time = time
            print(
                f"Customer {customer.id} arrival time: {customer.arrival_time:.2f}")

            served = False
            for i in range(num_servers):
                if not servers_busy[i]:
                    servers_busy[i] = True
                    next_departure_time[i] = time + customer.service_time
                    customer.service_start_time = time
                    customer.departure_time = next_departure_time[i]
                    customer.wait_time = 0
                    next_service_start_time[i] = customer.departure_time
                    print(
                        f"Next departure time for server {i}: {next_departure_time[i]:.2f}")
                    served = True
                    print("server is not busy. CUSTOMER SHOULD BE SERVED immediately.")
                    # print customer details for debugging
                    print(f"Customer {customer.id} details:")
                    print(f"Arrival time: {customer.arrival_time:.2f}")
                    print(f"Service time: {customer.service_time:.2f}")
                    print(
                        f"Service start time: {customer.service_start_time:.2f}")
                    print(f"Departure time: {customer.departure_time:.2f}")
                    print(f"Wait time: {customer.wait_time:.2f}")
                    break

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

                    print(
                        f"Next service start time: {next_service_start_time}")
                    print(
                        f"Service start time: {customer.service_start_time:.2f}")

                else:  # if queue is empty
                    customer.service_start_time = min(next_departure_time)
                    print(
                        f"Service start time: {customer.service_start_time:.2f}")

                customer.departure_time = customer.service_start_time + customer.service_time
                print(f"Departure time: {customer.departure_time:.2f}")

                customer.wait_time = customer.service_start_time - customer.arrival_time
                print(f"Wait time: {customer.wait_time:.2f}")

                queue.enqueue(customer, time)
                total_customers_waiting += 1
                total_wait_time += customer.wait_time
                print("server is busy. CUSTOMER SHOULD WAIT IN QUEUE.")
                # print customer details for debugging
                print(f"Customer {customer.id} details:")
                print(f"Arrival time: {customer.arrival_time:.2f}")
                print(f"Service time: {customer.service_time:.2f}")
                print(f"Service start time: {customer.service_start_time:.2f}")
                print(f"Departure time: {customer.departure_time:.2f}")
                print(f"Wait time: {customer.wait_time:.2f}")

                print(
                    f"Total customers waiting: {total_customers}, total wait time: {total_wait_time:.2f}")

            total_customers += 1
            print(f"Total customers: {total_customers}")
            next_arrival_time = time + random.expovariate(arrival_rate)
            print(f"Next arrival time: {next_arrival_time:.2f}")

        # handle departure event
        for i in range(num_servers):
            if time >= next_departure_time[i]:
                customer = queue.dequeue(time)
                if customer is not None:  # if queue is not empty

                    next_departure_time[i] = time + customer.service_time
                    print(
                        f"Next departure time for server {i}: {next_departure_time[i]:.2f}")

                else:  # if queue is empty
                    servers_busy[i] = False
                    next_departure_time[i] = float('inf')
                    print(f"Server {i} is now idle.")

        queue_history.append(len(queue.customers))
        print(f"Queue history: {queue_history}")
        # print(f"Queue history: {queue_history}")
        print(f"Queue length: {len(queue.customers)}")
        print(f"Queue customers: {queue.customers}")
        time += 0.1

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
