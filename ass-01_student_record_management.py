# STUDENT RECORD MANAGEMENT
import json
import re

class Student:
   
    def __init__(self, student_id, name, branch, year, marks):
        self.student_id = student_id
        self.name = name
        self.branch = branch
        self.year = year
        self.marks = marks

    def to_dict(self):
        
        return {
            'student_id': self.student_id,
            'name': self.name,
            'branch': self.branch,
            'year': self.year,
            'marks': self.marks
        }

    @staticmethod
    def from_dict(data):
        
        return Student(
            data['student_id'],
            data['name'],
            data['branch'],
            data['year'],
            data['marks']
        )

class ValidationError(Exception):
    
    pass

class StudentManager:
    
    def __init__(self, filename='students.json'):
        self.filename = filename
        self.students = self.load_students()

    def load_students(self, student_id, name, branch, year, marks):
        
        try:
            if not re.match(r'^\d{4}$', student_id):
                raise ValidationError("Student ID must be a 4-digit number.")
            if not name.replace(" ", "").isalpha():
                raise ValidationError("Name must contain only letters and spaces.")
            if not branch.isalpha():
                raise ValidationError("Branch must contain only letters.")
            if not (1 <= year <= 4):
                raise ValidationError("Year must be between 1 and 4.")
            if not (0 <= marks <= 100):
                raise ValidationError("Marks must be between 0 and 100.")
            return True
        except ValidationError as e:
            raise ValidationError(str(e))

    def load_students(self):
        
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return [Student.from_dict(record) for record in data]
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.filename, 'w') as file:
                json.dump([], file)
            return []
        except PermissionError:
            print("Error: No permission to to read/write the file.")
            raise

    def save_students(self):
        
        try:
            with open(self.filename, 'w') as file:
                json.dump([student.to_dict() for student in self.students], file, indent=2)
        except PermissionError:
            print("Error: Unable to write to to file.")
            raise

    def add_student(self, student_id, name, branch, year, marks):
        
        try:
            self.validate_input(student_id, name, branch, year, marks)
            if any(student.student_id == student_id for student in self.students):
                print("Error: Student ID already exists!")
                return
            self.students.append(Student(student_id, name, branch, year, marks))
            self.save_students()
            print("Student added successfully!")
        except ValidationError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def view_students(self, sort_by='student_id'):
        
        if not self.students:
            print("No records found.")
            return
        try:
            valid_fields = ['student_id', 'name', 'branch', 'year', 'marks']
            if sort_by not in valid_fields:
                sort_by = 'student_id'
            sorted_students = sorted(self.students, key=lambda x: getattr(x, sort_by))
            print("\n{:<10} {:<20} {:<10} {:<5} {:<10}".format("Student ID", "Name", "Branch", "Year", "Marks"))
            print("-" * 60)
            for student in sorted_students:
                print(f"{student.student_id:<10} {student.name:<20} {student.branch:<10} {student.year:<5} {student.marks:<10}")
        except Exception as e:
            print(f"Error displaying records: {e}")

    def update_student(self, student_id, name=None, branch=None, year=None, marks=None):
       
        try:
            for student in self.students:
                if student.student_id == student_id:
                    if name:
                        self.validate_input(student_id, name, student.branch, student.year, student.marks)
                        student.name = name
                    if branch:
                        self.validate_input(student_id, student.name, branch, student.year, student.marks)
                        student.branch = branch
                    if year is not None:
                        self.validate_input(student_id, student.name, student.branch, year, student.marks)
                        student.year = year
                    if marks is not None:
                        self.validate_input(student_id, student.name, student.branch, student.year, marks)
                        student.marks = marks
                    self.save_students()
                    print("Student updated successfully!")
                    return True
                print("Error: Student ID not found.")
                return False
        except ValidationError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def delete_student(self, student_id):
      
        try:
            for i, student in enumerate(self.students):
                if student.student_id == student_id:
                    self.students.pop(i)
                    self.save_students()
                    print("Student deleted successfully!")
                    return True
            print("Error: Student ID not found!")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False

def main():
    
    manager = StudentManager()
    while True:
        print("\nStudent Record Management System")
        print("====================================")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Exit")
        try:
            choice = input("Enter choice (1-5): ")
            if choice == '1':
                student_id = input("Enter Student ID (4 digits): ")
                name = input("Enter Name: ")
                branch = input("Enter Branch: ")
                year = int(input("Enter Year (1-4): "))
                marks = float(input("Enter Marks (0-100): "))
                manager.add_student(student_id, name, branch, year, marks)

            elif choice == '2':
                sort_by = input("Sort by (id, name, branch, year, marks) [default: id]: ").lower()
                if not sort_by:
                    sort_by = 'student_id'
                manager.view_students(sort_by)

            elif choice == '3':
                student_id = input("Enter Student ID to to update: ")
                name = input("Enter new Name (or press Enter to skip): ")
                branch = input("Enter new Branch (or press Enter to to skip): ")
                year = input("Enter new Year (1-4, or press Enter to to skip): ")
                marks = input("Enter new Marks (0-100, or press Enter to skip): ")
                year = int(year) if year else None
                marks = float(marks) if marks else None
                manager.update_student(student_id, name, marks, branch, year, marks)

            elif choice == '4':
                student_id = input("Enter Student ID to delete: ")
                manager.delete_student(student_id)

            elif choice == '5':
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")
        except ValueError:
            print("Error: Please enter valid numeric values for year and marks.")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()