from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas

Base.metadata.create_all(engine) #create the database

#Initialize app
app = FastAPI()

def get_session():
    session=SessionLocal()
    try:   
        yield session

    finally:
        session.close()
 
@app.get("/")
def root():
    return "Hello World!"
 
@app.post("/todo", response_model=schemas.ToDo,status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoCreate, session: Session = Depends(get_session)):

    tododb=models.ToDo(task = todo.task)

    session.add(tododb)
    session.commit()
    session.refresh(tododb)

    return tododb
 
@app.get("/todo/{id}", response_model=schemas.ToDo)
def read_todo(id: int, session: Session = Depends(get_session)):
    todo = session.query(models.ToDo).get(id) # get item with the given id
    # check if id exists. If not, return 404 error not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")
    
    return todo
 
@app.put("/todo/{id}", response_model=schemas.ToDo)
def update_todo(id: int, task:str, session: Session = Depends(get_session)):

    todo = session.query(models.ToDo).get(id) # get given id
    if todo:
        todo.task=task
        session.commit()

    # check if id exists. If not, return 404 error not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")
    
    return todo
 
@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, session: Session = Depends(get_session)):
    todo = session.query(models.ToDo).get(id) # get given id
    if todo:
        session.delete(todo)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")
    
    return None
 
@app.get("/todo", response_model = List[schemas.ToDo])
def read_todo_list(session: Session = Depends(get_session)):

    todo_list = session.query(models.ToDo).all() # get all todo items
    return todo_list