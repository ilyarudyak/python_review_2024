import re

email = input("What's your email address? ")

def validate(email):
    # regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    regex = r"^.+@.+\.edu$"
    email_regex = re.compile(regex)
    match = email_regex.match(email)
    if match:
        return True
    else:
        return False
    
if __name__ == "__main__":
    if validate(email):
        print("Valid email address")
    else:
        print("Invalid email address")
