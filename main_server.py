import regex
import asyncio
import websockets
import wiringpi



"""Server Constants"""
ip_s = "10.30.21.65"
port_s = 5678

r1_vld = 255
g1_vld = 0
b1_vld = 0

r2_vld = 255
g2_vld = 0
b2_vld = 0

r3_vld = 255
g3_vld = 0
b3_vld = 0

# https://raspberrypi.stackexchange.com/questions/298/can-i-use-the-gpio-for-pulse-width-modulation-pwm

async def validate_string(str):
    """
    Takes argument str and verifies that it is of the form [[r1, g1, b1], [r2, g2, b2], [r3, g3, b3]]
    Populates _vld variables if the form is proper
    Returns true if the string is valid and false if invalid
    """

    global r1_vld
    global g1_vld
    global b1_vld
    global r2_vld
    global g2_vld
    global b2_vld
    global r3_vld
    global g3_vld
    global b3_vld
    str_r = regex.match(r'(\[?\[\d{1,3}, \d{1,3}, \d{1,3}\],? ?\]?)', str)
    print(str_r)
    if str_r is None:
        return False
    else:
        values = await parse_string(str)
        r1_vld = values[0][0]
        g1_vld = values[0][1]
        b1_vld = values[0][2]
        r2_vld = values[1][0]
        g2_vld = values[1][1]
        b2_vld = values[1][2]
        r3_vld = values[2][0]
        g3_vld = values[2][1]
        b3_vld = values[2][2]
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
    await validate_string(data)
    return data


def update_led(led_pins):
    """
    Changes the values of the PWM signals to the LEDs based off of the values in rgb_values
    Returns void
    """
    rgb_values = [[0 for i in range(3)] for i in range(3)]
    rgb_values[0][0] = r1_vld
    rgb_values[0][1] = g1_vld
    rgb_values[0][2] = b1_vld
    rgb_values[1][0] = r2_vld
    rgb_values[1][1] = g2_vld
    rgb_values[1][2] = b2_vld
    rgb_values[2][0] = r3_vld
    rgb_values[2][1] = g3_vld
    rgb_values[2][2] = b3_vld
    for x in range(3):
        for y in range(3):
            wiringpi.pinMode(led_pins[x][y], 1)
            wiringpi.softPwmCreate(led_pins[x][y], 0, 255)
            wiringpi.softPwmWrite(led_pins[x][y], 255-rgb_values[x][y])
    print("updating the LEDS with")
    print(rgb_values)


def setColor(pins, rgb):
    """
    Takes two arguments: pins and rgb. Pins contains the three pins connected to a specific led and
    rgb contains the three color values for that LED
    Returns void
    """
#    print(pins)
#    print(rgb)
#    for i in range(0,3):
#        wiringpi.pinMode(pins[i], 1)
#        wiringpi.softPwmCreate(pins[i], 0, 255)
#        wiringpi.softPwmWrite(pins[i], 255-rgb[i])

async def main(websocket, port):
    """
    Is called by the websocket handler when a client connects to the server
    Returns void
    """
        #placeholder numbers
    led_pins = [[0, 2, 3],
                [1, 4, 5],
                [21, 22, 23]]
    rgb_values = await asyncio.create_task(receive_data(websocket))
    update_led(led_pins)


if __name__ == '__main__':
    """
    Establishes the websocket server at ws://ip:port and creates the asyncio event loop
    """
    wiringpi.wiringPiSetup()
    server = websockets.serve(main, ip_s, port_s)
    print("Server established at ws://{}:{}".format(ip_s, port_s))
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

