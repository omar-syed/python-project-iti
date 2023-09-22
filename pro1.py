import re
import datetime
import getpass
import json


class User:
    def __init__(self, first_name, last_name, email, password, confirm_password, mobile_phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        self.mobile_phone = mobile_phone

    def register(self):
        while not self.first_name.isalpha() or not self.first_name.isalnum():
            self.first_name = input("Please enter a valid first name: ")

        while not self.last_name.isalpha() or not self.last_name.isalnum():
            self.last_name = input("Please enter a valid last name: ")

        while not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            self.email = input("Please enter a valid email: ")

        if not re.match(r"\+20\d{9}", self.mobile_phone):
            print("Invalid Egyptian phone number format.")
            return

        while False:
            self.password = getpass.getpass("Enter your password: ")
        while False:
            self.confirm_password = getpass.getpass("Confirm your password: ")

        if self.password != self.confirm_password:
            print("Passwords do not match.")
            return

        self.save_to_file()
        print("Registration successful!")

    def save_to_file(self):
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "mobile_phone": self.mobile_phone,
            "password": self.password
        }

        with open("users.json", "a") as file:
            json.dump(data, file)
            file.write("\n")

    def login_user(self):
        email = input("Enter your email address: ")
        password = getpass.getpass("Enter your password: ")

        with open("users.json", "r") as file:
            users = file.readlines()

        for user_data in users:
            user = json.loads(user_data)
            if user["email"] == email and user["password"] == password:
                print("Login successful!")
                return user["email"]  # Return the user's email as a unique identifier

        print("Login failed!")
        return None


class Project:
    def __init__(self, title, details, total_target, start_date, end_date, created_by):
        self.title = title
        self.details = details
        self.total_target = total_target
        self.start_date = start_date
        self.end_date = end_date
        self.created_by = created_by

    def create(self, user_email):
        try:
            self.start_date = datetime.datetime.strptime(self.start_date, "%Y-%m-%d")
            self.end_date = datetime.datetime.strptime(self.end_date, "%Y-%m-%d")

            if self.end_date <= self.start_date:
                print("End date should be later than the start date.")
                return
        except ValueError:
            print("Invalid date format.")
            return

        self.save_to_file(user_email)
        print("Project created successfully!")

    def save_to_file(self, user_email):
        data = {
            "title": self.title,
            "details": self.details,
            "total_target": self.total_target,
            "start_date": self.start_date.strftime("%Y-%m-%d"),
            "end_date": self.end_date.strftime("%Y-%m-%d"),
            "created_by": user_email  # Associate the project with the user who created it
        }

        try:
            with open("projects.json", "r") as file:
                projects = json.load(file)
        except FileNotFoundError:
            projects = []

        projects.append(data)

        with open("projects.json", "w") as file:
            json.dump(projects, file)

    def view_all_projects(self):
        try:
            with open("projects.json", "r") as file:
                projects = json.load(file)
        except FileNotFoundError:
            projects = []

        if not projects:
            print("No projects found.")
            return

        for project in projects:
            print("Title:", project["title"])
            print("Details:", project["details"])
            print("Total Target:", project["total_target"])
            print("Start Date:", project["start_date"])
            print("End Date:", project["end_date"])
            print("--------------------")

    def edit(self, user_email):
        with open("projects.json", "r") as file:
            projects = json.load(file)

        if not projects:
            print("No projects found.")
            return

        title = input("Enter the title of the project you want to edit: ")

        for project in projects:
            if project["title"] == title and project["created_by"] == user_email:
                project["details"] = input("Enter the new details: ")
                project["total_target"] = input("Enter the new total target: ")
                project["start_date"] = input("Enter the new start date (YYYY-MM-DD): ")
                project["end_date"] = input("Enter the new end date (YYYY-MM-DD): ")

                with open("projects.json", "w") as file:
                    json.dump(projects, file)

                print("Project edited successfully!")
                return

        print("Project not found or you don't have permission to edit it.")

    def delete(self, user_email):
        with open("projects.json", "r") as file:
            projects = json.load(file)

        if not projects:
            print("No projects found.")
            return

        title = input("Enter the title of the project you want to delete: ")

        for project in projects:
            if project["title"] == title and project["created_by"] == user_email:
                projects.remove(project)

                with open("projects.json", "w") as file:
                    json.dump(projects, file)

                print("Project deleted successfully!")
                return

        print("Project not found or you don't have permission to delete it.")
    
    def search_by_date(self, date):
        with open("projects.json", "r") as file:
            projects = json.load(file)

        found_projects = []
        for project in projects:
            if project["start_date"] <= date <= project["end_date"]:
                found_projects.append(project)

        if found_projects:
            print("Found projects:")
            for project in found_projects:
                print("Title:", project["title"])
                print("Details:", project["details"])
                print("Total Target:", project["total_target"])
                print("Start Date:", project["start_date"])
                print("End Date:", project["end_date"])
                print("--------------------")
        else:
            print("No projects found for the given date.")    
        


# Main program
user = User("", "", "", "", "", "")
choice = ""

while choice != "4":
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        
        user.first_name = input("Enter your first name: ")
        while not user.first_name.isalpha() or not user.first_name.isalnum():
            user.first_name = input("Please enter a valid first name: ")
                
        user.last_name = input("Enter your last name: ")
        while not user.last_name.isalpha() or not user.last_name.isalnum():
            user.last_name = input("Please enter a valid last name: ")
                
        user.email = input("Enter your email address: ")
        while not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
            user.email = input("Please enter a valid email: ")
            
            
        user.mobile_phone = input("Enter your mobile phone number: ")
        while not re.match(r"\+20\d{9}", user.mobile_phone):
            user.mobile_phone = input("Invalid Egyptian phone number format! :")
                
        user.password = getpass.getpass("Enter your password: ")
        user.confirm_password = getpass.getpass("Confirm your password: ")
        while(user.password !=  user.confirm_password):
            print("Passwords do not match.")
            user.password = getpass.getpass("Enter your password: ")
            user.confirm_password = getpass.getpass("Confirm your password: ") 
        user.register()
    elif choice == "2":
        email = user.login_user()

        if email:
            project = Project("", "", "", "", "", "")
            choice = ""

            while choice != "6":
                print("1. Create Project")
                print("2. View All Projects")
                print("3. Edit Project")
                print("4. Delete Project")
                print("5. Search Projects by Date")
                print("6. Logout")
                print("7. Exit")
                choice = input("Enter your choice (1-6): ")

                if choice == "1":
                    project.title = input("Enter project title: ")
                    project.details = input("Enter project details: ")
                    project.total_target = input("Enter project total target: ")
                    project.start_date = input("Enter project start date (YYYY-MM-DD): ")
                    project.end_date = input("Enter project end date (YYYY-MM-DD): ")
                    project.create(email)
                elif choice == "2":
                    project.view_all_projects()
                elif choice == "3":
                    project.edit(email)
                elif choice == "4":
                    project.delete(email)
                elif choice == "5":
                    date = input("Enter the date to search (YYYY-MM-DD): ")
                    project.search_by_date(date)      
                elif choice == "6":
                    print("Logout successful!")
                    break
                elif choice == "7":
                    print("Exiting...")
                else:
                    print("Invalid choice. Please try again.")
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid choice. Please try again.")