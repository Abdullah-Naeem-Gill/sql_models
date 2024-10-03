from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager


class task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
  



sqlite_url = f"postgresql://model_owner:fo4YjeSyOMP6@ep-proud-morning-a5aqk95t.us-east-2.aws.neon.tech/model?sslmode=require"


engine = create_engine(sqlite_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    create_db_and_tables()
    yield
   


app:FastAPI = FastAPI(lifespan=lifespan)



@app.post("/task/")
def create_task(task: task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


@app.get("/heroes/")
def read_tasks():
    with Session(engine) as session:
        tasks = session.exec(select(task)).all()
        return tasks