import pika
import sys
import threading
from room_manager import create_room

class ChatRoom:
    def __init__(self, username, room_name, room_type):
        self.room_name = room_name
        self.username = username
        self.room_type = room_type  # direct (for private messages), fanout(for public messages eg. groups)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.exchange_name = room_name
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.room_type)
        
        # Set up consumers
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name, routing_key=self.room_name)
    
    def publish_message(self, message):
        self.channel.basic_publish(exchange=self.exchange_name, routing_key=self.room_name, body=message)
        print(f" [x] Sent message {message} to room: {self.room_name}")
    
    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        print(f" [*] Waiting for messages in room {self.room_name}")
        self.channel.start_consuming()
        
    def callback(self, ch, method, properties, body):
        sys.stdout.write("\033[K")
        print(f'\r [x] Received: {body.decode()}')
        sys.stdout.write(f"{self.username}> ")
        sys.stdout.flush()
        
    def close(self):
        self.connection.close()
    
if __name__ == "__main__":
    room_name = input("Enter room name: ")
    room_type = input("Enter room type: ")
    username = input("Enter a username: ")
    
    chat_room = create_room(username, room_name, room_type)
    
    # Start the consumer thread
    if isinstance(chat_room, str):
        print(chat_room)
        sys.exit(0)
    else:
        chat_rooms = ChatRoom(chat_room[0], chat_room[1], chat_room[2])
        print("Room created")
        cons_thread = threading.Thread(target=chat_rooms.start_consuming)
        cons_thread.start()

    # Run the input loop in the main thread
    try:
        while True:
            msg = input(f"{username}> ")
            chat_rooms.publish_message(msg)
    except KeyboardInterrupt:
        print("Interrupted")
        chat_rooms.close()
        cons_thread.join()
        sys.exit(0)
