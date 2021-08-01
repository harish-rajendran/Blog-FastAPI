from fastapi import FastAPI,Depends,status,Response,HTTPException,APIRouter
from  .. import models,schema,database,oauth2
from fastapi.security import OAuth2PasswordRequestForm
from ..database import engine,SessionLocal
from sqlalchemy.orm import Session, session
from typing import List


router = APIRouter(
    prefix='/blog',
    tags=['blogs']
)
get_db = database.get_db


@router.post('/',status_code=status.HTTP_201_CREATED)
def  create(request:schema.Blog,db:Session= Depends(get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    new_blog =  models.Blog(title=request.title,body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return request


@router.get('/',response_model=List[schema.Showblog])
def fetch(current_user: schema.User = Depends(oauth2.get_current_user),db:Session= Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get('/{id}',response_model=schema.Showblog)
def fetch_id(id,db:Session= Depends(get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    fetch_one = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not fetch_one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The requested id '{id}' was not found")
    return fetch_one


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db:Session=Depends(get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    blog_check = db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    if not blog_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"The blog id you mentioned({id}) does not exist please try again")
    db.commit()
    return f"Deleted blog id {id} succesfully"


@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schema.Blog,db:Session=Depends(get_db),current_user: schema.User = Depends(oauth2.get_current_user)):
    blog_check = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog_check.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"The blog id you mentioned({id}) does not exist please try again")
    blog_check.update(request)
    db.commit()
    return f"Blog id {id} updated successfully"