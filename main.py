# Python
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import HTTPException, status
from fastapi import status
from fastapi import Body
from fastapi import Form
from fastapi import Path

app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(BaseModel):
    password: str = Form(
        ...,
        min_length=8,
        max_length=64
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):
    password: str = Form(
        ...,
        min_length=8,
        max_length=64
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

class LoginOut(BaseModel): 
    email: EmailStr = Field(...)
    message: str = Field(default="Login Successfully!")

"""
    # Auxiliar funcion 

    ## funcion read
    def read_data(file):
        with open("{}.json".format(file), "r+", encoding="utf-8") as f: 
            return json.loads(f.read())

    ## funcion write
    def read_data(file, results):
        with open("{}.json".format(file), "r+", encoding="utf-8") as f: 
            f.seek(0)
            f.write(json.dumps(results))
"""
# Path Operations
example_messagge="3fa85f64-5717-4562-b3fc-2c963f66afa6"

## Users
USER_PATH = "users.json"
description_user_id = "This is the user ID"
detail_user = "¡This user doesn't exist!"
### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(user: UserRegister = Body(...)):
    """
    SignUp

    This path operation register a user in the app

    Parameters:
        - Request body parameter
            - user: UserRegister

    Returns a json with the basic user information
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: str
    """

    with open(USER_PATH, "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results,indent=4, sort_keys=True))
        return user

### Login a user
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login(
    email: EmailStr = Form(...), 
    password: str = Form(...)
):
    """
    Login

    This path operation login a user in the app

    Parameters:
        - Request body parameter
            - email: EmailStr
            - password: str

    Returns a LoginOut model with username and message
    """

    with open(USER_PATH, "r", encoding="utf-8") as f:
        datos = json.loads(f.read())
        for user in datos:
            if email == user['email'] and password == user['password']:
                return LoginOut(email=email)
        return LoginOut(email=email, message="Login Unsuccessfully!")

### Show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all user",
    tags=["Users"]
)
def show_all_users():
    """
    Show All Users

    This path operation shows all users in the app

    Parameters:
        -

    Returns a json list with all users in the app, with the following keys
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: str
    """
    with open(USER_PATH, "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user(user_id: str = Path(
    ...,
    description=description_user_id,
    example=example_messagge
)):
    """
    Show a Users

    This path operation show a user in the app

    Parameters:
        - user_id: UUID

    Returns a json list with all users in the app, with the following keys
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: str
    """
    with open(USER_PATH, "r", encoding="utf-8") as f:
        datos = json.loads(f.read())
        for user in datos:
            if user_id == user['user_id']:
                return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail_user
        )

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user(user_id: str = Path(
    ...,
    description=description_user_id,
    example=example_messagge
)):
    """
    Delete a Users

    This path operation delete a user in the app

    Parameters:
        - user_id: UUID

    Returns a json list with all users in the app, with the following keys
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: str
    """
    with open(USER_PATH, "r+", encoding="utf-8") as f:
        datos = json.loads(f.read())
        for user in datos:
            if user_id == user['user_id']:
                datos.remove(user)
                with open(USER_PATH, "w", encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(datos, indent=4, sort_keys=True))
                return user
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail_user
        )

### Update a tweet
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user(
    user_id: str = Path(
        ...,
        description="This is the user ID",
        example=example_messagge
    ),
    user: UserRegister = Body(...)
):
    """
    Update a Users

    This path operation update a user in the app

    Parameters:
        - user_id: UUID

    Returns a json list with all users in the app, with the following keys
        - user_id: UUID
        - email: EmailStr
        - first_name: str
        - last_name: str
        - birth_date: str
    """
    with open(USER_PATH, 'r+', encoding="utf-8") as f:
        datos = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        for user in datos:
            if user["user_id"] == user_id:
                datos[datos.index(user)] = user_dict
                with open(USER_PATH, 'w', encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(datos, indent=4, sort_keys=True))
                return user 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail_user
        )

## Tweets
TWEETS_PATH = "tweets.json"
description_tw_id = "This is the tweet ID"
detail_tweet = "¡This tweet doesn't exist!"

### Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]

)
def home():
    """
    Home

    This path operation shows all tweets in the app

    Parameters:
        -

    Returns a json list with all tweets in the app, with the following keys
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    with open(TWEETS_PATH, "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
    Post a Tweet

    This path operation post a tweet in the app

    Parameters:
        - Request body parameter
            - tweet: Tweet

    Returns a json with the basic tweet information
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """

    with open(TWEETS_PATH, "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results, indent=4, sort_keys=True))
        return tweet

### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet(
    tweet_id: str = Path(
        ...,
        description=description_tw_id,
        example=example_messagge
)):
    """
    Show a Tweet

    This path operation show a tweet in the app

    Parameters:
        - Request body parameter
            - tweet_id: str 

    Returns a json with the basic tweet information
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    with open(TWEETS_PATH, "r+", encoding="utf-8") as f:
        datos = json.loads(f.read())
        for tweet in datos:
            if tweet["tweet_id"] == tweet_id:
                return tweet
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail_tweet
        )
    
### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet(
    tweet_id: str = Path(
        ...,
        description=description_tw_id,
        example=example_messagge
)):
    """
    Delete a Tweet

    This path operation delete a tweet in the app

    Parameters:
        - Request body parameter
            - tweet_id: UUID 

    Returns a json with the basic tweet information
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    with open(TWEETS_PATH, "r+", encoding="utf-8") as f:
        datos = json.loads(f.read())
        for tweet in datos:
            if tweet["tweet_id"] == tweet_id:
                datos.remove(tweet)
                with open(TWEETS_PATH, 'w', encoding="utf-8") as f:
                    f.seek(0)
                    f.write(json.dumps(datos, indent=4, sort_keys=True))
                return tweet
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail_tweet
        )
    

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet():
    pass
