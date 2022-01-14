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
    def __init__(self, first_name:str = None, last_name:str = None,
            id_num:str = None, email:str = None, phonetic:str = None,
            reveal:str = None, spoken:bool = False, previous_contributions:int = 0,
            previous_flags:int = 0):

        self.first_name = first_name
        self.last_name = last_name
        self.id_num = id_num    # this could be int maybe?
        self.email = email
        self.phonetic = phonetic
        self.reveal_code = reveal
        self.spoken = spoken
        self.flagged = False    # default to unflagged on class start
        self.current_contributions = 0
        self.previous_contributions = previous_contributions  # number of contributions throughout the term
        self.previous_flags = previous_flags # number of flags throughout the term

    def toStrList(self)->list:
        return [self.first_name, self.last_name, self.id_num, self.email,
                self.phonetic, self.reveal_code, str(self.spoken),
                str(self.flagged), str(self.current_contributions),
                str(self.previous_contributions), str(self.previous_flags)]

    def getSpoken(self)->bool:
        return self.spoken

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
        return self.curent_contributions

    def getFlag(self)->bool:
        return self.flagged

    def setFlag(self, status:bool)->None:
        self.flagged = status
        return None

    def incrementContributions(self, n:int = 1)->None:
        self.current_contributions += n
        return None

    def setSpoken(self, status:bool)->None:
        self.spoken = status
        return None

def main():
    """Testing"""
    s = Student("Nick", "Johnstone", "951******", "nsj@gmail.com", "nook",
            "848fsdfhkjhe8f9", "True", 5, 4)
    print(s.toStrList())

if __name__ == "__main__":
    main()


