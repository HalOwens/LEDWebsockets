import regex
import asyncio
import websockets

"""Server Constants"""
ip_s = "10.0.1.8"
port_s = 5678

# https://raspberrypi.stackexchange.com/questions/298/can-i-use-the-gpio-for-pulse-width-modulation-pwm


async def validate_string(str):
    """
    Takes argument str and verifies that it is of the form [[r1, g1, b1], [r2, g2, b2], [r3, g3, b3]]
    Returns true if the string is valid and false if invalid
    """
    str_r = regex.match(r'(\[?\[\d, \d, \d\],? ?\]?)', str)
    if str_r is None:
        return False
    else:
        return True


async def parse_string(str):
    """
    Takes a string of the form [[r1, g1, b1], [r2, g2, b2], [r3, g3, b3]] and stores r g b values in a 2-d array
    Returns the two dimensional array: [[r1, g1, b1],
                                        [r2, g2, b2],
                                        [r3, g3, b3]]
    """
    buf = str.replace(" ", "").replace("[", "").replace("]", "").split(",")
    buffer = [[0 for i in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            buffer[i][j] = int(buf[j + (3 * i)])
    return buffer


async def receive_data(websocket):
    """
    Called when a client is connected. Waits for a string to be transmitted
    Returns the transmitted data
    """
    print("New client connected")
    data = await websocket.recv()
    if await validate_string(data):
        data = await parse_string(data)
    return data


def update_led(rgb_values):
    """
    Changes the values of the PWM signals to the LEDs based off of the values in rgb_values
    Returns void
    """
    print("updating the LEDS with")
    print(rgb_values)


async def main(websocket, port):
    """
    Is called by the websocket handler when a client connects to the server
    Returns void
    """
    rgb_values = await asyncio.create_task(receive_data(websocket))
    update_led(rgb_values)


if __name__ == '__main__':
    """
    Establishes the websocket server at ws://ip:port and creates the asyncio event loop
    """
    server = websockets.serve(main, ip_s, port_s)
    print("Server established at ws://{}:{}".format(ip_s, port_s))
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()