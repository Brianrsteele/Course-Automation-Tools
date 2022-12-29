import requests
import bs4
import datetime
from datetime import timedelta

# Currently Broken - might be worth fixing.

class ImportantDate():
	"""
	Important date object holds information about a holiday or important date.
	title: a string containing the name or information about the important date ("Spring Break"). 
	start_date: a datetime.date object representing the beginning day of the important date.
	end_date: a datetime.date object representing the end date of the important date.
	"""
	
	def __init__(self, title, start_date, end_date):
		"""
		Constructor for the Important Date class
		"""
		self.title = title
		self.start_date = start_date
		self.end_date = end_date
		self.length = self.end_date - self.start_date
	
	def __repr__(self):
		return self.title + ", " + str(self.start_date) + ", " + str(self.end_date) + ", " + str(self.length)

class RCTCImportantDateScraper():
	"""
	This class creates an object that will look up a given semester and year on the RCTC web site's published
	academic calendar.
	@param: semester The semester for the semester dates
	@param: year The year for the semester dates
	@param: start_date the date the semester starts - given a value in export_important_dates_tuples()
	@param: end_date the date the semester ends - given a value in export_important_dates_tuples()

	"""
	
	def __init__(self, semester, year):
		"""
		Constructor.
		semester: String, 'Fall', 'Spring', or 'Summer'
		year: String, a year in xxxx format, ie. '2018'.
		"""
		self.semester = semester
		self.year = year
		# get a list of dates from the RCTC academic calendar website
		self.important_dates_list = self.download_semester_holidays()
		self.semester_start = None
		self.semester_end = None
		self.dates = []
		
	def __repr__(self):
		return_string = 'Semester: {}\nYear: {}\nStart Date: {}\nEnd Date: {}\n{}'.format(self.semester,
							self.year, self.semester_start, self.semester_end, self.export_important_dates_tuples())
		return return_string
	
	def convert_rctc_months(self, month):
		"""
		This method returns a numerical representation for a month scraped from the RCTC web site's academic
		calendar page.
		month: string, one of the month abbreviations as it appears on the RCTC web site's academic calendar page.
		"""
		if month[-1:] == ".":
			month = month[0:-1]
		return {
			'Jan' : 1,
			'Feb' : 2,
			'Mar' : 3,
			'April' : 4,
			'May' : 5,
			'June' : 6,
			'July' : 7,
			'Aug' : 8,
			'Sept' : 9,
			'Oct' : 10,
			'Nov' : 11,
			'Dec' : 12,
		}[month]
		
	def create_dates(self):
		"""
		This method calls the self.export_important_dates_tuples() method and receives a list of tuples
		in the form ('title', 'Jan. 31, 2019') - where both members are strings.
		The method returns a list of important_date objects.
		If the start and end dates are different, the method creates multiple important_date objects, one for
		each day, and adds them all to the list.
		"""
		raw_dates = self.export_important_dates_tuples()
		for date in raw_dates:
			# Remove character code for space
			date_cleaned = date[1].replace('\xa0', ' ')
			date_cleaned = date_cleaned.split(',')
			year = date_cleaned[1].strip()
			month = date_cleaned[0][0:(date_cleaned[0].find(' ')+1)].strip()
			day = date_cleaned[0][(date_cleaned[0].find(' ')+1):].strip()
			title = date[0]
			# Dates that span multiple days are difficult to handle
			# Look for characters that indicate a span of days and
			# deal with finding the unique dates.
			if "-" in day:
				day = day.split('-')
				start = day[0].strip()
				end = day[1].strip()
			elif "&" in day:
				day = day.split('&')
				start = day[0].strip()
				end = day[1].strip()
			else:
				start = day
				end = day
			start_date = datetime.date(int(year), self.convert_rctc_months(month), int(start))
			end_date = datetime.date(int(year), self.convert_rctc_months(month), int(end))
			new_date = ImportantDate(title, start_date, end_date)
			if new_date.length > datetime.timedelta(days = 0):
				days_difference = new_date.end_date - new_date.start_date
				while days_difference >= timedelta(days = 0):
					temp_date = ImportantDate(
						title, new_date.end_date - days_difference, new_date.end_date - days_difference)
					self.dates.append(temp_date)
					days_difference = days_difference - timedelta(days = 1)
			else:
				self.dates.append(new_date)
		return self.dates
	
	def export_important_dates_tuples(self):
		"""
		returns a list of tuples containing information about important dates in the current 
		semester.
		ex. ('title', 'Jan. 31, 2019')
		"""
		temp_list = []
		# get the indexes of the "Classes begin" and "Semester Ends" events in the RCTCImportantDateScraper class.
		# self.important_dates_list list.
		start_end_positions = self.find_classes_start_end()
		classes_begin, classes_end = start_end_positions
		#find the last day to drop courses in the semester
		drop_begin = classes_begin + 3
		dates_begin = drop_begin + 4

		semester_start_tuple = tuple(self.important_dates_list[classes_begin:classes_begin + 3: 2])
		semester_drop_tuple = tuple(self.important_dates_list[drop_begin:drop_begin + 4: 3])
		semester_end_tuple = tuple(self.important_dates_list[classes_end:classes_end + 3: 2])

		temp_list.append(semester_start_tuple)
		temp_list.append(semester_drop_tuple)
		for item in range(dates_begin, start_end_positions[1] + 1, 3):
			temp_list.append(tuple(self.important_dates_list[item:item + 3: 2]))

		# Assign values to the start and end dates for the semester, parameters in the RCTCImport

		# First, format the dates in yyyy-mm-dd pattern
		start_date = semester_start_tuple[1]
		end_date = semester_end_tuple[1]

		# format the start date as a tuple (yyyy, mm, dd)
		start_year = int(start_date.split(' ')[2])
		start_month = int(self.convert_rctc_months(start_date.split(' ')[0]))
		start_day = int(start_date.split(' ')[1][:-1])

		# format the end date as a tuple (yyyy, mm, dd)
		end_year = int(end_date.split(' ')[2])
		end_month = int(self.convert_rctc_months(end_date.split(' ')[0]))
		end_day = int(end_date.split(' ')[1][:-1])

		# assign start and end dates
		self.semester_start = (start_year, start_month, start_day)
		self.semester_end = (end_year, end_month, end_day)

		return temp_list
				
	def find_classes_start_end(self):
		"""
		returns a tuple of the indexes for the semester start and stop dates contained in self.important_dates_list.
		They aren't at the first and last index positions in the list.
		e.g. "(2, 30)"
		"""

		# the "classes begin" information is at index 2
		start = [self.important_dates_list.index(item) for item in self.important_dates_list if item.endswith('Classes Begin')]
		# the "Semester Ends" information is at the second to last index
		end = [self.important_dates_list.index(item) for item in self.important_dates_list if item.endswith('Ends')]

		if len(start) == 0 or len(end) == 0:
			print("{}, {} doesn't seem to be listed on the RCTC Academic Calendar page.".format(self.semester,
																								self.year))

		return (start[0], end[0])

	def find_semester(self, semester_list):
		"""
		Returns an array of holidays for a given semester and year
		"""
		return_list = []
		for item in semester_list:
			semester_info = item[0].split(' ')
			if semester_info[0].lower() == self.semester.lower() and semester_info[3] == self.year:
				return_list = item	
		return	return_list
	
	def download_semester_holidays(self):
		
		"""
		Returns a list with information about important dates and holidays for a given
		semester at Rochester Community and Technical College. Returns None if not successful.
		pre-conditions: passed semester, year where semester = {"Fall", "Spring", or "Summer"} and
		year is a four digit number like "2018"
		post-condition: none
		invariant: the semester and year passed must be present in the table of important dates at
		https://www.rctc.edu/academics/academic-calendar.
		
		"""
		return_list = None
		#get the RCTC academic calendar page
		req = requests.get("https://www.rctc.edu/academics/academic-calendar/")
		try:
			req.raise_for_status()
		except Exception as exc:
			print("There was a problem: %s" % (exc))	
		#create the beautiful soup object for the RCTC academic calendar page
		academic_calendar = bs4.BeautifulSoup(req.text, features="lxml")
		
		#find all of the tables on the RCTC academic calendar page
		year_tables = academic_calendar.select('table')
		semester_list = []
		#iterate through all of the tables on the RCTC academic calendar page
		for table in year_tables:
			#get the text of the table and clean it up into a useable list
			year_table = table.getText()
			year_list = year_table.split('\n')
			
			for z in year_list:
				print(z)
			
			year_list_clean = [value for value in year_list if value != '']
			
			for z in year_list_clean:
				print(z)
			
			del year_list_clean[:2]
			del year_list_clean[1]
			# print('\n', year_list_clean)
			fall_start = [year_list_clean.index(item) for item in year_list_clean if item.startswith('Fall Semester')]
			
			spring_start = [year_list_clean.index(item) for item in year_list_clean if item.startswith('Spring Semester')]
			summer_start = [year_list_clean.index(item) for item in year_list_clean if item.startswith('Summer Session')]

			"""
				Fixed issue here: This loop is looking through a couple of different tables. A given table 
				might or might not list a given semester, i.e., a table might list Spring and Summer, but not Fall.
				
				This was causing an index out of range exception.
				
				Adding if statements fixed the isssue. 
				
				Only attempt to add the semester dates to the list if the semester is actually listed in
				the current table.
				
				QED.
			"""

			#append just the fall holidays on this table
			if (len(fall_start) > 0):
				semester_list.append(year_list_clean[fall_start[0]:spring_start[0]])
			#append just the spring holidays on this table
			if (len(spring_start) > 0):
				semester_list.append(year_list_clean[spring_start[0]:summer_start[0]])
			#append just the summer holidays on this table
			if (len(summer_start) > 0):
				semester_list.append(year_list_clean[summer_start[0]:])
		return self.find_semester(semester_list)


def main():			
	sem = RCTCImportantDateScraper('Spring Semester –', '2023')
	dates = sem.create_dates()
	for date in dates:
		print(date)
		
if __name__ == '__main__':
	main()



