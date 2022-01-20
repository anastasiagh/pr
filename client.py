from socket import AF_INET, socket, SOCK_STREAM
import threading
import tkinter
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import sys
import requests
import smtplib, ssl


def receive():
    # Handles receiving of messages
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf8")
            if "/send file:" in msg:
                command, filename = msg.split(':')
                print(filename)
                with open(filename, 'wb') as f:
                    print('file opened')
                    while True:
                        print('receiving data...')
                        data = client_socket.recv(1024)
                        print('data=%s', (data))
                        if not data:
                            break
                        # write data to a file
                        # f.write(data)
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    # Handles sending of messages
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def invite():
    top = tkinter.Tk()
    top.geometry("450x150")
    email_friend = tkinter.StringVar()  # For the messages to be sent.
    email_friend.set("")
    # Create an Entry Widget in the Toplevel window
    entry = tkinter.Entry(top, textvariable=email_friend)
    msg_friend = email_friend.get()
    print(msg_friend)
    email_friends.append(msg_friend)
    entry.bind("<Return>", send_invite)
    entry.pack()

    # Create a Button to print something in the Entry widget
    insert_button = tkinter.Button(top, text="Insert", command=send_invite).pack(pady=5)
    # Create a Button Widget in the Toplevel Window


def send_invite():
    receiver_email = "anastasia.gheo@gmail.com"
    print(receiver_email)
    # email_friends.pop()
    # print(email_friends)
    email_message = "Invite to try chat app"
    with smtplib.SMTP_SSL("smtp.gmail.com", EMAIL_PORT, context=ssl_context) as server:
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, receiver_email, email_message)


def on_closing(event=None):
    # This function is called when the window is closed.
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("Chat app")
email_friends = []
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=90, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()


def select_file():
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    files = {'file': open(filename, 'rb')}
    print(filename)
    print(files)
    getdata = requests.post(URL, files=files)
    print(getdata.text)


entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()
choose_file_button = tkinter.Button(top, text="Choose file", command=select_file)
choose_file_button.pack(pady=10)
invite_button = tkinter.Button(top, text="Invite friend", command=invite)
invite_button.pack(pady=10)

top.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == "__main__":
    # tcp
    client_socket = socket(AF_INET, SOCK_STREAM)
    EMAIL = 'testuniver08@gmail.com'  # your_email
    PASSWORD = 'bombonica'  # your_password
    EMAIL_PORT = 465
    # udp
    # client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client_socket.connect(('127.0.0.1', 8000))
    HTTP_PORT = 8004
    URL = 'http://127.0.0.1:' + str(HTTP_PORT)
    ssl_context = ssl.create_default_context()
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()
