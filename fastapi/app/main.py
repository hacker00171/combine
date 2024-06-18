import time
from typing import Optional
import typing
from fastapi import Body, Depends, FastAPI, HTTPException, Response,status
# import fastapi as fp
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import session
from .database import engine, get_db
from . import models


models.Base.metadata.create_all(bind=engine)
# it is used to create the table in database


app=FastAPI()

class book_details(BaseModel):
    tittle_book:str
    author:str
    published: bool=True


class user_details(BaseModel):
    name:str
    email:str
    password:str





#sqlalchemy query
@app.get("/post")
def get_post(db:session= Depends(get_db)):
   post= db.query(models.post).all()
   return{"data":post}    



@app.get("/user")
def user(db:session= Depends(get_db)):
    user=db.query(models.User).all()
    return{"data":user}


#sql alchemy to enter the new post into the query
@app.post("/create",status_code=status.HTTP_201_CREATED)
def create_post(new_book_details:book_details,db:session=Depends(get_db)):
    # post_dict=new_book_details.dict()
    # post_dict["id"]=3
    # post.append(post_dict)
#    post_dict= models.post(tittle_book=new_book_details.tittle_book, 
#                           author=new_book_details.author,
#                           published=new_book_details.published)
   post_dict=models.post(**new_book_details.dict())
   print(post_dict)
   db.add(post_dict)
   db.commit()
   db.refresh(post_dict)
   return{"message":post_dict}


#sqlalchemy for user
@app.post("/user/create")
def user_create(details:user_details,db:session=Depends(get_db)):
    post_dict=models.User(**details.dict())
    if post_dict==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no details")
    db.add(post_dict)
    db.commit()
    db.refresh(post_dict)
    return{"data":post_dict}



@app.get("/post/{id}")
def get_post(id:int, db:session=Depends(get_db)):
   post= db.query(models.post).filter(models.post.id==id).first()
   print(post)



#sql alchmey
@app.get("/{id}")
def get_post(id:int,db:session=Depends(get_db)):
    index= db.query(models.post).filter(models.post.id==id).first()
    print(index)

    
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"details is not found in {id}")
    

    return{"data":index }



# @app.get("/{id}")
# def get_post(id:int,):
    
#     index=find_post(id)
    
#     if index==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"details is not found in {id}")
    
#     return{"data":index }



@app.put("/post/{id}")
def update(id:int,update_post:book_details, db:session=Depends(get_db)):
    post=db.query(models.post).filter(models.post.id==id)
    post1=post.first()
    if post1 == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"not found in the database {id}")
    post.update(update_post.dict())
    db.commit()
    return{"data":post}



#sql alchemy query
@app.put("/post/{id}")
def put_post(id:int, db:session=Depends(get_db)):
    post=db.query(models.post).filter(models.post.id==id)

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            details=f"not found in the database {id}")
    post.delete(synchronize_session=False)
    db.commit()
    return{"data":post}







# while True:
#     try:
#         conn=psycopg2.connect(host='localhost',database='fastapi',
#                             user='postgres',password='1234',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         break
#     except Exception as error:
#         print("connection failed")
#         print("error",error)
#         time.sleep(2)
       


# book=[{"id":1, "tittle_book":"java","author":"srini" },
#        {"id":2, "tittle_book":"python", "author":"saravanan"},
#        {"id":3, "tittle_book":"c#", "author":"santhosh"},
#        {"id":4, "tittle_book":"SQL", "author":"dinesh"}]


# def find_post(id):
#     for p in book:
#         if p["id"]==id:
#             return p
        

# def delete_post(id):
#     for i,p in enumerate(book):
#         if p['id']==id:
#             return i


# # GET method is used to get the data using api
# @app.get("/") # it is a dector that make the below function into api
# def root():
#     return{"message":"Hello , Every one we welcome our company"}


# @app.get("/post")
# def post():
#    return{"data":book}



# @app.put("/{id}")
# def update(id:int,post:book_details):
#     index=delete_post(id)
#     if index==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"There is no data in this id{id}")
#     post_dict=post.dict()
#     post_dict['id']=id
#     book[index]=post_dict
#     return{"data":post_dict}






# @app.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id:int):
#     n_del=delete_post(id)
#     book.pop(id)
#     if n_del ==None:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
#                             detail=f'data delete in this id :{id}')
#     return Response(status_code=status.HTTP_404_NOT_FOUND)


# @app.get("/")
# def query_par()



#POST method is used to send the data to api

# @app.post("/create")
# def create_post(payload:dict=Body(...)):
#     print(payload)
#     return {"message":"successfully created"}
#     return{"newpost":f"title:{payload['tittle_book']} ,author: {payload['author']}"}


