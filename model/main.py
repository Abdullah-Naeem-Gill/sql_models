from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Task(SQLModel, table=True):  
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)

sqlite_url = f"postgresql://model_owner:fo4YjeSyOMP6@ep-proud-morning-a5aqk95t.us-east-2.aws.neon.tech/model?sslmode=require"
engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")  
def on_startup():
    create_db_and_tables()  

@app.post("/task/")
def create_task(task: Task):  
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.get("/tasks/") 
def read_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()  
        return tasks
