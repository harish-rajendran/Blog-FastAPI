from blog.hashing import Hash
from fastapi import FastAPI,Depends,status,Response,HTTPException,APIRouter
from ..database import engine,SessionLocal
from .. import models, hashing, schema,database
from ..hashing import Hash
from sqlalchemy.orm import Session, session
from typing import List


router =APIRouter(
    prefix='/user',
    tags=['Users']
)

get_db = database.get_db


@router.post('/',response_model=schema.Showuser)
def create_user(request:schema.User,db:Session=Depends(get_db),status_code=status.HTTP_201_CREATED):
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}',response_model=schema.Showuser)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id '{id}' is not available")
    return user