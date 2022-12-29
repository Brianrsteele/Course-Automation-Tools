import rctc_scrape_dates
import schedule_list_maker
from tkinter import *
from tkinter import filedialog
import datetime

# GUI tool to scrape a schedule from the RCTC academic calendar
# Currently not working - scraping the site is proving to be difficult
# as the html changes sort of unpredictably.

# Create a Tkinter object
root = Tk()
# Add the window title
root.title('RCTC Schedule Tool')



def quit_app():
    """
        Quits the application and closes the window.
    """
    root.destroy()


def submit():
    """
        Passes semester and year values to an RCTCImportantDates scraper object to scrape a list of important
        dates from the RCTC Academic calendar at https://www.rctc.edu/academics/academic-calendar/. Then creates a
        list of class meeting dates from the start_entry date to the end_entry date which includes only the
        days_of_week tuple. Saves a .txt file with the class meeting dates and holidays/non-meeting dates from the
        academic calendar listed in their appropriate date.
    """

    semester_str = str(semester.get())
    year_str = str(year.get())
    days_of_week = ()
    if str(mon.get()) == '1':
        days_of_week = days_of_week + (0,)
    if str(tue.get()) == '1':
        days_of_week = days_of_week + (1,)
    if str(wed.get()) == '1':
        days_of_week = days_of_week + (2,)
    if str(thu.get()) == '1':
        days_of_week = days_of_week + (3,)
    if str(fri.get()) == '1':
        days_of_week = days_of_week + (4,)
    if str(sat.get()) == '1':
        days_of_week = days_of_week + (5,)
    if str(sun.get()) == '1':
        days_of_week = days_of_week + (6,)
    
    sem = rctc_scrape_dates.RCTCImportantDateScraper(semester_str, year_str)

    try:
        important_dates = sem.create_dates()
    except IndexError as e:
        print(e)


    start_date = datetime.date(sem.semester_start[0], sem.semester_start[1], sem.semester_start[2])
    end_date = datetime.date(sem.semester_end[0], sem.semester_end[1], sem.semester_end[2])

    my_semester = schedule_list_maker.importantCourseDateList(start_date, end_date, days_of_week,
                                       important_dates)

    file_contents = ''
    
    for session in my_semester.date_list:
        file_contents = file_contents + ("{0}, {1}/{2}/{3}: {4}\n".format(session.start_date.strftime('%a'), session.start_date.month,
					    session.start_date.day, session.start_date.year, session.title))

    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    f.write(file_contents)
    f.close()
    
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Quit", command = quit_app)
menubar.add_cascade(label = "File", menu=filemenu)
root.config(menu=menubar)


# Set the Semester ----------------------------------------------------
semester_label = Label(root, text = 'Semester: ')
semester_label.grid(row = 0, column = 0, sticky = 'e', padx = 2, pady = 5)
semester = StringVar()
semester_entry = Entry(root, textvariable = semester)
semester_entry.grid(row = 0, column = 1, sticky = 'w' , padx = 2, pady = 5)
# Insert default values
semester_entry.insert(0, "Spring")

# Set the Year ----------------------------------------------------
year_label = Label(root, text = 'Year: ')
year_label.grid(row = 1, column = 0, sticky = 'e', padx = 2, pady = 5)
year = StringVar()
year_entry = Entry(root, textvariable = year)
year_entry.grid(row = 1, column = 1, sticky = 'w', padx = 2, pady = 5)
# Insert default values
year_entry.insert(0, "2019")



# Days of the week radio buttons------------------------------------
# Monday
mon = IntVar()
mon_checkbutton = Checkbutton(root, text = 'Monday', variable = mon)
mon_checkbutton.grid(row = 4, column = 1, sticky = 'w', padx = 5)
# Tuesday
tue = IntVar()
tue_checkbutton = Checkbutton(root, text = 'Tuesday', variable = tue)
tue_checkbutton.grid(row = 5, column = 1, sticky = 'w',  padx = 5)
# Wednesday
wed = IntVar()
wed_checkbutton = Checkbutton(root, text = 'Wednesday', variable = wed)
wed_checkbutton.grid(row = 6, column = 1, sticky = 'w',  padx = 5)
# Thursday
thu = IntVar()
thu_checkbutton = Checkbutton(root, text = 'Thursday', variable = thu)
thu_checkbutton.grid(row = 7, column = 1, sticky = 'w',  padx = 5)
# Friday
fri = IntVar()
fri_checkbutton = Checkbutton(root, text = 'Friday', variable = fri)
fri_checkbutton.grid(row = 8, column = 1, sticky = 'w',  padx = 5)
# Saturday
sat = IntVar()
sat_checkbutton = Checkbutton(root, text = 'Saturday', variable = sat)
sat_checkbutton.grid(row = 9, column = 1, sticky = 'w',  padx = 5)
# Sunday
sun = IntVar()
sun_checkbutton = Checkbutton(root, text = 'Sunday', variable = sun)
sun_checkbutton.grid(row = 10, column = 1, sticky = 'w',  padx = 5)

# Create Schedule/Submit button -------------------------------------------------
submit_button = Button(root, text = 'Create Schedule', command = submit)
submit_button.grid(row = 11, column = 1, sticky = 'e', padx = 10, pady = 10)


root.mainloop()
