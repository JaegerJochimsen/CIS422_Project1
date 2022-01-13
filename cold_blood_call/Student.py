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
    def __init__(self, first_name:str = None, last_name:str = None, id_num:str = None, email:str = None, phonetic:str = None, reveal:str = None, spoken:bool = False):
        self.first_name = first_name
        self.last_name = last_name
        self.id_num = id_num    # this could be int maybe?
        self.email = email
        self.phonetic = phonetic
        self.reveal_code = reveal
        self.spoken = False     # default to not spoken on class start
        self.flagged = False    # default to unflagged on class start
        self.contributions = 0  # default to 0 contributions on class start

    #def __repr__(self):
    #    return f'Student({self.first_name},{self.last_name},{self.spoken},{self.flagged},{self.contributions},{self.spoken})'

    #def __str__(self):
    #    return f'Student(name:{self.name},contact:{self.contact},spoken:{self.spoken},flagged:{self.flagged},contrib:{self.contributions},spoken:{self.spoken})'

    def toStrList(self)->list[str]:
        return [self.first_name, self.last_name, self.id_num, self.email, self.phonetic, self.reveal_code, str(self.spoken), str(self.flagged), str(self.contributions)]

    def getFirst(self)->str:
        return self.first_name

    def getLast(self)->str:
        return self.last_name

    def getID(self)->str:
        return self.id_num

    def getEmail(self)->str:
        return self.email
    
    def getPhonetic(self)->str:
        return self.phonetic

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





