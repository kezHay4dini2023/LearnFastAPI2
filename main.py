from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")  # decorater (this turns into a path operation) @ clarifies its gonna be a decorator. .get is an http method

# .get() - Method
# ("/login") - path
# root(): - Function 
async def root():
    return {"message": "Hello World!!! ;)"}



#retrieving method.
@app.get("/posts")
def get_post():
    return {"data": "This is your posts"}


@app.post("/createposts")
def createPosts(payLoad: dict = Body(...)):
    print(payLoad)
    return {"message": "successfully created posts"}