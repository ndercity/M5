'''
THANKS u/dvlop from reddit for the idea.
https://www.reddit.com/r/AskProgramming/comments/1f95xj5/is_it_possible_to_verify_a_gmail_email_address/

import requests
from bs4 import BeautifulSoup

# Function to check the email on the mail7.net site

def check_email(email):
    url = "https://mail7.net/emailchecker.html#emailCheck"
    data = {'email': email, 'submit': 'Check it'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Sending a POST request
    response = requests.post(url, data=data, headers=headers)
    
    # Parsing the response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Checking if the email is valid
    if soup.find('div', class_='alert alert-success'):
        return "OK"
    elif soup.find('div', class_='alert alert-danger') or soup.find('div', class_='alert alert-warning'):
        return "BAD"
    return "UNKNOWN"

status = check_email("aarrulr7yevdkdgpq6m@gmail.com") ///CHANGE THE PARAMETER TO CHECK EMAIL
print("Status:", status)
'''

'''
Full Code

import requests
from bs4 import BeautifulSoup

# Function to check the email on the mail7.net site
def check_email(email):
    url = "https://mail7.net/emailchecker.html#emailCheck"
    data = {'email': email, 'submit': 'Check it'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Sending a POST request
    response = requests.post(url, data=data, headers=headers)
    
    # Parsing the response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Checking if the email is valid
    if soup.find('div', class_='alert alert-success'):
        return "OK"
    elif soup.find('div', class_='alert alert-danger') or soup.find('div', class_='alert alert-warning'):
        return "BAD"
    return "UNKNOWN"

# Function to read emails from a file and check them
def process_emails(input_file, good_output, bad_output):
    with open(input_file, 'r') as f:
        emails = f.readlines()

    with open(good_output, 'w') as good, open(bad_output, 'w') as bad:
        for email in emails:
            email = email.strip()  # Removing any extra whitespace
            result = check_email(email)
            if result == "OK":
                good.write(email + "\n")
            else:
                bad.write(email + "\n")

# Specifying the input file and output files for results
process_emails("emails.txt", "good.txt", "bad.txt")
'''