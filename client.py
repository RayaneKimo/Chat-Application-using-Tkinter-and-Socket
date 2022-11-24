import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

IP = "127.0.0.1"
PORT = 1234

class Client:
    def __init__(self, host, port):

        self.sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk() # window
        msg.geometry("300x400")
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Choisir un pseudo :", parent=msg)
        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()


    def gui_loop(self): #to build the front end
      self.window = tkinter.Tk()
      self.window.configure(bg = "lightgray")
      self.chat_label= tkinter.Label(self.window, text="Chat : ", bg='yellow')
      self.chat_label.config(font=("Arial", 12))
      self.chat_label.pack(padx=20, pady=5)

      self.text_area= tkinter.scrolledtext.ScrolledText(self.window)
      self.text_area.pack(padx=20, pady=5)
      self.text_area.config(state='disabled') # Disabled to not change the content or Making the text read only

      self.msg_label = tkinter.Label(self.window, text = "Chat Box : ", bg='yellow')
      self.msg_label.config(font=("Arial", 12))
      self.msg_label.pack(padx=20, pady=5)

      self.input_area= tkinter.Text(self.window, height=3)
      self.input_area.pack(padx=20, pady=5)

      self.send_button=tkinter.Button(self.window, text="Send", command=self.write)
      self.send_button.config(font=("Arial", 12))
      self.send_button.pack(padx=20, pady=5)

      self.gui_done = True
      self.window.protocol("WM_DELETE_WINDOW", self.stop) # we call the window protocol to close the window and stop the programm
      self.window.mainloop()

    def stop(self):
      self.running = False  #we stop the running
      self.window.destroy() #we destroy the window
      self.sock.close()  #we close the socket
      exit(0)


    def write(self):
         message= f"{self.nickname} : {self.input_area.get('1.0', 'end')}"  # 1.0 and end : mean to get the message from the beginning till the end
         self.sock.send(message.encode("utf-8"))
         self.input_area.delete('1.0', 'end') #when we send the message upon the socket we delete the input area from the start till the end


    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode("utf-8")
                if message == "PSEUDO":
                    self.sock.send(self.nickname.encode("utf-8"))

                else:
                    if self.gui_done:
                        self.text_area.config(state="normal") # at this state we can change , insert some text received then it will be disabeled
                        self.text_area.insert('end', message)
                        self.text_area.yview('end') #we scroll with adding messages to show the end of the conversation
                        self.text_area.config(state="disabled") #Making the text read only


            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break





client= Client(IP, PORT)