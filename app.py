from flask import Flask, render_template, jsonify
from functions import generators
import json, time, random, datetime

app = Flask(__name__)


@app.route('/')
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

    with open('banking_records.json', 'r') as f:
        # read the list from the file in JSON format
        banking_records = json.load(f)

    with open('similar_system_records.json', 'r') as f:
        # read the list from the file in JSON format
        system_records = json.load(f)

    return render_template('complete_reconciliation.html', banking_records=banking_records[:15], current_year=current_year,
                           system_records=system_records[:15])


@app.route('/generate_records')
def generate_records():
    records = generators.generate_banking_records()
    return jsonify(records)


@app.route('/print_test')
def print_test():
    return "This is a print test"


@app.route('/long_task')
def long_task():
    # Simulate a long task by sleeping for 10 seconds
    time.sleep(10)

    # Return 1 or 0 randomly
    result = random.randint(0, 1)
    return jsonify(result=result)


if __name__ == '__main__':
    # app.run()
    app.run(debug=True, use_reloader=True)
