# semester_important_dates.py
# A program to save a file with a list of all of the class meeting
# session dates for a course during a semester in a format that can be
# imported into an excel file.
import datetime


def main():
    print_purpose()

    correct_date_range = False
    while correct_date_range == False:
        start_date = get_start_date()
        end_date = get_end_date()
        correct_date_range = check_date_range(start_date, end_date)

    semester_info = determine_semester_info(start_date)
    
    meeting_days = get_meeting_days()
    translated_days = translate_days(meeting_days)

    date_list = create_date_list(start_date, end_date)
    class_sessions = create_class_sessions(date_list, translated_days)

    export_dates_to_file(class_sessions, semester_info, meeting_days)


def print_purpose():
    print("""This program prints the meeting sessions for a college course that meets one or more days per week.\n
          """)
    return None


def get_start_date():
    """
    Returns a datetime.date object with the start date of the course.
    """
    print("What is the START date for the course?")
    year = int(input("Enter the YEAR in YYYY format: "))
    month = int(input("Enter the MONTH in MM format: "))
    day = int(input("Enter the DAY in DD format: "))
    print()
    start_date = datetime.date(year, month, day)                        
    return start_date


def get_end_date():
    """
    Returns a datetime.date object with the end date of the course.
    """
    print("What is the END date for the course?")
    year = int(input("Enter the YEAR in YYYY format: "))
    month = int(input("Enter the MONTH in MM format: "))
    day = int(input("Enter the DAY in DD format: "))
    print()
    end_date = datetime.date(year, month, day)                        
    return end_date


def create_date_list(base_date, end_date):
    """
        Returns a list of date objects, starting at the base_date and
        ending at the end_date
    """
    date = base_date
    date_list = []
    while date <= end_date:
        date_list.append(date)
        date = date + datetime.timedelta(days = 1)
    return date_list


def translate_days(days_of_week):
    """
        Returns a tuple of days of the week in number format for the meeting
        days passed in days_of_week in string format. Converts ('Mon', 'Wed') to
        (0, 2), for example
    """
    meeting_days = ()
    for i in days_of_week:
        i = i.lower()
        i = i.strip()
        i = i[0:3]
        if i == "sun":
            meeting_days = meeting_days + (6, )
        elif i == "mon" or i == "m":
            meeting_days = meeting_days + (0, )
        elif i == "tue" or i == "t":
            meeting_days = meeting_days + (1, )
        elif i == "wed" or i == "w":
            meeting_days = meeting_days + (2, )
        elif i == "thu" or i == "th":
            meeting_days = meeting_days + (3, )
        elif i == "fri" or i == "f":
            meeting_days = meeting_days + (4, )
        elif i == "sat" or i == "s":
            meeting_days = meeting_days + (5, )
        else:
            return None
    return meeting_days


def create_class_sessions(date_list, days_of_week):
    """
        Given a list of dates, this function returns a list of only the class
        meeting sessions based on a tuple of days of the week.
    """
    class_sessions = []
    for i in date_list:
        if i.weekday() in days_of_week:
            class_sessions.append(i)
    return class_sessions


def check_date_range(start_date, end_date):
    """ Given a start_date and end_date, this function determines if
        the start date is before the end date, or if the dates are in the
        past.
    """
    if end_date <= start_date:
        print("*--------------------------------------------------------*")
        print("Ooops, your end date is before your start date. Try again.")
        print("*--------------------------------------------------------*\n")
        return False
    elif start_date < datetime.date.today():
        print("*--------------------------------------------------------*")
        print("Ooops, these dates already passed. Try again.")
        print("*--------------------------------------------------------*\n")
        return False
    else: return True


def determine_semester_info(start_date):
    """ Give a date object, this function returns the semester and year
        that the class occurs, in string format
    """
    year = start_date.strftime('%Y')
    month = int(start_date.strftime('%m'))
    if month >= 8 and month <= 12:
        semester = "Fall"
    elif month >= 1 and month <= 4:
        semester = "Spring"
    elif month >= 5 and month <= 7:
        semester = "Summer"
    else:
        semester = "Unknown Semester"
    semester_info = semester + ", " + year
    return semester_info


def get_meeting_days():
    """
    Returns a tuple of three letter abbreviations for days that the course
    meets during the week in a format like this ('mon', 'wed', 'fri').
    """
    print("What days of the week does this course meet?")
    print("Please enter the days using three letter abbreviations")
    print("separated by commas, i.e. 'mon', 'wed', 'fri'")
    input_days = input("What weekdays does the class meet each week: ")
    input_days = input_days.split(',')
    meeting_days = ()
    for i in input_days:
        i = i.strip()
        i = i.lower()
        i = i[0:3]
        meeting_days = meeting_days + (i,)
    return meeting_days


def print_dates(date_list, semester_info):
    """
        Prints a list of date objects in a more legible form.
    """
    print(semester_info)
    print("day, date")
    for day in date_list:
        print("{0}, {1}/{2}/{3}".format(day.strftime('%a'), day.month, day.day, day.year))


def export_dates_to_file(class_sessions, semester_info, meeting_days):
    """ Given a list of class sessions, this function exports a file
        with a list of meeting days and dates in the format "day, date", i.e.
        "Mon, 01/11/2016". The file is saved to the desktop and titled with
        the semester, year, and meeting days, i.e. "SPRING_2016_Mon_Wed.txt"
    """
    my_title = create_title(semester_info, meeting_days)
    location =  my_title
    
    session = []
    for date in class_sessions:
        session.append(date.strftime('%a, %m/%d/%Y\n'))
        
    export_file = open(location, "w")
    
    for i in session:
        export_file.write(i)
    export_file.close()
    print("You can find a text file with dates in 'Dropbox/Python/syllabus project/'")
    return None


def create_title(semester_info, meeting_days):
    """ Creates a title based on the semester info and meeting days,
        in the format "SPRING_2016_Tue_Thu.txt".
    """
    title = ""
    sem = semester_info.upper()
    clean_sem = ''
    for i in sem:
        if i == " ":
            continue
        else:
            clean_sem += i
    sem = clean_sem.split(",")
    sem = "_".join(sem)
    title += sem
    for i in meeting_days:
        i = i.upper()
        title = title + "_" + i
    title += ".txt"
    return title

main()
