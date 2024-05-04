import pydantic
import typing
import json
from json.decoder import JSONDecodeError 

def write_to_file(new_data):
    filename = "emp_details.json"
    try:
        with open(filename, 'r') as openfile:
            existing = json.load(openfile)
    except:
        existing = []
    existing.append(new_data)
    with open(filename, "w") as file:
        json.dump(existing, file)

class Emp_Details(pydantic.BaseModel):
    name: str
    emp_id: int
    title: str
    dept: str

class Employee:
    def __init__(self, employee: Emp_Details):
        self.name = employee.name
        self.emp_id = employee.emp_id
        self.title = employee.title
        self.dept = employee.dept

    def display_emp(self):
        """This function to display the employee details"""
        print("Employee details are :")
        print(f"Name: {self.name}, ID: {self.emp_id}, Title: {self.title}, Department: {self.dept}")

    def to_dict(self):
        return {
            'name': self.name,
            'emp_id': self.emp_id,
            'title': self.title,
            'department': self.dept
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['emp_id'], data['title'], data['dept'])
        
class Department:
    def __init__(self, dept_name):
        self.dept_name = dept_name
        self.employees = []

    def add_emp(self, employee):
        """This function to add the employee details for respective department"""
        if employee not in self.employees:
            self.employees.append(employee)
            print(f"Employee: {employee} added to the department {self.dept_name}")
        else:
            print(f"This employee not belongs to the department {self.dept_name}")

    def remove_emp(self, employee_id):
        for i, data in enumerate(self.employee):
            if employee_id == data['emp_id']:
                self.employees.pop(i)
                print(f"Employee removed from the department {self.dept_name}")
            else:
                print(f"Employee Not found in the department {self.dept_name}")
    
    def display_employees(self):
        for emp in self.employees:
            print(emp)
    
    def to_dict(self):
        return {
            'department_name': self.department_name,
            'employees': [emp.to_dict() for emp in self.employees]
        }

    @classmethod
    def from_dict(cls, data):
        department = cls(data['department_name'])
        department.employees = [Employee.from_dict(emp_data) for emp_data in data['employees']]
        return department

class Company:
    def __init__(self):
        self.departments = {}
        self.load_data()

    def add_dept(self, department_name):
        if department_name not in self.departments:
            self.departments[department_name] = Department(department_name)
            print("Added department to the company")
        else:
            print("Department already present in the company")

    def remove_dept(self, department_name):
        if department_name in self.departments:
            del self.departments[department_name]
            print("Removed department from the company")
        else:
            print("Department not found in the company")

    def dispaly_all(self):
        print("Below are the department details under the company")
        print(self.company)

    def dispaly_departments(self):
        print("Below are the departments under the company")
        print([d['dept_name'] for d in self.company])

    def save_data(self):
        with open('emp_details.json', 'w') as output:
            json.dump({dept_name: dept.to_dict() for dept_name, dept in self.departments.items()}, output, indent=4)

    def load_data(self):
        try:
            with open('emp_details.json', 'r') as input:
                data = json.load(input)
                self.departments = {dept_name: Department.from_dict(dept_data) for dept_name, dept_data in data.items()}
        except (FileNotFoundError, JSONDecodeError):
            self.departments = {}
    
def print_menu():
    print("""
    1. Add Employee
    2. Remove Employee
    3. List All Employees in Department
    4. Add Department
    5. Remove Department
    6. List All Departments
    7. Exit
    """)

def main():
    print("Welcome to the Employee Management system")
    while True:
        company = Company()
        print_menu()
        try:
            user_input = input("Please select any one of the above to perform the action\n")
            if user_input == '1':
                name = input("Enter employee's name: ")
                emp_id = input("Enter employee ID: ")
                title = input("Enter employee's title: ")
                dept = input("Enter department: ")
                if dept not in company.departments:
                    print("Department does not exist.")
                    continue
                emp = Employee(name, emp_id, title, dept)
                company.departments[dept].add_emp(emp)
                company.save_data()
            elif user_input == '2':
                emp_id = input("Enter employee ID to remove: ")
                dept = input("Enter department: ")
                if department in company.departments:
                    company.departments[department].remove_emp(emp_id)
                    company.save_data()
                else:
                    print("Department does not exist.")
            elif user_input == '3':
                department = input("Enter department to list employees: ")
                if department in company.departments:
                    company.departments[department].display_employees()
                    company.save_data()
                else:
                    print("Department does not exist.")
            elif user_input == '4':
                department_name = input("Enter new department name: ")
                company.add_dept(department_name)
                company.save_data()
            elif user_input == '5':
                department_name = input("Enter department name to remove: ")
                company.remove_dept(department_name)
                company.save_data()
            elif user_input == '6':
                company.display_departments()
            elif user_input == '7':
                company.save_data()
                break
            else:
                print("Invalid option. Please try again.")
        except Exception as e:
            print("Please enter a valid integer as a input")

if __name__ == "__main__":
    main()
