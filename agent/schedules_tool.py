import requests
from langchain_core.tools import tool

BASE_URL = "http://127.0.0.1:8000/api/schedules"


@tool
def get_lectures(year: str = None, day: str = None, course: str = None) -> str:
    """
    Get lectures filtered by year, day, or course.
    year can be "1st", "2nd", "3rd", or "4th".
    day can be "Monday", "Tuesday", "Wednesday", "Thursday", or "Friday".
    """

    params = {}
    if year:
        params["year"] = year
    if day:
        params["day"] = day
    if course:
        params["course"] = course

    response = requests.get(f"{BASE_URL}/lectures/", params=params)

    if response.status_code != 200:
        return "Error fetching lectures."

    lectures = response.json()

    if not lectures:
        return "No lectures found."

    result = ""
    for lec in lectures:
        result += f"""
Course: {lec['course_name']}
Day: {lec['day_of_week']}
Lecturer: {lec['lecturer']}
Start: {lec['start_time']}
End: {lec['end_time']}
-------------------
"""
    return result

@tool
def get_exams(year: str = None, course: str = None) -> str:
    """
    Get exams filtered by year or course.
    """

    params = {}
    if year:
        params["year"] = year
    if course:
        params["course"] = course

    response = requests.get(f"{BASE_URL}/exams/", params=params)

    if response.status_code != 200:
        return "Error fetching exams."

    exams = response.json()

    if not exams:
        return "No exams found."

    result = ""
    for exam in exams:
        result += f"""
Course: {exam['course_name']}
Date: {exam['date']}
Start: {exam['start_time']}
End: {exam['end_time']}
-------------------
"""
    return result