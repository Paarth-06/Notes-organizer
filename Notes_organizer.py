import os
from datetime import *
import json

class Categories:
    def __init__(self):
        self.ist = timezone(timedelta(hours = 5, minutes = 30)) #creating indian standard timezone
        self.date = datetime.now(self.ist).strftime("%d - %b - %Y : %A") #shows only date - month name  - year : Day name
        self.time = datetime.now(self.ist).strftime("%I : %M : %S %p") # shows only time in 24 hour format , %p specifies am or pm
        self.category_list = [] # list to store all the categories
        if not os.path.exists("logs.txt"): # if the log file does not exist, it'll create one
                f= open("logs.txt","w")
                f.close()
        if not os.path.exists("Category.json"): #if the category file does not exist , it'll create one. 
            f = open("Category.json","w")
            f.close()
        else:
            try:
                with open("Category.json", "r") as f: #If category file exist, it'll read it and assign the values to the self.category_list, so the data not only is in the memory, it is stored locally.
                    self.category_list = json.load(f) #so if the program gets restarted, it'll retain all the past stored values
            except json.JSONDecodeError:
                self.category_list = []

    def creating_notes(self): #Handles Creating notes categories
        print("Note : To exit, just type 'q' in small case \n")
        self.cat_name = input("Enter a category name : ")
        if self.cat_name == 'q':
            return
        else:
            while True:
                if not os.path.exists(self.cat_name):
                    f = open(self.cat_name,"w")
                    f.close()
                    print(f"{self.cat_name} was created successfully !!!")
                    f = open("logs.txt","a")
                    data = f"{self.cat_name} was created on {self.date} at {self.time}" # Writes the data in the log with proper dates and time at the time of execution
                    f.write(data + "\n") #Stores data in a newline after every iteration
                    f.close()
                    self.category_list.append(self.cat_name) #updating self.category_list for reflecting the current changes
                    with open("Category.json","w") as f: #updating the changes in the category .json
                        json.dump(self.category_list, f)
                elif os.path.exists(self.cat_name):
                    print(f"Sorry {self.cat_name} already exist , please try other name to continue... ")
                self.cat_name = input("Enter a category name : ")
                if self.cat_name == 'q':
                    break

    def deleting_category(self): #Handles deleting the notes categories
        while True:
            print(f"The categories are: {', '.join(f'{i} : {cat}' for i, cat in enumerate(self.category_list, start = 1))}")
            user_response = input("Enter The category name : ")
            if os.path.exists(user_response):
                user_confirmation = input("DANGER!!! YOU ARE ABOUT TO DELETE THE FILE, THE FILE OR IT'S CONTENT CANNOT BE RECOVERED, DO YOU STILL WISH TO CONTINUE yes/no : ").lower()
                if user_confirmation == 'yes':
                    self.category_list.remove(user_response)
                    os.remove(user_response)
                    f = open("logs.txt","a")
                    data = f"{user_response} was deleted on {self.date} at {self.time}"
                    f.write(data + "\n")
                    f.close()
                    with open("Category.json","w") as f:
                        json.dump(self.category_list, f)
                    print(f"{user_response} was deleted successfully...")
                    user_exit = input("Do you wish to continue yes/no : ").lower()
                    if user_exit == 'no':
                        break
                elif user_confirmation =='no':
                    break
                else:
                    print("Not a valid action, try again later...")
            else:
                print("Sorry the file does not exist....")
            

    def rename_cat(self): #Handles renaming the note categories
        while True:
            print(f"The categories are: {', '.join(f'{i} : {cat}' for i, cat in enumerate(self.category_list, start = 1))}")
            user_response = input("Enter the category name : ")
            if os.path.exists(user_response):
                new_name = input("Enter a new name : ")
                f = open(user_response, "r")
                data = f.read()
                f.close()
                os.remove(user_response) #removes the old name
                self.category_list.remove(user_response)#removes the old name
                f = open(new_name,"w")
                f.write(data)
                f.close()
                f = open("logs.txt","a")
                data = f"{user_response} was renamed to {new_name} on {self.date} at {self.time}"
                f.write(data + "\n")
                f.close()
                self.category_list.append(new_name)
                with open("Category.json","w") as f:
                        json.dump(self.category_list, f)
                print(f"Category was renamed from {user_response} to {new_name}")
                user_exit = input("Do you wish to continue yes/no : ").lower()
                if user_exit == 'no':
                    break

    def view_log(self):
        f = open("logs.txt","r")
        readlines = f.readlines()
        f.close()
        for line in readlines:
            print(line)
    def view_cat(self):
        for i, cat in enumerate(self.category_list,start = 1):
            print(f"Categories are : {i} : {cat}")

