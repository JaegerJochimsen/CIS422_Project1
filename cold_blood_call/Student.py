"""
File: Student.py
Description: contains Student class definition for holding student information
Dependencies: None
Author(s): Jaeger Jochimsen 1/12/22
Credit: n/a
Modifications:
    1/15/22 12:45 PM    Jaeger Jochimsen    Added documentation and changed member vars
    1/21/22 12:00 PM    Jaeger Jochimsen    Added absences field and made method changes accordingly
    1/24/22 12:00 PM    Jaeger Jochimsen    Fixed documentation and removed unecessary (uncalled) functions)
"""

class Student(object):
    """
    Form a Student object containing all the info for a student.

    Used By: 
        Classroom.py - used to convert list of list of student info strings to list of student objects

    Members:
        Member Name:                : Type  : Default Val  -> Description
        -----------------------------------------------------------------
        self.__first_name             : str   : None         -> student first name
        self.__last_name              : str   : None         -> student last name
        self.__id_num                 : str   : None         -> student id_number 
        self.__email                  : str   : None         -> student email address
        self.__phonetic               : str   : None         -> student preferred first name pronunciation
        self.__present                : bool  : True         -> present is if student is in class or not 
        self.__spoken                 : bool  : False        -> represents whether or not student has spoken recently (this class or end of last class)
        self.__flag_count             : int   : 0            -> represents whether or not the student has been flagged by instructor
        self.__current_contributions  : int   : 0            -> number of times student has contributed to class discussion for current session
        self.__previous_contributions : int   : 0            -> number of total times student has contributed to class discussion
        self.__previous_flags         : int   : 0            -> number of total times student has been flagged by instructor
        self.__previous_absence       : int   : 0            -> number of total times student has been marked absent

    Methods:
        Example Student : student = Student("Joe", "Summers", "951******", "jSummers@email.com", "Jo-ee", True, False, True, 1, 3, 4, 0)
        Private:
            N/A
        Public:
            Description:    toStrList(self)->list[str]                  :   return a list of strings representing the attributes of the Student object
            Usage:          student.toStrList()                         ->  ["Joe", "Summers", "951******", "jSummers@email.com", "Jo-ee", "True", "False",
                                                                            "True", "1", "3", "4","0"] 

            Description:    getPresent(self)->bool                      :   return the present field of the Student object
            Usage:          student.getPresent()                        ->  True

            Description:    getSpoken(self)->bool                       :   return the spoken field of the Student object
            Usage:          student.getSpoken()                         ->  False

            Description:    incrementFlag(self, n:int = 1)->None        :   increment Student __flag_count field by n; return None
            Usage:          student.incrementFlag()                     ->  None
            
            Description:    setSpoken(self, status:bool)->None          :   set Student object member field to status; return None
            Usage:          student.setSpoken(True)                     ->  None

            Description:    incrementContributions(self, n:int)->None   :   increment the Student object current_contributions field by n; n = 1 by
                                                                            default
            Usage:          student.incrementContributions(5)           ->  None

            Description:    setPresent(self, status:bool)-> None        :   set the present status of Student
            Usage:          student.setPresent(True)                    ->  None

            Description:    incrementAbsences(self, n:int=1)            :   increment previous absence count by n (defaulted to 1)
            Usage:          student.incrementAbsences()                 ->  None

    Additional Notes:
        member variables are marked as private and can only be accessed through methods

    """
    def __init__(self, first_name:str = None, last_name:str = None,
            id_num:str = None, email:str = None, phonetic:str = None,
            present:bool = True, spoken:bool = False, previous_contributions:int = 0,
            previous_flags:int = 0, previous_absences:int = 0):

        self.__first_name = first_name
        self.__last_name = last_name
        self.__id_num = id_num    # this could be int maybe?
        self.__email = email
        self.__phonetic = phonetic
        self.__present = present
        self.__spoken = spoken
        self.__flag_count = 0    # default to unflagged on class start FIXME! Documentation
        self.__current_contributions = 0
        self.__previous_contributions = previous_contributions  # number of contributions throughout the term
        self.__previous_flags = previous_flags # number of flags throughout the term
        self.__previous_absence = previous_absences

    def toStrList(self)->list:
        """Produce list of strings representing the attributes of the Student object"""
        return [self.__first_name, self.__last_name, self.__id_num, self.__email,
                self.__phonetic, str(self.__present), str(self.__spoken),
                str(self.__flag_count), str(self.__current_contributions),
                str(self.__previous_contributions), str(self.__previous_flags), str(self.__previous_absence)]

    def getPresent(self)->bool:
        return self.__present_code

    def getSpoken(self)->bool:
        return self.__spoken

    def incrementFlag(self, n:int = 1)->None:
        self.__flag_count += n
        return None

    def setSpoken(self, status:bool)->None:
        self.__spoken = status
        return None

    def incrementContributions(self, n:int = 1)->None:
        self.__current_contributions += n
        return None

    def setPresent(self, status:bool)->None:
        self.__present = status
        return None

    def incrementAbsences(self, n:int=1)->None:
        self.__previous_absence += n
        return None

    def __str__(self):
        return f"{self.__first_name} {self.__last_name}"

def main():
    """Testing"""
    s = Student("Nick", "Johnstone", "951******", "nsj@gmail.com", "nook",
            "848fsdfhkjhe8f9", "True", 5, 4)
    print(s.toStrList())

if __name__ == "__main__":
    main()


