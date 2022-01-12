"""
File: Student.py
Description: contains Student class definition for holding student information
Dependencies: None
Author(s): Jaeger Jochimsen 1/12/22
Credit:
"""

class Student(object):
    """
    Student Class Definition
    - Holds a single student's information 
    - Gives methods for changing/reading student information
    """
    # FIXME: may need to reorder this based on file input format
    # Default to None vals, then use getters and setters to fill out if not
    # given in the constructor call
    def __init__(self, name:str = None, contact:str = None, spoken:bool = False):
        self.name = name
        self.contact = contact
        self.spoken = spoken
        self.flagged = False    # default to unflagged on class start
        self.contributions = 0  # default to 0 contributions on class start
        self.spoken = False     # default to not spoken on class start

    def __repr__(self):
        return f'Student({self.name},{self.contact},{self.spoken},{self.flagged},{self.contributions},{self.spoken})'

    def __str__(self):
        return f'Student(name:{self.name},contact:{self.contact},spoken:{self.spoken},flagged:{self.flagged},contrib:{self.contributions},spoken:{self.spoken})'

    def getName(self)->str:
        return self.name

    def getContact(self)->str:
        return self.contact

    def getContributions(self)->int:
        return self.contributions

    def getFlag(self)->bool:
        return self.flagged

    def setFlag(self, status:bool)->None:
        self.flagged = status
        return None

    def incrementContributions(self, n:int = 1)->None:
        self.contributions += n
        return None

    def setSpoken(self, status:bool)->None:
        self.spoken = status
        return None





