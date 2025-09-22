from database.models import User, Student
from database.database import SessionLocal


def user_exists(user_id: int) -> bool:
    db = SessionLocal()
    try:
        exists = db.query(User).filter(User.id == user_id).first() is not None
        return exists
    finally:
        db.close()

def add_user(user_id: int, first_name: str, last_name: str | None, username: str | None):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.id == user_id).first()
    
    if not existing_user:
        user = User(id=user_id, first_name=first_name, last_name=last_name, username=username)
        db.add(user)
        db.commit()
    
    db.close()

def set_user_state(user_id: int, state: str):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    
    if user:
        user.state = state
        db.commit()
    
    db.close()

def get_user_state(user_id: int) -> str | None:
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    return user.state if user else None

def get_user_language(user_id: int) -> str | None:
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()

    return user.language if user else None

def set_user_language(user_id: int, language: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if user:
            user.language = language 
            db.commit()
    finally:
        db.close()

def set_student_first_name(user_id: int, first_name: str):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.telegram_user_id == user_id).first()

        if student:
            student.first_name = first_name.strip()
        else:
            student = Student(
                first_name=first_name.strip(),
                telegram_user_id=user_id
            )
            db.add(student)

        db.commit()
    finally:
        db.close()

def set_student_last_name(user_id: int, last_name: str):
    try:
        db = SessionLocal()
        student = db.query(Student).filter(Student.telegram_user_id == user_id).first()
        
        if student:
            student.last_name = last_name.strip()
            db.commit()
    finally:
        db.close()

def set_student_age(user_id: int, age: int):
    try: 
        db =  SessionLocal()
        student = db.query(Student).filter(Student.telegram_user_id == user_id).first()

        if student: 
            student.age = age
            db.commit()
    finally:
        db.close()

def set_student_phone_number(user_id: int, phone_number: str):
    try: 
        db =  SessionLocal()
        student = db.query(Student).filter(Student.telegram_user_id == user_id).first()

        if student: 
            student.phone_number = phone_number
            db.commit()
    finally:
        db.close()

def set_student_address(user_id: int, address: str):
    try: 
        db =  SessionLocal()
        student = db.query(Student).filter(Student.telegram_user_id == user_id).first()

        if student: 
            student.address = address
            db.commit()
    finally:
        db.close()


def set_student_course(user_id: int, course: str):
    try: 
        db = SessionLocal()
        student = db.query(Student).filter(Student.telegram_user_id == user_id).first()

        if student:
            student.course = course
            db.commit()
    finally:
        db.close()

def set_student_level(user_id: int, level: str):
    try: 
        db = SessionLocal()
        student = db.query(Student).filter(Student.telegram_user_id == user_id).first()

        if student:
            student.level = level
            db.commit()
    finally:
        db.close()


def set_student_time(user_id: int, time: str):
    try: 
        db = SessionLocal()
        student = db.query(Student).filter(Student.telegram_user_id == user_id).first()

        if student:
            student.time = time
            db.commit()
    finally:
        db.close()
    