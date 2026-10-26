from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str 
    published: bool = True
    rating: Optional[int] = None


my_posts = [{
    "title": "title of post 1",
    "content": "conent of post 1",
    "id": 4001
},
    {
    "title": "favorite foods",
    "content": "i like pizza",
    "id": 2001 
    }
]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")  # decorater (this turns into a path operation) @ clarifies its gonna be a decorator. .get is an http method

# .get() - Method
# ("/login") - path
# root(): - Function 
async def root():
    return {"message": "Hello World!!! ;)"}


# READ
#retrieving method.
@app.get("/posts")
def get_post():
    return {"data": my_posts}


# @app.post("/createposts")
# def createPosts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_post": f"title: {payLoad["title"]}, content: {payLoad["content"]}"}

# title string, content string, category, Bool published

# @app.post("/posts")
# def createPosts(post: Post):
#     print(post)
#     print(post.dict())
#     return {"data": post}

# CREATE
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def createPosts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return{"detail": post}

# READ 

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found. sorry bb :("
                            )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    return {"post_detail": post}

# DELETE

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # delete post
    # find the index in the array that has required ID
    # my_posts.pop(index)

    index = find_index_post(id)
    if index == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    index = find_index_post(id)
    if index == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    
    return{
        "data" : post_dict
    }
