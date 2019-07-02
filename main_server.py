import regex
import asyncio
import websockets
import wiringpi



"""Server Constants"""
ip_s = "192.168.192.239"
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


def update_led(led_pins, rgb_values):
    """
    Changes the values of the PWM signals to the LEDs based off of the values in rgb_values
    Returns void
    """
    for i in range(3):
        setColor(led_pins[i], rgb_values[i])
    print("updating the LEDS with")
    print(rgb_values)


def setColor(pins, rgb):
    """
    Takes two arguments: pins and rgb. Pins contains the three pins connected to a specific led and
    rgb contains the three color values for that LED
    Returns void
    """
    for pinToWrite in pins:
        wiringpi.pinMode(pinToWrite, 1)
        wiringpi.softPwmCreate(pinToWrite, 0 , 255 )
        for color in rgb:
            wiringpi.softPmwWrite(pinToWrite, color)
            #May need a small delay after call of this
            #wiringpi.delay(5)

async def main(websocket, port):
    """
    Is called by the websocket handler when a client connects to the server
    Returns void
    """
        #placeholder numbers
    led_pins = [[1 2 3]
                [4 5 6]
                [7 8 9]]
    rgb_values = await asyncio.create_task(receive_data(websocket))
    update_led(led_pins, rgb_values)


if __name__ == '__main__':
    """
    Establishes the websocket server at ws://ip:port and creates the asyncio event loop
    """
    wiringpi.wiringPiSetup()
    server = websockets.serve(main, ip_s, port_s)
    print("Server established at ws://{}:{}".format(ip_s, port_s))
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()