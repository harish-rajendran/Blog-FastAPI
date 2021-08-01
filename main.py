from  fastapi import FastAPI
from  typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get('/blog')
def index(limit:int = 10,published:bool=True,sort: Optional[str]=None):
    if published:
        return {"data":f"{limit} published blogs from the db"}
    else:
        return {"data":f"{limit} blogs from the db"}


@app.get('/blog/unpublished')
def unpublished():
    return {'data':'all unpublished blogs'}


@app.get('/blog/{id}')
def about(id:int):
    #fetch  blog with id
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id,limit=10):
    #fetch comments based on id
    return {'data':{'1','2','3'}}


class Blog(BaseModel):
    title: str
    body: str
    published_at : Optional[bool]= False


@app.post('/blog')
def create_blog(request: Blog):
    return{"messsage":f"blog created with title '{request.title}'"}
    

@app.post("/dummypath/")
async def get_body(req: dict):
    return req