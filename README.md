# BITS ERP portal
Student portal for creating timetable according to randomly generated priority numbers

# Features
1. Student registration by admin(superuser) only
2. Admin generates the PR numbers which determine the time slot for student timetable registration
3. Class slots with fixed number of student seats 
4. Validation of required subjects
5. Timetable display

# Models
1. slot
    * course -> Course code of subject (eg- CSF111)
    * name -> Subject Name (eg- Computer Programming)
    * teacher -> Teacher Name
    * day -> Number corresponding to day (0-6)
    * hour -> Number corresponding to time(1-9) (eg- 8:00-8:50am -> 1)
    * totalseats -> Total seats a class can have
    * availableseats -> Available seats of that class
    * stype -> Lec, Tut, Prac (lecture tutorial or practical)
    * room -> Location of class
    
2. Erpuser
    * semester 
    * bitsid -> eg- 2016A7PS064P
    * cgpa
    * timetable
    * record -> Course codes( with line break) should be entered that a student is  permitted to take 
    * pr -> priority numbers
