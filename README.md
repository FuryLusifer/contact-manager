
# Contact Manager CLI Application

A simple command-line interface (CLI) Contact Manager written in Python.  
It allows you to add, list, search, update, and delete contacts stored in a JSON file.

---

## Features

- Add new contacts with name, phone number, and email
- List all saved contacts in a neat table format
- Search contacts by name, phone number, or email (supports partial and case-insensitive search)
- Update existing contact information
- Delete contacts with confirmation prompt
- Data persistence using a JSON file (`contact_db.json`)
- Color-coded terminal output for better user experience

---

## Requirements

- Python 3.x (tested on Python 3.13.5)
- Works on Windows, macOS, and Linux terminals that support ANSI escape codes for colored output

---

## Usage

1. Clone or download this repository.

2. Run the Python script:

   ```bash
   python contact_manager.py
   ```

3. Use the on-screen menu to interact with the application.

---

## How to Search

- General search: enter any text to search across name, number, and email.

- Field-specific search: use the syntax `field:value` to search within a specific field.  
  Supported fields: `name`, `number`, `email`

Example:

```
name:john
email:gmail.com
number:123
```

---

## Code Structure

- `ContactManager` class handles all logic: file operations, user input, and contact management.
- Contacts are stored as dictionaries with `name`, `number`, and `email` keys.
- Data is saved and loaded from `contact_db.json`.

---

## Notes

- Input validations are done for required fields and email format.
- Phone numbers and emails are checked for duplicates before adding new contacts.
- To exit the program, choose option 6 from the menu.

---

## License

This project is open source and free to use.

---

## Author

[Your Name]

---

Feel free to contribute, suggest features, or report issues!
