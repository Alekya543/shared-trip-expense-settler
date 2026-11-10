# Shared Trip Expense Settler

## Project Overview
Shared Trip Expense Settler is a Python-based application designed to manage shared expenses among people during trips.

It helps participants record expenses, split costs equally, calculate individual balances, and determine who needs to pay whom to settle all outstanding amounts.

## Features
- **Participant Registration:** Add people participating in a trip.
- **Expense Management:** Record expenses with descriptions, amounts, and payers.
- **Equal Expense Splitting:** Automatically divide expenses among selected beneficiaries.
- **Accurate Calculations:** Uses integer paise calculations to avoid floating-point errors.
- **Balance Calculation:** Calculates how much each participant owes or should receive.
- **Automatic Settlement:** Uses a greedy settlement algorithm to minimize payment transactions.
- **Edit and Delete:** Modify or remove expenses with automatic recalculation.
- **Data Persistence:** Saves application data in a JSON file.
- **Input Validation:** Prevents invalid amounts, invalid payers, and duplicate beneficiaries.

## Technologies Used
- Python
- HTTPServer
- HTML Forms and Tables
- JSON for data storage

## Project Structure
```text
Shared-Trip-Expense-Settler/
│
├── app.py
├── common.py
│
└── Store/
    └── data.json
```

## Installation and Execution

### Prerequisites
- Python 3 installed on your system.
- A web browser.

### Steps

1. Download or clone the project.
2. Open the project folder in VS Code or another editor.
3. Open the terminal.
4. Run the following command:

```bash
python app.py
```

5. Open the local URL displayed by the application in your browser.

## How It Works

1. Register the trip participants.
2. Add an expense description.
3. Select the person who paid.
4. Enter the expense amount.
5. Select the beneficiaries.
6. The application calculates each person's share.
7. View individual balances.
8. Use the settlement feature to determine the payments required to settle expenses.

## Testing

The following six test cases were executed successfully:

| Test Case | Description | Result |
|---|---|---|
| TC-01 | Basic expense calculation | PASS |
| TC-02 | ₹1 remainder distribution among 3 members | PASS |
| TC-03 | Invalid payer validation | PASS |
| TC-04 | Duplicate beneficiary validation | PASS |
| TC-05 | Invalid amount validation (zero, negative, more than 2 decimal places) | PASS |
| TC-06 | Data persistence after application restart | PASS |

## Conclusion
The Shared Trip Expense Settler simplifies expense management among trip participants. It provides accurate calculations, automatic settlement, input validation, and persistent storage, reducing the effort required to manually calculate shared expenses.
