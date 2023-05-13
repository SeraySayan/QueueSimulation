import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# Use a service account
cred = credentials.Certificate(
    'firestore491test-firebase-adminsdk-7l56g-2cd92c9238.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# All customer data can be read
customers_ref = db.collection(u'Tickets')
docs = customers_ref.stream()

total_customer = 0
total_wait_time = 0
total_service_time = 0
total_arrival_time = 0
for doc in docs:
    # print(f'{doc.id} => {doc.to_dict()}')
    total_customer += 1

    wait_time = doc.to_dict()['total_waited_time']
    # last char deletion
    wait_time = wait_time[:-1]
    total_wait_time += float(wait_time)

    arrival_time = str(doc.to_dict()['date_time'])
    arrival_timestamp = datetime.fromisoformat(arrival_time)
    total_arrival_time += arrival_timestamp.timestamp()
    process_time = doc.to_dict()['total_process_time']

    if process_time is not None:
        # last char deletion
        process_time = process_time[:-1]
        total_service_time += float(process_time)

    print("-------------------")
    print("Customer ID: ", doc.id)
    print("Arrival Time: ", arrival_time)
    print("Wait Time: ", wait_time)
    print("Process Time: ", process_time)


print("-------------------")
