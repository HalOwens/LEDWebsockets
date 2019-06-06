from tkinter import *
from tkinter import ttk, StringVar
import asyncio
import websockets

"""Raised when a field is empty in the UI"""
class EmptyFieldError(Exception):
    pass


"""Server Constants"""
ip = "10.30.128.92"
port = 5678

"""Tkinter vars"""
root = Tk()
status = StringVar()


async def set_status(str):
    """
    Replaces the multiple calls to this code pattern which was used to update
        the status indicator text in the UI
    Returns void
    """
    status.set(str)
    root.update()
    await asyncio.sleep(.8)


async def create_buffer():
    """
    Maps the values of the StringVar()s inside of Data to integer data
        if a value is > 255 it is set to 255
        if a value is < 0 it is set to 0
    Returns buffer if all data fields are full else it raises an EmptyFieldError exception"
    """
    buffer = [[0 for i in range(3)] for i in range (3)]
    try:
        for i in range(3):
            for j in range(3):
                val = int(data[i][j].get())
                if 0 < val < 255:
                    buffer[i][j] = val
                elif val >= 256:
                    buffer[i][j] = 255
                else:
                    buffer[i][j] = 0
        return buffer
    except ValueError:
        raise EmptyFieldError



async def send_data(buffer):
    """
    Connects to the server ws://ip:port and transmits buffer as a str
    Returns true if data is successfully transmitted false if transmission fails for any reason
    """
    await set_status("Connecting...")
    try:
        async with websockets.client.connect("ws://{}:{}".format(ip, port)) as websocket:
            await set_status("Connected")
            await set_status("Transmitting Values")
            print("Connection at ws://{}:{} established".format(ip, port))
            print("Transmitting RGB values")
            await websocket.send(str(buffer))
            await set_status("Data Transmitted ✓")
            print("Closing connection at ws://{}:{}".format(ip, port))
            websocket.close()
            return True
    except ConnectionRefusedError:
        await set_status("Unable to Connect")
        print("Unable to connect to server at w://{}:{}".format(ip, port))
        return False


def send(*args):
    """
    Function that is bound to the <send> button needed because a button cannot be bound
        to and asynchronous function
    Returns void
    """
    try:
        buffer = asyncio.run(create_buffer())
        asyncio.run(send_data(buffer))
    except EmptyFieldError:
        status.set("ERROR: Populate all fields with numbers")


if __name__ == '__main__':
    root.title("LED Manager")
    root.iconbitmap('exbICO.ico')

    mainframe = ttk.Frame(root, padding=".3i")
    mainframe.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    """Holds the values of each entry box"""
    data = [[StringVar() for i in range(3)] for i in range(3)]

    """Holds references to the entry box widgets"""
    data_entry = [[0 for i in range(3)] for i in range (3)]

    """Creates ttk Entry widgets that feed into values of data[][] and the places them into the frame"""
    for i in range(3):
        for j in range(3):
            data_entry[i][j] = ttk.Entry(mainframe, width=7, textvariable=data[i][j])
            data_entry[i][j].grid(column=i+1, row=j+2)
            data_entry[i][j].focus()

    """ Creates the labels on all entry boxes and buttons"""
    ttk.Label(mainframe, textvariable=status).grid(column=4, row=2)
    ttk.Label(mainframe, text="Red 0-255").grid(column=0, row=2)
    ttk.Label(mainframe, text="Green 0-255").grid(column=0, row=3)
    ttk.Label(mainframe, text="Blue 0-255").grid(column=0, row=4)
    ttk.Label(mainframe, text="LED #1").grid(column=1, row=1)
    ttk.Label(mainframe, text="LED #2").grid(column=2, row=1)
    ttk.Label(mainframe, text="LED #3").grid(column=3, row=1)
    ttk.Button(mainframe, text="Send", command=send).grid(column=4, row=3)
    root.bind('<Return>', send)

    """Draw TKinter Frame"""
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)


    """Main Loop"""
    while True:
        try:
            root.update_idletasks()
            root.update()
        except TclError:
            sys.exit(0)