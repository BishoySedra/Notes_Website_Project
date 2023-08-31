import re

# Regular expression pattern for validating email addresses
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

# Function to check if an email address is valid
def is_valid_email(email):
    return re.match(email_pattern, email)