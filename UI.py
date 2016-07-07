import tkinter as tk
from insights import MyServer


class ServerUI(tk.Frame):
    server = None

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.server = MyServer(12345)
        self.pack()
        self.create_widgets()


    def create_widgets(self):
        print('ssadasdas')
        self.run_server = tk.Button(self)
        self.run_server["text"] = "RunServer"
        self.run_server["command"] = self.run_server
        self.run_server.pack(side="top")

        self.stop_server = tk.Button(self)
        self.stop_server["text"] = "StopServer"
        self.stop_server["command"] = self.stop_server
        self.stop_server.pack(side="bottom")


        self.QUIT = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.QUIT.pack(side="bottom")

    def run_server(self):
        print("Start")
        self.server.run()

    def stop_server(self):
        print("End")
        self.server.server_running_status = False


# root = tk.Tk()
# app = ServerUI(master=root)
# app.mainloop()
