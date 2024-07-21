from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)

transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

@app.route('/')
def get_transactions():
    return render_template('transactions.html', transactions=transactions)

@app.route('/add', methods=['POST', 'GET'])
def add_transaction():
    if request.method == 'POST':
        transaction = {                                  # Create a new transaction object using form field values
            'id': len(transactions) + 1,                 # Generate a new ID based on the current length of the transactions list
            'date': request.form['date'],                # Get the 'date' field value from the form
            'amount': float(request.form['amount'])      # Get the 'amount' field value from the form and convert it to a float
        }
        transactions.append(transaction)                 # Append the new transaction to the transactions list
        return redirect(url_for('get_transactions'))
    return render_template('form.html')

@app.route('/edit/<int:transaction_id>', methods = ['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        date = request.form['date']
        amount = float(request.form['amount'])

        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
        return redirect(url_for('get_transactions'))
    
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template('edit.html', transaction=transaction)
    
    return {'message': 'Transaction not found'}, 404

@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for('get_transactions'))

if __name__ == '__main__':
    app.run(debug=True)
    