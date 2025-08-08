import os
import json
class ContactManager:

    def __init__(self):
        contact_dict = []

    def show_menu(self):
        print("    ------- Contact Manager -------")
        print("1. Add new contact")
        print("2. List all contacts")
        print("3. Search contact")
        print("4. Update contact")
        print("5. Delete contact")
        print("6. Exit")

    def take_user_choice(self):
        choice = input("Enter your choice: ").strip()
        return choice
    
    def add_new_contact(self):
        print("Pressed 1")
        

    def list_all_contacts(self):
        print("Pressed 2")

    def search_contact(self):
        print("Pressed 3")

    def update_contact(self):
        print("Pressed 4")

    def delete_contact(self):
        print("Pressed 5")

    def exit_app(self):
        print("See you next time.")
        exit()
        
    def run_contact_manager(self):
        while True:
            self.show_menu()
            choice = self.take_user_choice()
            if choice == "1":
                self.add_new_contact()
            
            elif choice == "2":
                self.list_all_contacts()
            
            elif choice == "3":
                self.search_contact()

            elif choice == "4":
                self.update_contact()
            
            elif choice == "5":
                self.delete_contact()
            
            elif choice == "6":
                self.exit_app()
            
            else:
                print("Wrong Input! Enter again...")

contact = ContactManager()
contact.run_contact_manager()