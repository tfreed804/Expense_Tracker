#This will be my second independent project. The goal is to create an expense tracker for general use runnable through CLI.

#import required modules here.
import os
import csv
from datetime import datetime

#define the file path and file header
csv_file = "data/expenses.csv"
header = ["date", "category", "amount", "description"]

#Ensure the directory exists
def ensure_csv_initialized():
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    if not os.path.isfile(csv_file) or os.stat(csv_file).st_size == 0:
        with open(csv_file, "w", newline="") as file:
            my_writer = csv.writer(file)
            my_writer.writerow(header)

#Function to clear screen between function calls
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def add_expense():  #function that allows the user to add an expense
    clear_screen()
    while True: #loop to prompt user for the expense date until valid input is received
        try:
            date = input("Enter the date of this expense (MM/DD/YYYY format): ")    
            date_format = "%m/%d/%Y"
            correct_date = datetime.strptime(date, date_format)
            formatted_date = correct_date.strftime("%m/%d/%Y")
            break
        except ValueError:
            print("Your date format is incorrect. Try again.")
            continue


    category = input("Enter the category of this expense: ").strip().title()    #prompt user for the expense category

    while True: #loop to prompt the user for expense amount until valid input is received
        try:
            amount = input("Enter the amount spent on this expense (including cents): ")
            float_amount = round(float(amount), 2)
            break
        except ValueError:
            print("Your input was invalid, try again.")
            input("Press Enter to continue...")
            clear_screen()
            continue

    description = input("Enter a general description of this expense: ").strip()    #prompt user for the expense description

    new_row = [formatted_date, category, float_amount, description]   #save user inputs to a list that will be written to the file in a new row

    with open(csv_file, "a", newline="") as file:
        my_writer = csv.writer(file)
        my_writer.writerow(new_row)

    print("Expense successfully recorded!\n")

    input("\nPress Enter to return to the main menu...")

def edit_expense():     #function to handle editing previous expenses
    clear_screen()
    with open(csv_file, "r") as file:
        my_reader = csv.reader(file)
        next(my_reader)
        rows = list(my_reader)

        if not rows:
            print("No expenses to edit.")
            input("\nPress Enter to continue...")
            return

        for index, row in enumerate(rows):
            print(f"{index + 1}. Date: {row[0]} | Category: {row[1]} | Amount: ${float(row[2]):.2f} | Description: {row[3]}")

        try:
            selection = int(input("Enter the number of the expense to edit: \n"))
            if 1 <= selection <= len(rows):
                selected_row = rows[selection -1]
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a valid expense number.")
            return
        
    print("\nPress Enter without typing anything to keep the current value.\n")     #prompt for new values with current as default

    while True:     #loop to validate new user input
        #Date
        new_date = input(f"Enter new date (MM/DD/YYYY) [{selected_row[0]}]: ")

        if new_date == "":
            new_date = selected_row[0]
            break

        try:
            datetime.strptime(new_date, "%m/%d/%Y")
            break
        except ValueError:
            print("Invalid date format. Please try again.")

    #Category
    new_category = input(f"Enter new category [{selected_row[1]}]: ")

    if new_category == "":
        new_category = selected_row[1]

    #Amount
    while True:
        new_amount = input(f"Enter new amount [{selected_row[2]}]: ")

        if new_amount == "":
            floated_new_amount = float(selected_row[2])
            break

        try:
            floated_new_amount = float(new_amount)
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            input("Press Enter to continue...")
            continue

    #Description
    new_description = input(f"Enter new description [{selected_row[3]}]: ")
    
    if new_description == "":
        new_description = selected_row[3]

    #Update the selected row with new values
    rows[selection -1] = [new_date, new_category, floated_new_amount, new_description]

    #Update the file
    with open(csv_file, "w", newline="") as file:
        my_writer = csv.writer(file)
        my_writer.writerow(header)
        my_writer.writerows(rows)

    print("\nExpense updated successfully!\n")

    input("\nPress Enter to return to the main menu...")

def delete_expense():   #function that allows the removal of an expense
    clear_screen()
    with open(csv_file, "r") as file:
        my_reader = csv.reader(file)
        next(my_reader)     #skips the header line
        rows = list(my_reader)      #saves expense rows as a list

        if not rows:    #prints message if now expenses have been added yet
            print("No expenses to delete.")
            input("\nPress Enter to continue...")
            return

        for index, row in enumerate(rows):
            print(f"{index + 1}. Date: {row[0]} | Category: {row[1]} | Amount: ${float(row[2]):.2f} | Description: {row[3]}")
        
        try:
            selection = int(input("Enter the number of the expense to delete: "))
            if 1 <= selection <= len(rows):
                deleted = rows.pop(selection - 1)
                print("Deleted expense: ", deleted)
            else:
                print("Invalid selection.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid expense number.")
            input("Press Enter to continue...")
            clear_screen()
            return
    
    with open(csv_file, "w", newline="") as file:
        my_writer = csv.writer(file)
        my_writer.writerow(header)
        my_writer.writerows(rows)

    print("Expense deleted successfully!\n")

    input("\nPress Enter to return to the main menu...")

def view_expenses(): #function that allows the user to view added expenses
    clear_screen()
    with open(csv_file, "r") as file:
        my_reader = csv.reader(file)
        next(my_reader)     #this line will skip the header when reading the file
        rows = list(my_reader)

        if not rows:
            print("No expenses recorded yet")
            input("\nPress Enter to continue...")
            return
        
        # Print table headers
        print(f"{'Date':<12} {'Category':<15} {'Amount':<10} Description")
        print("-" * 60)

        #print rows
        for row in rows:
            #convert date for a nicer display
            date_obj = datetime.strptime(row[0], "%m/%d/%Y")
            pretty_date = date_obj.strftime("%b %d, %Y")

            #Display row
            print(f"{pretty_date:<12} {row[1]:<15} ${float(row[2]):<10.2f} {row[3]}")

        #Display sum of all expenses
        total = sum(float(row[2]) for row in rows)
        print("-" * 60)
        print(f"{'Total':<27} ${total:.2f}")

        input("\nPress Enter to return to the main menu...")


#Above this line - functions utilized by the program
#Below this line - the program loop            

while True:     #This is the loop that will allow the program to run continuosly until the user chooses to exit
    ensure_csv_initialized()
    clear_screen()
    
    print("\nWelcome to the Expense Tracker! Please select an option to proceed.\n")
    
    response = input("1. Add a new expense\n2. View saved expenses\n3. Edit an expense\n4. Delete an expense\n5. Close the Expense Tracker\n")

    if response == "1":
        add_expense()
    elif response == "2":
        view_expenses()
    elif response =="3":
        edit_expense()
    elif response == "4":
        delete_expense()
    elif response == "5":
        print("Thank you for using the Expense Tracker! Until next time!")
        break
    else:
        print("Your input was invalid. Try again.")
        continue
