from customer import Customer
from server import Server
from bankqueue import Queue
import random
import numpy as np


class BankSimulation:
    servers = []
    queue = []
    total_customers = 0
    total_service_time = 0
    total_wait_time = 0
    total_waiting_customers = 0
    num_servers = 0
    arrival_rate = 0
    service_rate = 0
    simulation_customer_number = 0
    simülation_time = 0
    total_idle_time = 0
    total_entry_time = 0
    total_exit_time = 0

    def __init__(
        self, simulation_customer_number, arrival_rate, service_rate, num_servers
    ):
        self.num_servers = num_servers
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.simulation_customer_number = simulation_customer_number

    def initialize_servers(self):
        for i in range(self.num_servers):
            self.servers.append(Server(i + 1))

    def initialize_queue(self):
        self.queue = Queue()

    def find_server(self):
        server_index = 0
        available_server = self.servers[0].last_departure_time
        for i in range(1, len(self.servers)):
            if self.servers[i].last_departure_time < available_server:
                available_server = self.servers[i].last_departure_time
                server_index = i

        return server_index

    def find_min_server(self):
        server_index = 0
        available_server = self.servers[0].current_departure_time
        for i in range(1, len(self.servers)):
            if self.servers[i].current_departure_time < available_server:
                available_server = self.servers[i].current_departure_time
                server_index = i

        return server_index

    def initialize_simulation(self):
        self.initialize_servers()
        self.initialize_queue()

    def calculate_metrics(self):
        print(f"\n**********************************************************\n")

        print("Calculating metrics...")
        print(f"Total customers: {self.total_customers}")
        print(f"Total service time: {self.total_service_time}")
        print(f"Total wait time: {self.total_wait_time}")
        print(f"Total waiting customers: {self.total_waiting_customers}")
        print(f"\n**********************************************************\n")
        print(f"Average service time: {self.total_service_time/self.total_customers}")
        if self.total_waiting_customers == 0:
            print("Average wait time: 0")
        else:
            print(
                f"Average wait time: {self.total_wait_time/self.total_waiting_customers}"
            )

        print(
            f"Average idle time (Not sure): {self.total_idle_time/(self.simülation_time/0.01)}"
        )
        print(
            f"Average number of customers in the queue (Not sure): {(self.total_wait_time/self.simülation_time)}"
        )
        # Average number of customers in the system
        print(
            f"Average number of customers in the system (Not sure): {self.total_service_time/self.simülation_time}"
        )
        print(f"Simulation Time: {self.simülation_time}")

        print(f"\n**********************************************************\n")

        rho = self.arrival_rate / (self.num_servers * self.service_rate)
        print(f"Rho : {rho}")

        print(f"Gelmesi gereken result : {rho/(1-rho)}")

        print(f"Alinan sonuc: {self.total_exit_time/self.simülation_time}")

        print(f"\n**********************************************************\n")

        # waiting time in the system
        print(
            f"Waiting time in the system: {self.total_wait_time+self.total_service_time}"
        )

        # average waiting time in the system
        print(
            f"Average waiting time in the system (Ws OK): {(self.total_wait_time+self.total_service_time)/self.total_customers}"
        )

        # average number of customers in the system
        print(
            f"Average number of customers in the system (Ls) (OK): {(self.total_service_time/self.simülation_time)+(self.total_wait_time/self.simülation_time)}"
        )

        # average waiting time in the queue
        print(
            f"Average waiting time in the queue (Wq)(ok): {(self.total_wait_time/self.total_waiting_customers)}"
        )

        # average number of customers in the queue
        print(
            f"Average number of customers in the queue (Lq): {self.total_wait_time/self.simülation_time}"
        )

        # Probablity of 0 jobs in the system with calculating idle time
        print(
            f"Probablity of 0 jobs in the system with calculating idle time (Not Sure): {self.total_idle_time/self.simülation_time}"
        )


