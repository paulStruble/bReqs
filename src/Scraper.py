import requests
from bs4 import BeautifulSoup
from lxml import html
import re


class Course:
    """A course containing relevant information such as its code, title, description, etc."""
    # TODO: complete implementation
    def __init__(self, course):
        self.code = None
        self.title = None
        self.units = None
        self.terms_offered = None
        self.description = None
        self.prerequisites = None
        self.hours_and_format = None
        self.additional_details = None


class Scraper:
    """A webscraper used to extract course information from the official Berkeley course catalog"""

    def get_course_tags(self) -> list[str]:
        """Get a list of all course tags"""
        course_tags = []

        catalog_response = requests.get('https://guide.berkeley.edu/courses/')
        if catalog_response.status_code == 200:
            catalog_soup = BeautifulSoup(catalog_response.content, 'lxml')
            for link in catalog_soup.find_all('a'):
                href = link.get('href')
                if href is not None and re.match(r'/courses/.+', href) is not None:
                    course_tag = href.split('/')[-2]
                    if course_tag != 'courses':
                        course_tags.append(course_tag)
        else:
            raise Exception(f'Failed to fetch course catalog. Status code: {catalog_response.status_code}')

        return course_tags

    def get_courses(self, course_tag: str) -> list[Course]:
        """Get a list of Course objects for all courses with this course tag"""
        courses = []

        course_response = requests.get('https://guide.berkeley.edu/courses/' + course_tag + '/')
        if course_response.status_code == 200:
            course_soup = BeautifulSoup(course_response.content, 'lxml')
            for courseblock in course_soup.find_all(class_='courseblock', recursive=True):
                course = self.courseblock_to_description(courseblock)
                courses.append(course)
        else:
            raise Exception(f'Failed to fetch [{course_tag.capitalize()}] course descriptions. Status code: {course_response.status_code}')

        return courses

    def courseblock_to_description(self, course_description: str) -> Course:
        """Convert a courseblock into a Course object"""
        pass
        # TODO: implement


if __name__ == '__main__':
    scraper = Scraper()
    course_tags = scraper.get_course_tags()
    print(course_tags)
    course_descriptions = scraper.get_courses(course_tags[0])

    # Each letter in alphabet has a section for departments/majors starting with that latter
    # Each letter has a <ul> of department/major links
