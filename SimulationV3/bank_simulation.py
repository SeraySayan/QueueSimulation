from customer import Customer
from server import Server
from bankqueue import Queue
import random
import numpy as np


class BankSimulation:
    servers = []
    queue = []
    list_customers = []
    after_service_start_list = []
    total_served_customers = 0
    total_service_time = 0
    total_wait_time = 0
    total_waiting_customers = 0
    num_servers = 0
    arrival_rate = 0
    service_rate = 0
    simulation_customer_number = 0
    simulation_time = 0
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

    def initialize_customers(self):
        for i in range(self.simulation_customer_number):
            if i == 0:
                arrival_time = np.random.exponential(
                    scale=1 / self.arrival_rate)
            else:
                arrival_time = np.random.exponential(
                    scale=1 / self.arrival_rate) + self.list_customers[i-1].arrival_time
            service_time = np.random.exponential(scale=1 / self.service_rate)
            self.list_customers.append(
                Customer(i + 1, arrival_time, service_time))
        self.list_customers.sort(key=lambda x: x.arrival_time)

    def initialize_simulation(self):
        self.initialize_servers()
        self.initialize_queue()
        self.initialize_customers()

    def all_servers_busy(self):
        for i in range(len(self.servers)):
            if self.servers[i].is_available:
                return False
        return True

    def calculate_metrics(self):
        print(f"\n**********************************************************\n")

        print("Calculating metrics...")
        print(f"Total customers: {self.total_served_customers}")
        print(f"Total service time: {self.total_service_time}")
        print(f"Total wait time: {self.total_wait_time}")
        print(f"Total waiting customers: {self.total_waiting_customers}")
        print(f"\n**********************************************************\n")
        print(
            f"Average service time: {self.total_service_time/self.total_served_customers}")
        if self.total_waiting_customers == 0:
            print("Average wait time: 0")
        else:
            print(
                f"Average wait time: {self.total_wait_time/self.total_waiting_customers}"
            )

        print(
            f"Average number of customers in the queue (Not sure): {(self.total_wait_time/self.simulation_time)}"
        )
        # Average number of customers in the system
        print(
            f"Average number of customers in the system (Not sure): {self.total_service_time/self.simulation_time}"
        )
        print(f"Simulation Time: {self.simulation_time}")
        print(f"Total exit time: {self.total_exit_time}")

        print(f"\n**********************************************************\n")

        rho = self.arrival_rate / (self.num_servers * self.service_rate)
        print(f"Rho : {rho}")

        print(f"Gelmesi gereken result : {rho/(1-rho)}")

        print(f"Alinan sonuc: {self.total_exit_time/self.simulation_time}")

        print(f"\n**********************************************************\n")

        # waiting time in the system
        print(
            f"Waiting time in the system: {self.total_wait_time+self.total_service_time}"
        )

        # average waiting time in the system
        print(
            f"Average waiting time in the system (Ws OK): {(self.total_wait_time+self.total_service_time)/self.total_served_customers}"
        )

        # average number of customers in the system
        print(
            f"Average number of customers in the system (Ls) (OK): {(self.total_service_time/self.simulation_time)+(self.total_wait_time/self.simulation_time)}"
        )

        # average waiting time in the queue
        print(
            f"Average waiting time in the queue (Wq)(ok): {(self.total_wait_time/self.total_waiting_customers)}"
        )

        # average number of customers in the queue
        print(
            f"Average number of customers in the queue (Lq): {self.total_wait_time/self.simulation_time}"
        )


def simulation(simulation_customer_number, arrival_rate, service_rate, num_servers):
    bankSimulation = BankSimulation(
        simulation_customer_number, arrival_rate, service_rate, num_servers
    )
    bankSimulation.initialize_simulation()
    print("Simulation started.")
    arrived_customer_number = 0
    print(bankSimulation.list_customers)
    for i in range(len(bankSimulation.list_customers)):
        bankSimulation.list_customers[i].print_customer_details()
    print(bankSimulation.simulation_customer_number)
    print(bankSimulation.total_served_customers)
    print(bankSimulation.after_service_start_list)
    print(bankSimulation.queue)


if __name__ == "__main__":
    simulation(10, 3, 4, 1)
