import sys
from database.models import Room, session

def create_room(username, room_name, room_type):
    try:
        rooms = session.query(Room).all()
        
        for room in rooms:
            if room.name == room_name:
                return "Room already exists!"
        
        chat_room = (username, room_name, room_type)
        new_room = Room(name=room_name, type=room_type)
        session.add(new_room)
        session.commit()
        return chat_room
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
        
    
