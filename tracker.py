#This will be my second independent project. The goal is to create an expense tracker for general use runnable through CLI.

#import required modules here.
import os
import csv

#check if the file exists (create if it doesnt) and access it
csv_file = "data/expenses.csv"


if os.path.exists(csv_file) == False:
    with open(csv_file, "w") as file:
        