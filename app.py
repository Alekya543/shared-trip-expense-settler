
"""Shared Trip Expense Settler with edit and delete extensions."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common import Store, form, heading, note, table, run, money, rupees

store = Store(
    Path(__file__).with_name('data.json'),
    {'people': [], 'expenses': []}
)


# 1. Calculate each participant's balance
def balances(people, expenses):
    result = {p: 0 for p in people}

    for expense in expenses:
        amount = expense['amount']
        members = expense['members']

        base, extra = divmod(amount, len(members))

        result[expense['payer']] += amount

        for index, member in enumerate(members):
            share = base + (1 if index < extra else 0)
            result[member] -= share

    return result


# 2. Generate suggested settlements
def settle(result):
    debtors = [[p, -v] for p, v in result.items() if v < 0]
    creditors = [[p, v] for p, v in result.items() if v > 0]

    transfers = []
    i, j = 0, 0

    while i < len(debtors) and j < len(creditors):
        amount = min(debtors[i][1], creditors[j][1])

        transfers.append([
            debtors[i][0],
            creditors[j][0],
            amount
        ])

        debtors[i][1] -= amount
        creditors[j][1] -= amount

        if debtors[i][1] == 0:
            i += 1

        if creditors[j][1] == 0:
            j += 1

    return transfers


# 3. Validate expense information
def validate_expense(data):
    people = store.data['people']

    description = data['description'].strip()
    payer = data['payer'].strip()
    amount = money(data['amount'])
    members = [p.strip() for p in data['members'].split(',')]

    if not description:
        raise ValueError('Enter an expense description.')

    if payer not in people:
        raise ValueError('Payer must be a registered participant.')

    if not members or any(not p or p not in people for p in members):
        raise ValueError('All sharing members must be registered participants.')

    # Check for duplicate beneficiaries
    if len(members) != len(set(members)):
        raise ValueError('A participant cannot be selected more than once.')

    return {
        'description': description,
        'payer': payer,
        'amount': amount,
        'members': members
    }


# 4. Display the application
def view():
    out = note(
        'Positive balance means receive money; '
        'negative balance means pay.'
    )

    out += heading('Register Participants')

    out += form(
        'people',
        [('people', 'Names separated by commas', 'text',
          ','.join(store.data['people']) or 'Asha,Balu,Chitra')],
        'Set participants'
    )

    out += note('Participants: ' + ', '.join(store.data['people']))

    out += heading('Add New Expense')

    out += form(
        'expense',
        [
            ('description', 'Expense description', 'text', 'Taxi'),
            ('payer', 'Paid by participant', 'text', ''),
            ('amount', 'Amount in rupees', 'text', '900.00'),
            ('members', 'Shared by names separated by commas', 'text', '')
        ],
        'Add expense'
    )

    # Display recorded expenses
    out += heading('Recorded Expenses')

    expense_rows = []

    for index, expense in enumerate(store.data['expenses'], start=1):
        expense_rows.append([
            str(index),
            expense['description'],
            expense['payer'],
            rupees(expense['amount']),
            ', '.join(expense['members'])
        ])

    out += table(
        ['No.', 'Description', 'Payer', 'Amount', 'Shared by'],
        expense_rows
    )

    # Edit expense form
    out += heading('Edit an Expense')

    out += note(
        'Enter the expense number shown in the Recorded Expenses table.'
    )

    out += form(
        'edit',
        [
            ('index', 'Expense number', 'number', '1'),
            ('description', 'New description', 'text', 'Taxi'),
            ('payer', 'New payer', 'text', ''),
            ('amount', 'New amount in rupees', 'text', '900.00'),
            ('members', 'New sharing members separated by commas', 'text', '')
        ],
        'Update expense'
    )

    # Delete expense form
    out += heading('Delete an Expense')

    out += form(
        'delete',
        [('index', 'Expense number to delete', 'number', '1')],
        'Delete expense'
    )

    # Display balances
    result = balances(
        store.data['people'],
        store.data['expenses']
    )

    out += heading('Balances')

    out += table(
        ['Person', 'Net balance'],
        [(p, rupees(v)) for p, v in result.items()]
    )

    # Display settlements
    out += heading('Suggested Settlements')

    out += table(
        ['Who pays', 'Who receives', 'Amount'],
        [(a, b, rupees(c)) for a, b, c in settle(result)]
    )

    return out


# 5. Process user actions
def handle(data):

    action = data['action']

    if action == 'people':

        if store.data['expenses']:
            raise ValueError(
                'Participants cannot be replaced after recording expenses.'
            )

        people = [p.strip() for p in data['people'].split(',')]

        if len(people) < 2 or '' in people or len(set(people)) != len(people):
            raise ValueError('Use at least two unique nonempty names.')

        store.data['people'] = people

    elif action == 'expense':

        expense = validate_expense(data)
        store.data['expenses'].append(expense)

    elif action == 'edit':

        index = int(data['index']) - 1

        if index < 0 or index >= len(store.data['expenses']):
            raise ValueError('Invalid expense number.')

        updated_expense = validate_expense(data)

        store.data['expenses'][index] = updated_expense

    elif action == 'delete':

        index = int(data['index']) - 1

        if index < 0 or index >= len(store.data['expenses']):
            raise ValueError('Invalid expense number.')

        store.data['expenses'].pop(index)

    else:
        raise ValueError('Unknown action.')

    # Save every successful change
    store.save()


# 6. Start the application
if __name__ == '__main__':
    run(
        'Shared Trip Expense Settler',
        view,
        handle
    )

