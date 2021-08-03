import requests


class UserAccount:
    def __init__(self):
        self.balance=0
        print("Welcome to the Account!")

    def deposit(self, amount):
        self.balance += amount
        print("\n Amount Deposited:", amount)

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print("\n You Withdrew:", amount)
        else:
            print("\n Insufficient balance  ")

    def display(self):
        print("\n Net Available Balance=", self.balance)
