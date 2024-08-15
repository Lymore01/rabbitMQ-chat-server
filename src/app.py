from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os
from src.server.server import ChatRoom
from src.room_manager import create_chat_room
import random
import threading
import sys

db_path = os.path.join(os.path.dirname(__file__), "sqlite.db")
def fetch_from_db(query, params=None):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return cursor.fetchall()
    except Exception as e:
        return f"Error: {e}"
    finally:
        connection.close()

class Room(BaseModel):
    room_name: str
    room_type: str | None = 'direct'
    room_url: str

class User(BaseModel):
    username: str
    room_url:str
    
    
app = FastAPI()


@app.get("/")
def hello():
    return fetch_from_db("SELECT * FROM members")

@app.post("/create-room")
def create_room(room: Room):
    try:     
        chat_room = create_chat_room(room.room_name, room.room_type, room.room_url)#tuple ('room1', 'direct')
        if chat_room:
            print("created")     
            add_chat_room = ChatRoom(chat_room[0], chat_room[1], chat_room[2])
            
            return {
                'message':"Room created successfully!",
                'details':add_chat_room.display_room()
            }
        else:
            return "No chat room"
    except Exception as e:
        return {
            'message':"Error creating room",
            'details':e
        }
        
@app.post("/join-room")
def join_room(user: User):
    try:
        room = fetch_from_db("SELECT * FROM rooms WHERE url = ?", (user.room_url,))
        if not room:
            return "Room does not exist"

        if not user.username:
            user.username = f"user{random.randint(0, 999)}"
        else:
            user.username += f'{random.randint(1000, 9999)}'

        # using ? in the values prevent sql injection
        fetch_from_db(
            "INSERT INTO members (name, room_id) VALUES (?, ?)",
            (user.username, user.room_url)
        )
        
        room_name = room[0][1]
        
        
        return {
            'message': f"User '{user.username}' joined room {room_name} successfully."
        }
       
    except Exception as e:
        return {
            'message': "Error joining room",
            'details': str(e)
        }

@app.post("/send")
def start_chat(room_name, room_type, room_url, message):
    try:
        chat_room = ChatRoom(room_name, room_type, room_url)
        
        if isinstance(chat_room, str):
            sys.exit(0)
        else:
            cons_thread = threading.Thread(target=chat_room.start_consuming)
            cons_thread.start()

        # Run the input loop in the main thread
        try:
            while True:
                chat_room.publish_message(message)
        except KeyboardInterrupt:
            chat_room.close()
            cons_thread.join()
            sys.exit(0)
    except:
            pass

@app.get("/messages")
def get_messages():
    pass

@app.get("/rooms")
def get_rooms(id: str = "all"):
    if id == 'all':
        return fetch_from_db("SELECT * FROM rooms")
    else:
       return fetch_from_db(f"SELECT * FROM rooms WHERE id = ?", (id,))