import regex
import asyncio
import websockets
#import wiringpi


class Server():

    def __init__(self):
        """Server Constants"""
        self.ip_s = "10.30.21.64"
        self.port_s = 5678
        self.r1_vld = 255
        self.g1_vld = 0
        self.b1_vld = 0
        self.r2_vld = 255
        self.g2_vld = 0
        self.b2_vld = 0
        self.r3_vld = 255
        self.g3_vld = 0
        self.b3_vld = 0

    def begin(self):
        #wiringpi.wiringPiSetup()
        self.server = websockets.serve(host.main, self.ip_s, self.port_s)
        print("Server established at ws://{}:{}".format(self.ip_s, self.port_s))
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    async def validate_string(self, str):
        """
        Takes argument str and verifies that it is of the form [[r1, g1, b1], [r2, g2, b2], [r3, g3, b3]]
        Populates _vld variables if the form is proper
        Returns true if the string is valid and false if invalid
        """
        str_r = regex.match(r'(\[?\[\d{1,3}, \d{1,3}, \d{1,3}\], \[\d{1,3}, \d{1,3}, \d{1,3}\], \[\d{1,3}, \d{1,3}, \d{1,3}\]\]?)', str)
        if str_r is None:
            return False
        else:
            values = await self.parse_string(str)
            self.r1_vld = values[0][0]
            self.g1_vld = values[0][1]
            self.b1_vld = values[0][2]
            self.r2_vld = values[1][0]
            self.g2_vld = values[1][1]
            self.b2_vld = values[1][2]
            self.r3_vld = values[2][0]
            self.g3_vld = values[2][1]
            self.b3_vld = values[2][2]
            return True

    @staticmethod
    async def parse_string(string):
        """
        Takes a string of the form [[r1, g1, b1], [r2, g2, b2], [r3, g3, b3]] and stores r g b values in a 2-d array
        Returns the two dimensional array: [[r1, g1, b1],
                                            [r2, g2, b2],
                                            [r3, g3, b3]]
        """
        buf = string.replace(" ", "").replace("[", "").replace("]", "").split(",")
        buffer = [[0 for i in range(3)] for i in range(3)]
        for i in range(3):
            for j in range(3):
                buffer[i][j] = int(buf[j + (3 * i)])
        return buffer

    async def receive_data(self, websocket):
        """
        Called when a client is connected. Waits for a string to be transmitted
        Returns the transmitted data
        """
        print("New client connected")
        data = await websocket.recv()
        if await self.validate_string(data):
            return data
        else:
            return False


    def update_led(self, led_pins):
        """
        Changes the values of the PWM signals to the LEDs based off of the values in rgb_values
        Returns void
        """
        rgb_values = [[0 for i in range(3)] for i in range(3)]
        rgb_values[0][0] = self.r1_vld
        rgb_values[0][1] = self.g1_vld
        rgb_values[0][2] = self.b1_vld
        rgb_values[1][0] = self.r2_vld
        rgb_values[1][1] = self.g2_vld
        rgb_values[1][2] = self.b2_vld
        rgb_values[2][0] = self.r3_vld
        rgb_values[2][1] = self.g3_vld
        rgb_values[2][2] = self.b3_vld
        for x in range(3):
            for y in range(3):
                pass
                #wiringpi.pinMode(led_pins[x][y], 1)
                #wiringpi.softPwmCreate(led_pins[x][y], 0, 255)
                #wiringpi.softPwmWrite(led_pins[x][y], 255-rgb_values[x][y])
        print("updating the LEDS with")
        print(rgb_values)

    async def main(self, websocket, port):
        """
        Is called by the websocket handler when a client connects to the server
        Returns void
        """
        led_pins = [[0, 2, 3],
                    [1, 4, 5],
                    [21, 22, 23]]
        rgb_values = await asyncio.create_task(self.receive_data(websocket))
        if rgb_values == 0:
            pass
        else:
            self.update_led(led_pins)


if __name__ == '__main__':
    """
    Establishes the websocket server at ws://ip:port and creates the asyncio event loop
    """
    host = Server()
    host.begin()
    #wiringpi.wiringPiSetup()
    #server = websockets.serve(host.main, ip_s, port_s)
    #print("Server established at ws://{}:{}".format(ip_s, port_s))
    #asyncio.get_event_loop().run_until_complete(server)
    #asyncio.get_event_loop().run_forever()

