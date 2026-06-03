from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

DATA_FILE = "courses.json"

class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

def load_courses():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_courses(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.get("/courses")
def get_courses():
    try:
        courses = load_courses()
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/courses")
def add_course(course: Course):
    try:
        courses = load_courses()
        courses.append(course.dict())
        save_courses(courses)
        return {"message": "과목이 추가되었습니다.", "added": course}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))