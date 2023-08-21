from typing import Union
from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
import time
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool =True


# configuring the postgre database
while True:
    try:
        connection = psycopg2.connect(
            database='fastapi',
            user='postgres',
            password='postgres',
            host='localhost',
            port=5432,
            cursor_factory=RealDictCursor
        )
        cursor = connection.cursor()
        print("database connection is established")
        break
    except Exception as error:
        print({'error': error})
        time.sleep(3)


@app.get('/')
def home():
    return {'message': 'Welcome'}

my_posts= [{'title': "Hello", 'content':'This is conent', 'id':1},{'title': "FastAPi", 'content':'This is fastapi', 'id':2}]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

# def find_index(id):
#     for index,post in enumerate(my_posts):
#         if post['id'] == id:
#             return index

# @app.get('/posts')
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")
#     all_posts = cursor.fetchall()
#     print("all_post", all_posts)
#     return {"data": all_posts}


@app.post('/posts',status_code=201)
def create_post(post: Post):
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """,(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    connection.commit()
    return {"message":" Created post successfully", "post": new_post}


@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    cursor.execute("""  SELECT * FROM posts WHERE id=%s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id was {id} not found")
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {"message": f"Post with id {id} was not found"}
    return {"post": post}

@app.delete('/posts/{id}')
def delete_post(id: int):
    cursor.execute("""  DELETE FROM posts WHERE id = %s returning * """, str((id),))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id was {id} not found")
    connection.commit()
    return {"message": f"Post with id {id} has been deleted successfully", "deleted_post": deleted_post}

@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *""",(post.title, post.content, post.published, str((id))))
    updated_post = cursor.fetchone()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    connection.commit()
    return {"message": "Post updated successfully", "updated_post": updated_post}
    