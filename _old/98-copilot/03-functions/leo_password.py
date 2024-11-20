import string

def is_strong_password(password):
    """
    A strong password is not the word 'password'
    and is not the word 'qwerty'.
    Return True if the password is a strong password, False if not.
    """
    if password == 'password' or password == 'qwerty':
        return False
    return True

def is_strong_password_v2(password):
    """
    A strong password has at least one uppercase character,
    at least one number, and at least one special symbol (punctuation).
    Return True if the password is a strong password, False if not. 
    """
    has_uppercase = any(char.isupper() for char in password)
    has_number = any(char.isdigit() for char in password)
    has_special = any(char in string.punctuation for char in password)
    # print(string.punctuation)
    return has_uppercase and has_number and has_special

def get_strong_password():
    """
    Keep asking the user for a password until it is a strong
    password, and return that strong password. Use the function
    is_strong_password_v2() to check if the password is strong.
    """
    while True:
        password = input('Enter a strong password: ')
        if is_strong_password_v2(password):
            # Print success message and return the password
            print('Password is strong!')
            return password
        print('That password is not strong enough. Try again.')


if __name__ == '__main__':

    # # Add some simple tests for the function is_strong_password()
    # assert is_strong_password('password') == False
    # assert is_strong_password('qwerty') == False
    # assert is_strong_password('password1') == True

    # # Add some simple tests for the function is_strong_password_v2()
    # assert is_strong_password_v2('password') == False
    # assert is_strong_password_v2('qwerty') == False
    # assert is_strong_password_v2('password1') == False
    # assert is_strong_password_v2('Password1!') == True
    # assert is_strong_password_v2('N3w Y0rk J375') == False

    get_strong_password()
