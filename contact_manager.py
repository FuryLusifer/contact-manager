import os
import sys
import json

class Colors:
    """ANSI escape sequences for coloring terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'   # Success
    WARNING = '\033[93m'   # Warnings, prompts
    FAIL = '\033[91m'      # Errors
    ENDC = '\033[0m'       # Reset to default
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ContactManager:
    """
    A simple CLI-based Contact Manager.
    Stores contact details (name, phone number, email) in a JSON file.
    Supports adding, listing, searching, updating, and deleting contacts.
    """

    def __init__(self):
        self.contact_db = "contact_db.json"
        self.contacts_list = []

    # ---------------- MENU ----------------
    def show_menu(self):
        print(f"\n{Colors.HEADER}    ------- Contact Manager -------{Colors.ENDC}")
        print("1. Add new contact")
        print("2. List all contacts")
        print("3. Search contact")
        print("4. Update contact")
        print("5. Delete contact")
        print("6. Exit")

    def take_user_choice(self):
        choice = input(f"{Colors.WARNING}Enter your choice: {Colors.ENDC}").strip()
        return choice

    # ---------------- FILE HANDLING ----------------
    def validate_contact_db(self):
        if os.path.exists(self.contact_db):
            with open(self.contact_db, "r") as file:
                try:
                    self.contacts_list = json.load(file)
                except json.JSONDecodeError:
                    self.contacts_list = []
        else:
            with open(self.contact_db, "w") as file:
                json.dump([], file)
            self.contacts_list = []
        return True
    
    def save_contacts_to_file(self):
        with open(self.contact_db, "w") as file:
            json.dump(self.contacts_list, file, indent=4)

    def print_contact_list(self, contacts=None):
        if contacts is None:
            contacts = self.contacts_list

        print(f"{Colors.BOLD}{'S.N':<6} {'Name':<20} {'Phone Numbers':<15} {'Email':<30}{Colors.ENDC}")
        print('-' * 60)

        for index, contact in enumerate(contacts, start=1):
            print(
                f"{index:<6} {contact['name']:<20} {contact['number']:<15} "
                f"{contact['email']:<30}"
            )

    # ---------------- CORE FUNCTIONS ----------------
    def add_new_contact(self):
        self.validate_contact_db()

        name = input(f"{Colors.WARNING}Enter Fullname: {Colors.ENDC}").title().strip()
        number = input(f"{Colors.WARNING}Enter Phone Number: {Colors.ENDC}").strip()
        email = input(f"{Colors.WARNING}Enter email address: {Colors.ENDC}").strip().lower()

        if not name or not number or not email:
            print(f"{Colors.FAIL}All fields are required.{Colors.ENDC}")
            return
        if "@" not in email or "." not in email:
            print(f"{Colors.FAIL}Invalid email format.{Colors.ENDC}")
            return

        for contact in self.contacts_list:
            if contact['number'].replace(" ", "").replace("-", "") == number.replace(" ", "").replace("-", ""):
                print(f"{Colors.FAIL}A contact with this number already exists.{Colors.ENDC}")
                return
            if contact['email'] == email:
                print(f"{Colors.FAIL}A contact with this email already exists.{Colors.ENDC}")
                return

        new_contact = {
            "name": name,
            "number": number,
            "email": email
        }
        self.contacts_list.append(new_contact)
        self.save_contacts_to_file()

        print(f"{Colors.OKGREEN}Contact '{name}' saved successfully.{Colors.ENDC}")

    def list_all_contacts(self):
        self.validate_contact_db()
        if not self.contacts_list:
            print(f"\n{Colors.WARNING}No contacts found.{Colors.ENDC}")
            return
        
        print(f"\n{Colors.OKCYAN}---------------------- Contact List ------------------------{Colors.ENDC}")
        self.print_contact_list()

    def search_contact(self):
        term = input(f"{Colors.WARNING}Enter search term (e.g. name:john): {Colors.ENDC}").strip()
        self.validate_contact_db()

        if not term:
            print(f"{Colors.FAIL}Search term cannot be empty.{Colors.ENDC}")
            return

        results = []

        if ":" in term:
            field, value = term.split(":", 1)
            field = field.strip().lower()
            value = value.strip().lower()

            if field not in ["name", "number", "email"]:
                print(f"{Colors.FAIL}Invalid field. Use name, number, or email.{Colors.ENDC}")
                return

            for contact in self.contacts_list:
                target_value = contact[field].lower()
                if field == "number":
                    target_value = target_value.replace(" ", "").replace("-", "")
                    value = value.replace(" ", "").replace("-", "")
                if value in target_value:
                    results.append(contact)
        else:
            term_lower = term.lower()
            normalized_term = term_lower.replace(" ", "").replace("-", "")

            for contact in self.contacts_list:
                if (term_lower in contact['name'].lower()
                    or normalized_term in contact['number'].replace(" ", "").replace("-", "")
                    or term_lower in contact['email'].lower()):
                    results.append(contact)

        if not results:
            print(f"{Colors.FAIL}No match found.{Colors.ENDC}")
            return

        print(f"\n{Colors.OKCYAN}--------------------- Search Results -----------------------{Colors.ENDC}")
        self.print_contact_list(results)

    def update_contact(self):
        self.validate_contact_db()
        name = input(f"{Colors.WARNING}Enter the name of the contact to update: {Colors.ENDC}").strip().lower()

        for contact in self.contacts_list:
            if contact['name'].lower() == name:
                print(f"{Colors.WARNING}Leave field empty to keep current value.{Colors.ENDC}")
                new_name = input(f"New name ({contact['name']}): ").strip() or contact['name']
                new_number = input(f"New number ({contact['number']}): ").strip() or contact['number']
                new_email = input(f"New email ({contact['email']}): ").strip() or contact['email']

                if new_email != contact['email']:
                    if "@" not in new_email or "." not in new_email:
                        print(f"{Colors.FAIL}Invalid email format. Update aborted.{Colors.ENDC}")
                        return

                contact['name'] = new_name
                contact['number'] = new_number
                contact['email'] = new_email

                self.save_contacts_to_file()
                print(f"{Colors.OKGREEN}Contact updated successfully.{Colors.ENDC}")
                return

        print(f"{Colors.FAIL}Contact not found.{Colors.ENDC}")

    def delete_contact(self):
        self.validate_contact_db()
        name = input(f"{Colors.WARNING}Enter the name of the contact to delete: {Colors.ENDC}").strip().lower()

        for contact in self.contacts_list:
            if contact['name'].lower() == name:
                confirm = input(f"{Colors.WARNING}Are you sure you want to delete '{contact['name']}'? (y/n): {Colors.ENDC}").strip().lower()
                if confirm == "y":
                    self.contacts_list.remove(contact)
                    self.save_contacts_to_file()
                    print(f"{Colors.OKGREEN}Contact deleted successfully.{Colors.ENDC}")
                else:
                    print(f"{Colors.WARNING}Delete cancelled.{Colors.ENDC}")
                return

        print(f"{Colors.FAIL}Contact not found.{Colors.ENDC}")

    def exit_app(self):
        print(f"{Colors.OKBLUE}See you next time.{Colors.ENDC}")
        sys.exit()

    # ---------------- RUN APP ----------------
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
                print(f"{Colors.FAIL}Wrong Input! Enter again...{Colors.ENDC}")

# --------- Start the App ----------
if __name__ == "__main__":
    contact = ContactManager()
    contact.run_contact_manager()