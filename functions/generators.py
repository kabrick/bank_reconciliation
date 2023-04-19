import json
import random
from datetime import datetime, timedelta
import random
import datetime


def generate_banking_records():
    memo = ["Payment", "Withdrawal", "Deposit", "Transfer"]
    records = []
    balance = 0
    timestamp = datetime.datetime(2020, 1, 1)

    for i in range(10000):
        record = {'memo': random.choice(memo)}

        if random.choice([True, False]) or balance < 1:
            record['credit_amount'] = round(random.uniform(10000, 10000000))
            record['debit_amount'] = 0
            balance += record['credit_amount']
        else:
            record['credit_amount'] = 0
            record['debit_amount'] = round(random.uniform(10000, 10000000))
            balance -= record['debit_amount']

        record['balance_after'] = round(balance)
        record['timestamp'] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        timestamp += datetime.timedelta(seconds=random.randint(1800, 10800))
        records.append(record)

    with open('banking_records.json', 'w') as f:
        # write the list to the file in JSON format
        json.dump(records, f)

    with open('similar_system_records.json', 'w') as f:
        # write the list to the file in JSON format
        json.dump(records, f)

    return "Complete"

