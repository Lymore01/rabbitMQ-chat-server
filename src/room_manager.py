import sys
from src.database.models import Room, session
from sqlalchemy.exc import SQLAlchemyError


def create_chat_room(room_name, room_type, room_url):
    try:
       
        existing_room = session.query(Room).filter_by(name=room_name).first()
        if existing_room:
            return "Room already exists!"
        new_room = Room(name=room_name, type=room_type, url=room_url)
        session.add(new_room)
        session.commit()

        return room_name, room_type, room_url
    except SQLAlchemyError as e:
        session.rollback() 
        return f"Error creating room: {e}"
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
    finally:
        session.close()
        
    
