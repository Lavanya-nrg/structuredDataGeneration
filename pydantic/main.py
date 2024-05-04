import uuid
from datetime import datetime, timedelta
import pandas as pd
from pydantic import BaseModel, confloat, validator
from enums import DepartmentEnum
from faker import Faker
import random

fake = Faker()

class Student(BaseModel):
    id: uuid.UUID
    name: str
    date_of_birth: datetime
    GPA: confloat(ge=0, le=4)
    course: str | None
    department: DepartmentEnum
    fees_paid: bool

    @validator('date_of_birth')
    def ensure_16_or_over(cls, value):
        sixteen_years_ago = datetime.now() - timedelta(days=365 * 16)
        if value > sixteen_years_ago:
            raise ValueError('Date of Birth must be 16 or over')
        return value

def enum_to_string(department: DepartmentEnum) -> str:
    return department.value.replace("_", " ").title()

synthetic_data = []
for _ in range(10): 
    synthetic_student = Student(
        id=uuid.uuid4(),
        name=fake.name(), 
        date_of_birth=datetime.now() - timedelta(days=random.randint(16 * 365, 25 * 365)),
        GPA=random.uniform(0, 4),
        course=None,
        department=random.choice(list(DepartmentEnum)),
        fees_paid=random.choice([True, False])
    )
    synthetic_data.append(synthetic_student)

data_dict = [student.dict() for student in synthetic_data]
for entry in data_dict:
    entry['department'] = enum_to_string(entry['department'])  
df = pd.DataFrame(data_dict)

df.to_csv('synthetic_students.csv', index=False)

print("DataFrame saved to synthetic_students.csv")