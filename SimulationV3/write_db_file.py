from db_config import db
import os


def retrieve_data():

    # Mevcut çalışma dizini
    current_directory = os.getcwd()

    # Dosya adı
    filename = "output_file.txt"

    # Tam dosya yolunu oluştur
    output_file = os.path.join(current_directory, filename)

    no_of_servers = 0
    # Get the number of servers from Employees collection then write to the file
    employees_ref = db.collection(u'Employees')
    docs = employees_ref.stream()
    for doc in docs:
        no_of_servers += 1
    print("No of servers: ", no_of_servers)
# Get the data of customers from Tickets collection then write to the file
    customers_ref = db.collection(u'Tickets')
    docs = customers_ref.stream()
    total_customers = 0

    with open(output_file, 'w') as file:
        for doc in docs:
            customer_id = doc.id
            arrival_time = doc.to_dict()['date_time']
            process_time = doc.to_dict()['total_process_time']
            priority = doc.to_dict()['priority']

            file.write("Customer ID:{}\n".format(customer_id))
            file.write("Arrival Time:{}\n".format(arrival_time))
            file.write("Process Time:{}\n".format(process_time))
            file.write("Priority:{}\n".format(priority))

            print_customer_details(
                customer_id, arrival_time, process_time, priority)
            total_customers += 1
        file.write("Total Customers: {}\n".format(total_customers))
        file.write("No of servers: {}\n".format(no_of_servers))

    print("Data has been written to the file: {}".format(output_file))
    print("Total Customers: ", total_customers)
    print("No of servers: ", no_of_servers)


def print_customer_details(doc_id, arrival_time, process_time, priority):
    print("-------------------")
    print("Customer ID: ", doc_id)
    print("Arrival Time: ", arrival_time)
    print("Process Time: ", process_time)
    print("Priority: ", priority)
    print("-------------------")


def main():
    retrieve_data()


if __name__ == "__main__":
    main()
