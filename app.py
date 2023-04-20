import datetime
import time
import json
import os
from flask import Flask, render_template, jsonify, request, url_for, redirect
from functions import generators

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    current_year = datetime.datetime.now().year
    return render_template('index.html', current_year=current_year)


@app.route('/import_records')
def import_records():
    current_year = datetime.datetime.now().year

    return render_template('import_records.html', current_year=current_year)


@app.route('/complete_reconciliation')
def complete_reconciliation():
    current_year = datetime.datetime.now().year

    with open('json_files/banking_records.json', 'r') as f:
        # read the list from the file in JSON format
        banking_records = json.load(f)

    with open('json_files/similar_system_records.json', 'r') as f:
        # read the list from the file in JSON format
        system_records = json.load(f)

    return render_template('complete_reconciliation.html', banking_records=banking_records[:15],
                           current_year=current_year,
                           system_records=system_records[:15])


@app.route('/generate_records')
def generate_records():
    records = generators.generate_banking_records()
    return jsonify(records)


@app.route('/print_test')
def print_test():
    return "This is a print test"


@app.route('/run_reconciliation')
def run_reconciliation():
    with open('json_files/banking_records.json', 'r') as f:
        # read the list from the file in JSON format
        banking_records = json.load(f)

    with open('json_files/similar_system_records_missing.json', 'r') as f:
        # read the list from the file in JSON format
        system_records = json.load(f)

    bank_set = {
        (record['memo'], record['credit_amount'], record['debit_amount'], record['balance_after'], record['timestamp'])
        for record in banking_records}

    system_set = {
        (record['memo'], record['credit_amount'], record['debit_amount'], record['balance_after'], record['timestamp'])
        for record in system_records}

    unmatched_bank = [dict(zip(['memo', 'credit_amount', 'debit_amount', 'balance_after', 'timestamp'], record)) for
                      record in bank_set - system_set]
    unmatched_system = [dict(zip(['memo', 'credit_amount', 'debit_amount', 'balance_after', 'timestamp'], record)) for
                        record in system_set - bank_set]

    save_reconciliation = [{"unmatched_bank": unmatched_bank, "unmatched_system": unmatched_system}]

    reconciliation_id = str(int(datetime.datetime.now().timestamp()))

    file_path = 'json_files/reports/' + reconciliation_id + '.json'

    # create the directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as f:
        # write the list to the file in JSON format
        json.dump(save_reconciliation, f)

    bank_closing_balance = banking_records[-1]['balance_after']
    system_closing_balance = system_records[-1]['balance_after']
    unmatched_bank_len = len(unmatched_bank)
    unmatched_system_len = len(unmatched_system)

    time.sleep(5)

    return {'reconciliation_id': reconciliation_id, 'bank_closing_balance': bank_closing_balance,
            'unmatched_bank_len': unmatched_bank_len,
            'system_closing_balance': system_closing_balance, 'unmatched_system_len': unmatched_system_len}


@app.route('/submit_reconciliation', methods=['POST'])
def submit_reconciliation():
    reconciliation = {"date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      "bank_closing_balance": request.form['bank_closing_balance'],
                      "system_closing_balance": request.form['system_closing_balance'],
                      "balance_difference": request.form['balance_difference'],
                      "performed_by": request.form['performed_by'], "bank_name": request.form['bank_name'],
                      "memo": request.form['memo'], "reconciliation_id": request.form['reconciliation_id']}

    file_path = 'json_files/reports.json'

    # create the directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w') as f:
        # write the list to the file in JSON format
        json.dump(reconciliation, f)

    return redirect(url_for('index'))


if __name__ == '__main__':
    # app.run()
    app.run(debug=True, use_reloader=True)
