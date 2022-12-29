import datetime
import rctc_scrape_dates




class importantCourseDateList:	
	"""
	Creates a list of meeting sessions for a college course, starting on start_date and ending on end_date.
	if a meeting session is in the important_dates list, the important_date_list object will be appended to
	the list of meeting sessions, recording holidays and other special days in the schedule
	start_date: a datetime.date object representing the staring date of a course
	end_date: a datetime.date object representing the ending date of a course
	days_of_week: a tuple with the meeting days of the week in integer format,
		i.e. ('Mon', 'Wed') == (0, 2)
	important_dates: list of ImportantDate objects
	
	"""

	def __init__(self, start_date, end_date, days_of_week, important_dates):
		self.start_date = start_date
		self.end_date = end_date
		self.days_of_week = days_of_week
		self.important_dates = important_dates
		self.date_list = self.create_date_list()

	def create_date_list(self):
		"""
		Returns a list of date objects, starting at the base_date and
		ending at the end_date
		"""
		date = self.start_date
		date_list = []
		while date <= self.end_date:
			if date.weekday() in self.days_of_week:
				session = rctc_scrape_dates.ImportantDate('', date, date)
				for item in self.important_dates:
					if item.start_date == session.start_date:
						session = item			
				date_list.append(session)
			date = date + datetime.timedelta(days = 1)
		return date_list

def main():
		# Create an object to scrape dates from the RCTC Academic Calendar page
		sem = rctc_scrape_dates.RCTCImportantDateScraper('Spring', '2023')

		# use create_dates() to create a list of important dates from the RCTC Academic Calendar
		important_dates = sem.create_dates()

		start_date = datetime.date(sem.semester_start[0], sem.semester_start[1], sem.semester_start[2])
		end_date = datetime.date(sem.semester_end[0], sem.semester_end[1], sem.semester_end[2])

		days_of_week = (0, 2)

		semester = importantCourseDateList(start_date, end_date, days_of_week, important_dates)

		for session in semester.date_list:
			print("{0}, {1}/{2}/{3}: {4}".format(session.start_date.strftime('%a'), session.start_date.month,
							session.start_date.day, session.start_date.year, session.title))


if __name__ == '__main__': 
	main()
