#This will be my second independent project. The goal is to create an expense tracker for general use runnable through CLI.

#import required modules here.
import os
import csv
from datetime import datetime

#check if the file exists (create if it doesnt) and access it
csv_file = "data/expenses.csv"


if os.path.exists(csv_file) == False:
    with open(csv_file, "w", newline="") as file:
        my_writer = csv.writer(file)
        header = ["date", "category", "amount", "description"]

        my_writer.writerow(header)

def add_expense():  #function that allows the user to add an expense
    while True: #loop to prompt user for the expense date until valid input is received
        try:
            date = input("Enter the date of this expense (MM/DD/YYYY format): ")    
            date_format = "%m/%d/%Y"
            correct_date = datetime.strptime(date, date_format)
            break
        except ValueError as e:
            print(f"Your date format is incorrect. Try again.")
            continue


    category = input("Enter the category of this expense: ")    #prompt user for the expense category

    while True: #loop to prompt the user for expense amount until valid input is received
        try:
            amount = input("Enter the amount spent on this expense (including cents): ")
            float_amount = float(amount)
            break
        except:
            print("Your input was invalid, try again.")
            continue

    description = input("Enter a general description of this expense: ")    #prompt user for the expense description

    new_row = [date, category, float_amount, description]   #save user inputs to a list that will be written to the file in a new row

    with open(csv_file, "a", newline="") as file:
        my_writer = csv.writer(file)
        my_writer.writerow(new_row)

    print("Expense successfully recorded!\n")

def view_expenses(): #function that allows the user to view added expenses
    with open(csv_file, "r") as file:
        my_reader = csv.reader(file)
        next(my_reader)     #this line will skip the header when reading the file

        rows = list(my_reader)
        if not rows:
            return "No expenses recorded yet"

        for row in rows:
            print(f"Date: {row[0]} | Category: {row[1]} | Amount: ${float(row[2]):.2f} | Description: {row[3]}")


#Above this line - functions utilized by the program
#Below this line - the program loop            

while True:     #This is the loop that will allow the program to run continuosly until the user chooses to exit
    print("\nWelcome to the Expense Tracker! Please select an option to proceed.\n")
    
    response = input("1. Add a new expense\n2. View saved expenses\n3. Close the Expense Tracker\n")

    if response == "1":
        add_expense()
    elif response == "2":
        view_expenses()
    elif response == "3":
        print("Thank you for using the Expense Tracker! Until next time!")
        break
    else:
        print("Your input was invalid. Try again.")
        continue
