import json
from datetime import datetime
class Account:
    def __init__(self, account_no, name, account_type, pin, balance=0,
                 transactions=None):
        self.account_no = account_no
        self.name = name
        self.account_type = account_type
        self.pin = pin
        self.balance = balance

        if transactions is None:
            self.transactions = []
        else:
            self.transactions = transactions

    # Deposit money
    def deposit(self, amount):

        if amount <= 0:
            print("Invalid amount")
            return False

        self.balance += amount

        self.transactions.append({
            "type": "Deposit",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance_after_transaction": self.balance
        })

        print("Amount deposited successfully.")
        return True

    # Withdraw money
    def withdraw(self, amount):

        if amount <= 0:
            print("Invalid amount")
            return False

        if amount > self.balance:
            print("Insufficient balance.")
            return False

        self.balance -= amount

        self.transactions.append({
            "type": "Withdraw",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance_after_transaction": self.balance
        })

        print("Amount withdrawn successfully.")
        return True

    # Check balance
    def check_balance(self):

        print("\nCurrent Balance:", self.balance)

    # Show account details
    def show_details(self):

        print("\n---------- ACCOUNT DETAILS ----------")
        print("Account Number :", self.account_no)
        print("Name           :", self.name)
        print("Account Type   :", self.account_type)
        print("Balance        :", self.balance)
        print("-------------------------------------")

    # Show transaction history
    def show_transactions(self):

        print("\n---------- TRANSACTION HISTORY ----------")

        if len(self.transactions) == 0:
            print("No transactions found.")
            return

        for transaction in self.transactions:

            print("Type       :", transaction["type"])
            print("Amount     :", transaction["amount"])
            print("Date       :", transaction["date"])
            print(
                "Balance    :",
                transaction["balance_after_transaction"]
            )

            print("----------------------------------------")

    # Convert object into dictionary
    def to_dict(self):

        return {
            "name": self.name,
            "account_type": self.account_type,
            "pin": self.pin,
            "balance": self.balance,
            "transactions": self.transactions
        }


class Bank:

    FILE_NAME = "bank_data.json"

    def __init__(self):

        self.accounts = {}

        self.load_data()

    # Load data from JSON
    def load_data(self):

        try:

            with open(self.FILE_NAME, "r") as file:

                data = json.load(file)

                for account_no, account_data in data.items():

                    account = Account(
                        account_no,
                        account_data["name"],
                        account_data["account_type"],
                        account_data["pin"],
                        account_data["balance"],
                        account_data["transactions"]
                    )

                    self.accounts[account_no] = account

        except FileNotFoundError:

            self.accounts = {}

    # Save data into JSON
    def save_data(self):

        data = {}

        for account_no, account in self.accounts.items():

            data[account_no] = account.to_dict()

        with open(self.FILE_NAME, "w") as file:

            json.dump(data, file, indent=4)

    # Create account
    def create_account(self):

        print("\n---------- CREATE ACCOUNT ----------")

        account_no = input("Enter Account Number: ")

        if account_no in self.accounts:

            print("Account already exists.")
            return

        name = input("Enter Name: ")

        account_type = input(
            "Enter Account Type (Savings/Current): "
        )

        pin = input("Create 4-digit PIN: ")

        if len(pin) != 4 or not pin.isdigit():

            print("PIN must contain exactly 4 digits.")
            return

        try:

            initial_deposit = float(
                input("Enter Initial Deposit: ")
            )

        except ValueError:

            print("Please enter a valid amount.")
            return

        if initial_deposit < 0:

            print("Amount cannot be negative.")
            return

        account = Account(
            account_no,
            name,
            account_type,
            pin,
            initial_deposit
        )

        if initial_deposit > 0:

            account.transactions.append({
                "type": "Initial Deposit",
                "amount": initial_deposit,
                "date": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "balance_after_transaction": initial_deposit
            })

        self.accounts[account_no] = account

        self.save_data()

        print("\nAccount created successfully.")

    # Find account
    def get_account(self):

        account_no = input("Enter Account Number: ")

        if account_no not in self.accounts:

            print("Account not found.")
            return None

        account = self.accounts[account_no]

        pin = input("Enter PIN: ")

        if pin != account.pin:

            print("Incorrect PIN.")
            return None

        return account

    # Deposit
    def deposit_money(self):

        print("\n---------- DEPOSIT ----------")

        account = self.get_account()

        if account is None:
            return

        try:

            amount = float(
                input("Enter amount to deposit: ")
            )

        except ValueError:

            print("Invalid amount.")
            return

        if account.deposit(amount):

            self.save_data()

    # Withdraw
    def withdraw_money(self):

        print("\n---------- WITHDRAW ----------")

        account = self.get_account()

        if account is None:
            return

        try:

            amount = float(
                input("Enter amount to withdraw: ")
            )

        except ValueError:

            print("Invalid amount.")
            return

        if account.withdraw(amount):

            self.save_data()

    # Check balance
    def check_balance(self):

        print("\n---------- CHECK BALANCE ----------")

        account = self.get_account()

        if account is None:
            return

        account.check_balance()

    # Account details
    def account_details(self):

        print("\n---------- ACCOUNT DETAILS ----------")

        account = self.get_account()

        if account is None:
            return

        account.show_details()

    # Transaction history
    def transaction_history(self):

        print("\n---------- TRANSACTIONS ----------")

        account = self.get_account()

        if account is None:
            return

        account.show_transactions()

    # Change PIN
    def change_pin(self):

        print("\n---------- CHANGE PIN ----------")

        account = self.get_account()

        if account is None:
            return

        new_pin = input("Enter New 4-digit PIN: ")

        if len(new_pin) != 4 or not new_pin.isdigit():

            print("PIN must contain exactly 4 digits.")
            return

        account.pin = new_pin

        self.save_data()

        print("PIN changed successfully.")

    # Close account
    def close_account(self):

        print("\n---------- CLOSE ACCOUNT ----------")

        account_no = input("Enter Account Number: ")

        if account_no not in self.accounts:

            print("Account not found.")
            return

        account = self.accounts[account_no]

        pin = input("Enter PIN: ")

        if pin != account.pin:

            print("Incorrect PIN.")
            return

        if account.balance > 0:

            print(
                "Please withdraw your remaining balance "
                "before closing the account."
            )

            return

        del self.accounts[account_no]

        self.save_data()

        print("Account closed successfully.")

    # Main menu
    def menu(self):

        while True:

            print("\n")
            print("====================================")
            print("       BANK MANAGEMENT SYSTEM")
            print("====================================")

            print("1. Create Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Check Balance")
            print("5. Account Details")
            print("6. Transaction History")
            print("7. Change PIN")
            print("8. Close Account")
            print("9. Exit")

            print("====================================")

            choice = input("Enter your choice: ")

            if choice == "1":

                self.create_account()

            elif choice == "2":

                self.deposit_money()

            elif choice == "3":

                self.withdraw_money()

            elif choice == "4":

                self.check_balance()

            elif choice == "5":

                self.account_details()

            elif choice == "6":

                self.transaction_history()

            elif choice == "7":

                self.change_pin()

            elif choice == "8":

                self.close_account()

            elif choice == "9":

                print("Thank you for using Bank Management System.")
                break

            else:

                print("Invalid choice. Please try again.")


# Create Bank object
bank = Bank()

# Start application
bank.menu()