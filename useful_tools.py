import markdown
import docx
from Markdown2docx import Markdown2docx

# Planning an update that would spin out a course syllabus and weekly schedule
# from data in json files.

# https://pypi.org/project/Markdown2docx/#description
# https://python-docx.readthedocs.io/en/latest/
# https://python-markdown.github.io
# https://pypi.org/project/markdown2/

# https://jinja.palletsprojects.com/en/3.1.x/api/#basics
# https://mlhive.com/2022/03/working-with-lists-in-python-docx
# https://pypi.org/project/docxtpl/


my_string = """
# My Title #
All the world's indeed a stage and we are merely players.
            
* Performers
* Portrayers
* Each another's audience"""

html = markdown.markdown(my_string)

print(html)

project = Markdown2docx('test')
project.eat_soup()
project.save()