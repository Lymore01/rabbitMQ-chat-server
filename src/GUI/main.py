import tkinter as tk
from PIL import Image, ImageTk

# Initialize the main window
root = tk.Tk()
root.title("Chat App")
root.geometry("360x500")
root.configure(bg='#f6faf3')


image = Image.open("images/message.png")
image = image.resize((220, 110))
photo = ImageTk.PhotoImage(image)


image_frame = tk.Frame(root, bg="#f6faf3", width=360, height=150)
text_frame = tk.Frame(root, bg="#f6faf3", width=360, height=250)

image_frame.pack(side="top", fill="both", expand=True)
text_frame.pack(side="bottom", fill="both", expand=True)


background_image = tk.Label(image_frame, image=photo, bg="#f6faf3")
background_image.place(relx=0.5, rely=0.5, anchor="center")


label = tk.Label(text_frame, text="Let's chat!", fg='#1a2c32', bg='#f6faf3', font=("Poppins", 20))
label.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

button = tk.Button(text_frame, text="Create room", bg='#13250e', fg='white', font=('Poppins', 12))
button.grid(row=1, column=0, pady=10, padx=10, sticky="ew")


text_frame.grid_rowconfigure(0, weight=1)
text_frame.grid_rowconfigure(1, weight=1)
text_frame.grid_columnconfigure(0, weight=1)


root.mainloop()
