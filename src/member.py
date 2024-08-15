import threading
from src.server.server import ChatRoom
import sys
from database.models import Room,Member,session

class ChatMembers:
    def __init__(self, username, room_name, room_type):
        self.username = username
        self.room_name = room_name
        self.room_type = room_type
        self.chat_room = ChatRoom(self.username,self.room_name, self.room_type)
    
    def join_room(self):
        print(f"Joined room {self.room_name} successfully")
        cons_thread = threading.Thread(target=self.start_consuming)
        cons_thread.start()
        while True:
            self.start_chat()
            
    
    def start_chat(self):
        message = input(f"{self.username}> ")
        self.chat_room.publish_message(message)
        
    def start_consuming(self):
        self.chat_room.start_consuming()
        
    def close(self):
        self.chat_room.close()

if __name__ == "__main__":
    try:
        username = input("Enter your username: ")
        room_name = input("Enter room name: ")
        room_type = input("Enter room type: ")
        
        
        rooms = session.query(Room).all()
 
        room_exists = any(room.name == room_name for room in rooms)
        
        
        if not room_exists:
            print("Incorrect room name!")
            sys.exit(0)

        chat_member = ChatMembers(username, room_name, room_type)
        chat_member.join_room()
        
               
    except KeyboardInterrupt:
        print("Interrupted")
        chat_member.close()
        sys.exit(0)