class Notes(Categories): #This is a child class, and the parent is Categories

    def add_notes(self): #Lets the user add notes into the desired file
        print(f"The categories are: {', '.join(f'{i} : {cat}' for i, cat in enumerate(self.category_list, start = 1))}")
        user_note_response = input("Which category to enter in : ")
        if not os.path.exists(user_note_response):
            print(f"{user_note_response} does not exists..")
        else:
            with open(user_note_response,"a") as f:
                while True:
                    print("Start writing and press enter for new line and write 'EXIT' to quit : \n")
                    
                    data = input()
                    f.write(data + "\n")
                    if data == data + "": #if the user wants to write in the next line in a continuous manner, it'll enter in a loop and won't break till you type EXIT.
                        while True:
                            data2 = input()
                            f.write(data2+"\n")
                            if data2 == "EXIT":
                                f.close()
                                with open(user_note_response,"r") as f:
                                    read_data = f.read()
                                    new_data = read_data.replace("EXIT", "") #removing EXIT, as it gets typed when you try to exit.
                                    f.close()
                                f = open(user_note_response,"w")
                                f.write(new_data)
                                f.close()   
                                print("Your data was written succsessfully...")
                                f = open("logs.txt","a")
                                data = f"Data was written in {user_note_response} on {self.date} at {self.time}"
                                f.write(data + "\n")
                                f.close()
                                return
                            
    def removing_data(self): #Completly removes the data from a file 
        while True:
            print(f"The categories are: {', '.join(f'{i} : {cat}' for i, cat in enumerate(self.category_list, start = 1))}")
            user_del_response = input("Select the file to delete the content of : ")
            if os.path.exists(user_del_response):
                user_response= input(f"DANGERR!! YOU ARE ABOUT TO DELETE THE CONTENT OF {user_del_response} WHICH IS NOT RECOVERABLE DO YOU WISH TO PROCEEED YES/NO :  ").lower()
                if user_response == "yes":
                    f = open(user_del_response,"w")
                    f.close()
                    f = open("logs.txt","a")
                    data = f"Data of {user_del_response} was deleted on {self.date} at {self.time}"
                    f.write(data + "\n")
                    f.close()
                    print("YOUR DATA WAS WIPED SUCCESSFLLY!!")
                    user_exit_response = input("Do you wish to proceed yes/no : ").lower()
                    if user_exit_response == 'no':
                        break
                elif user_response == 'no':
                    return
                else:
                    print("Not a valid action...")
            else:
                print(f"Sorry {user_del_response} does not exist...")

    def edit_notes(self): #Let's the user rewrite new data into a pre-existing file with pre-existing data
        while True:
            print(f"The categories are: {', '.join(f'{i} : {cat}' for i, cat in enumerate(self.category_list, start = 1))}")
            user_response = input("Enter the category : ")
            if os.path.exists(user_response):
                user_confirmation = input("YOU ARE ABOUT TO REWRITE THE ENTIRE FILE WITH NEW DATA, DO  YOU WISH TO PROCEED YES/NO : ").lower()
                if user_confirmation == 'yes':
                    f = open(user_response,"w")
                    print("Start writing, enter 'EXIT' to quit : \n")
                    data = input()
                    f.write(data + "\n")
                    if data == data + "":
                        while True:
                            data2 = input()
                            f.write(data2+"\n")
                            if data2 == "EXIT":
                                f.close()
                                with open(user_response,"r") as f:
                                    read_data = f.read()
                                    new_data = read_data.replace("EXIT", "")
                                    f.close()
                                    f = open(user_response,"w")
                                    f.write(new_data)
                                    f.close()
                                    f = open("logs.txt","a")
                                    data = f"Data of {user_response} was re-written on {self.date} at {self.time}"
                                    f.write(data + "\n")
                                    f.close()
                                    print("Your data was re-written succsessfully...")
                                    return

run_main_program = Notes()
action = {
    "createcat": run_main_program.creating_notes,
    "deletecat": run_main_program.deleting_category,
    "editcat": run_main_program.rename_cat,
    "addnotes": run_main_program.add_notes,
    "delnotes": run_main_program.removing_data,
    "rewrite": run_main_program.edit_notes,
    "viewlog": run_main_program.view_log,
    "viewcat": run_main_program.view_cat,
}
while True:
    print(f"Welcome.. \nActions :\n➊Create Note categories : 'createcat' \n➋ Delete Note categories : 'deletecat' \n➌ Edit categories name : 'editcat' \n➍ Add notes to subject : 'addnotes' \n➎ Delete all notes inside a subject : 'delnotes' \n➏ Re-write notes : 'rewrite' \n➐ View Logs : 'viewlog' \n➑ View categories : 'viewcat' \n➒ Exit : 'exit' ")

    user_ans = input("\nEnter your response : ").lower()
    if user_ans in action:
        action[user_ans]()
    elif user_ans == "exit":
        break
    else:
        print("Not a valid option...")


#Future upgrade might be :- creating a separate folder and then store the created files there for better cleanliness
