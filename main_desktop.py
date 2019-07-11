from tkinter import *
from tkinter import ttk, StringVar
import asyncio
import websockets

root = Tk()


class EmptyFieldError(Exception):
    """Raised when a field is empty in the UI"""
    pass


class Desktop():
    def __init__(self):
        """Server Constants"""
        self.ip = "10.30.21.64"
        self.port = 5678

        """Tkinter vars"""
        self.status = StringVar()
        self.tx_string = ""

        """Holds the values of each entry box"""
        self.data = [[0 for i in range(3)] for i in range(3)]
        self.input1 = StringVar()
        self.input2 = StringVar()
        self.input3 = StringVar()
        self.input4 = StringVar()
        self.input5 = StringVar()
        self.input6 = StringVar()
        self.input7 = StringVar()
        self.input8 = StringVar()
        self.input9 = StringVar()

        """Holds references to the entry box widgets"""
        self.data_entry = [[0 for i in range(3)] for i in range(3)]

    def bind_data(self):
        self.data[0][0] = self.input1
        self.data[0][1] = self.input2
        self.data[0][2] = self.input3
        self.data[1][0] = self.input4
        self.data[1][1] = self.input5
        self.data[1][2] = self.input6
        self.data[2][0] = self.input7
        self.data[2][1] = self.input8
        self.data[2][2] = self.input9

    def send(self, *args):
        """
        Function that is called when the send button is pressed, exist to asynchronously call other functions
        Returns void
        """
        try:
            buffer = asyncio.run(self.build_string())
            asyncio.run(self.send_data(buffer))
        except EmptyFieldError:
            self.status.set("ERROR: Populate all fields with numbers")

    def initializeGUI(self):
        """Add title and EXB Logo to top bar"""
        root.title("LED Manager")
        root.iconbitmap('exbICO.ico')

        """Establishes basic formatting for the TKinter frame"""
        mainframe = ttk.Frame(root, padding=".3i")
        mainframe.grid(column=0, row=0)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        """Creates ttk Entry widgets that feed into values of data[][] and the places them into the frame"""
        self.data_entry[0][0] = ttk.Entry(mainframe, width=7, textvariable=self.input1)
        self.data_entry[0][1] = ttk.Entry(mainframe, width=7, textvariable=self.input2)
        self.data_entry[0][2] = ttk.Entry(mainframe, width=7, textvariable=self.input3)
        self.data_entry[1][0] = ttk.Entry(mainframe, width=7, textvariable=self.input4)
        self.data_entry[1][1] = ttk.Entry(mainframe, width=7, textvariable=self.input5)
        self.data_entry[1][2] = ttk.Entry(mainframe, width=7, textvariable=self.input6)
        self.data_entry[2][0] = ttk.Entry(mainframe, width=7, textvariable=self.input7)
        self.data_entry[2][1] = ttk.Entry(mainframe, width=7, textvariable=self.input8)
        self.data_entry[2][2] = ttk.Entry(mainframe, width=7, textvariable=self.input9)
        for i in range(3):
            for j in range(3):
                self.data_entry[i][j].grid(column=i + 1, row=j + 2)
                self.data_entry[i][j].focus()

        """ Creates the labels on all entry boxes and buttons"""
        ttk.Label(mainframe, textvariable=self.status).grid(column=4, row=2)
        ttk.Label(mainframe, text="Red 0-255").grid(column=0, row=2)
        ttk.Label(mainframe, text="Green 0-255").grid(column=0, row=3)
        ttk.Label(mainframe, text="Blue 0-255").grid(column=0, row=4)
        ttk.Label(mainframe, text="LED #1").grid(column=1, row=1)
        ttk.Label(mainframe, text="LED #2").grid(column=2, row=1)
        ttk.Label(mainframe, text="LED #3").grid(column=3, row=1)
        ttk.Button(mainframe, text="Send", command=self.send).grid(column=4, row=3)
        root.bind('<Return>', self.send)

        """Draw TKinter Frame"""
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

    async def set_status(self, str):
        """
        Takes the argument str and adds it to the GUI above the send button then returns void
        """
        self.status.set(str)
        root.update()
        await asyncio.sleep(.8)

    async def build_string(self):
        """
        Maps the values of the StringVar()s inside of Data to integer data
            if a value is > 255 it is set to 255
            if a value is < 0 it is set to 0
        Returns buffer if all data fields are full else it raises an EmptyFieldError exception"
        """
        self.bind_data()
        buffer = [[0 for i in range(3)] for i in range (3)]
        try:
            for i in range(3):
                for j in range(3):
                    val = int(self.data[i][j].get())
                    if 0 <= val <= 255:
                        buffer[i][j] = val
                    elif val >= 256:
                        buffer[i][j] = 255
                    else:
                        buffer[i][j] = 0
            self.tx_string = str(buffer)
            return buffer
        except ValueError:
            raise EmptyFieldError

    async def send_data(self, buffer):
        """
        Takes the argument buffer, connects to the server ws://ip:port and sends buffer as a string
        Returns true if data is successfully transmitted false if transmission fails for any reason
        """
        await self.set_status("Connecting...")
        try:
            async with websockets.client.connect("ws://{}:{}".format(self.ip, self.port)) as websocket:
                await self.set_status("Connected")
                await self.set_status("Transmitting Values")
                print("Connection at ws://{}:{} established".format(self.ip, self.port))
                print("Transmitting RGB values")
                print(self.tx_string)
                await websocket.send(self.tx_string)
                await self.set_status("Data Transmitted ✓")
                print("Closing connection at ws://{}:{}".format(self.ip, self.port))
                websocket.close()
                return True
        except ConnectionRefusedError:
            await self.set_status("Unable to Connect")
            print("Unable to connect to server at w://{}:{}".format(self.ip, self.port))
            return False
        except OSError:
            await self.set_status("Unable to Connect")
            print("OSError Thrown")
            return False


if __name__ == '__main__':
    client = Desktop()
    client.initializeGUI()
    """Main Loop"""
    while True:
        try:
            root.update_idletasks()
            root.update()
        except TclError:
            sys.exit(0)