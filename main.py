from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

# JSON 파일 경로 (main.py와 같은 폴더)
DATA_FILE = "courses.json"

# 수강기록 하나의 구조를 정의 (입력값 검증용)
class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str


# JSON 파일에서 데이터 읽기
def load_courses():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# JSON 파일에 데이터 저장
def save_courses(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# GET /courses - 전체 수강기록 반환
@app.get("/courses")
def get_courses():
    try:
        courses = load_courses()
        return courses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# POST /courses - 새 과목 추가
@app.post("/courses")
def add_course(course: Course):
    try:
        courses = load_courses()
        courses.append(course.dict())
        save_courses(courses)
        return {"message": "과목이 추가되었습니다.", "added": course}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))