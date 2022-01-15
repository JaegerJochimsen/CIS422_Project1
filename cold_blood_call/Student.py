"""
File: Student.py
Description: contains Student class definition for holding student information
Dependencies: None
Author(s): Jaeger Jochimsen 1/12/22
Credit: n/a
"""

class Student(object):
    """
    Form a Student object containing all the info for a student.

    Used By: 
        Classroom.py - used to convert list of list of student info strings to list of student objects

    Members:
        Member Name:                : Type  : Default Val  -> Description
        -----------------------------------------------------------------
        self.first_name             : str   : None         -> student first name
        self.last_name              : str   : None         -> student last name
        self.id_num                 : str   : None         -> student id_number 
        self.email                  : str   : None         -> student email address
        self.phonetic               : str   : None         -> student preferred first name pronunciation
        self.reveal                 : str   : None         -> reveal code associated with student
        self.spoken                 : bool  : False        -> represents whether or not student has spoken recently (this class or end of last class)
        self.flagged                : bool  : False        -> represents whether or not the student has been flagged by instructor
        self.previous_flags         : int   : 0            -> number of total times student has been flagged by instructor
        self.current_contributions  : int   : 0            -> number of times student has contributed to class discussion for current session
        self.previous_contributions : int   : 0            -> number of total times student has contributed to class discussion

    Methods:
        Example Student : student = Student("Joe", "Summers", "951******", "jSummers@email.com", "Jo-ee", "REVEAL1", False, True, 1, 3, 4)
        Private:
            N/A
        Public:
            Description:    toStrList(self)->list[str]      :   return a list of strings representing the attributes of the Student object
            Usage:          student.toStrList()             ->  ["Joe", "Summers", "951******", "jSummers@email.com", "Jo-ee", "REVEAL1", "False",
                                                                "True", "1", "3", "4"] 
            
            Desciption:     getFirst(self)->str             :   return the first_name field of the Student object
            Usage:          student.getFirst()              ->  "Joe"

            Desciption:     getLast(self)->str              :   return the last_name field of the Student object
            Usage:          student.getLast()               ->  "Summers"

            Description:    getID(self)->str                :   return the id_num field of the Student object
            Usage:          student.getID()                 ->  "951******"

            Description:    getEmail(self)->str             :   return the email field of the Student object
            Usage:          student.getEmail()              ->  "jSummers@email.com"

            Description:    getPhonetic(self)->str          :   return the phonetic field of the Student object
            Usage:          student.getPhonetic()           ->  "Jo-ee"

            Description:    getReveal(self)->str            :   return the reveal_code field of the Student object
            Usage:          student.getReveal()             ->  "REVEAL1"

            Description:    getSpoken(self)->bool           :   return the spoken field of the Student object
            Usage:          student.getSpoken()             ->  False

            Description:    getFlag(self)->bool             :   return the flagged field of the Student object
            Usage:          student.getFlag()               ->  True

            Description:    getContributions(self)->int     :   return the current_contributions field of the Student object
            Usage:          student.getContributions()      ->  3

            Description:    getPrevContributions(self)->int :   return the previous_contributions field of the Student object
            Usage:          student.getPrevContributions()  ->  4

            Description:    getPrevFlags(self)->int         :   return the previous_flags field of the Student object
            Usage:          student.getPrevFlags()          ->  1

    Additional Notes:

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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def main():
    """Testing"""
    s = Student("Nick", "Johnstone", "951******", "nsj@gmail.com", "nook",
            "848fsdfhkjhe8f9", "True", 5, 4)
    print(s.toStrList())

if __name__ == "__main__":
    main()