def simulate_MMn(simulation_customer_number, arrival_rate, service_rate, num_servers):
    bankSimulation = BankSimulation(
        simulation_customer_number, arrival_rate, service_rate, num_servers
    )
    bankSimulation.initialize_simulation()
    next_arrival_time = np.random.exponential(scale=1 / bankSimulation.arrival_rate)
    # print(f"Next arrival time: {next_arrival_time}")

    while bankSimulation.total_customers < bankSimulation.simulation_customer_number:
        # print(f"Simulation time: {bankSimulation.simülation_time}")

        # handle departure event
        for i in range(len(bankSimulation.servers)):
            if (
                bankSimulation.simülation_time
                >= bankSimulation.servers[i].current_departure_time
            ):
                customer = bankSimulation.queue.dequeue()
                bankSimulation.servers[i].pop_customer()

                if customer is not None:  # if queue is not empty
                    # print("Customer should be removed from queue. (DEPARTURE)")

                    bankSimulation.servers[
                        i
                    ].current_departure_time = customer.departure_time

                    # customer.print_customer_details()
                    # bankSimulation.queue.print_queue_details()

                    # print("başka müşteri geçti servera")
                    # bankSimulation.servers[i].print_server_details()

                else:  # if queue is empty
                    bankSimulation.servers[i].is_busy = False
                    bankSimulation.servers[i].current_departure_time = float("inf")

                    print(f"Server {i+1} is now idle.")
                    bankSimulation.total_idle_time += 1
                    # bankSimulation.servers[i].print_server_details()

        # handle arrival event
        if next_arrival_time <= bankSimulation.simülation_time:
            bankSimulation.total_customers += 1
            # create customer
            customer = Customer(
                bankSimulation.total_customers,
                next_arrival_time,
                np.random.exponential(scale=1 / bankSimulation.service_rate),
            )

            served = False
            for i in range(len(bankSimulation.servers)):
                if not bankSimulation.servers[i].is_busy:
                    # change server status
                    bankSimulation.servers[i].is_busy = True
                    # update stats
                    customer.service_start_time = customer.arrival_time
                    customer.wait_time = 0
                    customer.departure_time = (
                        customer.service_start_time + customer.service_time
                    )
                    bankSimulation.total_exit_time += (
                        customer.departure_time - customer.arrival_time
                    )
                    # serve customer
                    bankSimulation.servers[
                        i
                    ].current_departure_time = customer.departure_time
                    bankSimulation.servers[
                        i
                    ].last_departure_time = customer.departure_time
                    bankSimulation.servers[i].customers.append(customer)
                    served = True
                    customer.print_customer_details()
                    # bankSimulation.servers[i].print_server_details()
                    break

            if not served:
                # find server with shortest queue
                i = bankSimulation.find_server()

                # add customer to queue
                customer.service_start_time = bankSimulation.servers[
                    i
                ].last_departure_time
                customer.wait_time = customer.service_start_time - customer.arrival_time
                customer.departure_time = (
                    customer.service_start_time + customer.service_time
                )
                bankSimulation.total_exit_time += (
                    customer.departure_time - customer.arrival_time
                )

                bankSimulation.servers[i].last_departure_time = customer.departure_time
                bankSimulation.queue.customers.append(customer)
                bankSimulation.servers[i].customers.append(customer)
                # print("Customer added to queue")
                # customer.print_customer_details()
                # bankSimulation.servers[i].print_server_details()
                # bankSimulation.queue.print_queue_details()

                bankSimulation.total_wait_time += customer.wait_time
                bankSimulation.total_waiting_customers += 1

            bankSimulation.total_service_time += customer.service_time
            next_arrival_time = bankSimulation.simülation_time + np.random.exponential(
                scale=1 / bankSimulation.arrival_rate
            )
            # print(f"Next arrival time: {next_arrival_time}")

        bankSimulation.simülation_time += 0.001
    # calculate and print stats
    bankSimulation.calculate_metrics()


simulate_MMn(1024, 5, 8, 1)
