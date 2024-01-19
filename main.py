from stupidArtnet import StupidArtnetServer
import time
import time
from rpi_ws281x import PixelStrip
from math import log2
import os

LED_COUNT = int(os.getenv('LED_COUNT'))        # Number of LED pixels.
LED_PIN = 21                                    # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10                                  # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000                            # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10                                    # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255                            # Set to 0 for darkest and 255 for brightest
LED_INVERT = False                              # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0                                 # set to '1' for GPIOs 13, 19, 41, 45 or 53

# It is used as a library
LED_FOR_SEGMENT = int(os.getenv("LED_PER_SEGMENT"))
NUMBER_OF_SEGMENT = LED_COUNT // LED_FOR_SEGMENT
NUMBER_OF_CHANNEL = 3 * NUMBER_OF_SEGMENT

UNIVERSE = int(os.getenv("UNIVERSE"))

class LedController:

    strobe_state:bool = False
    brightness: int = 255
    strobe_interval:int = 0
    last_time:float = 0.0

    def __init__(self) -> None:
        if NUMBER_OF_CHANNEL > 512:
            print("Too many segment for the number of channel")
            exit()
        self.artnet_server = StupidArtnetServer()

        # Initalize strip
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

        # Start ArtNet listener
        self.listener = self.artnet_server.register_listener(UNIVERSE)

    def strobe(self): # Let do more efficent, maybe with interrupts
        if self.strobe_interval < 10:
            self.strip.setBrightness(self.brightness)
        elif abs(time.time()-self.last_time)>1-(log2(self.strobe_interval)/8.10):
            self.strip.setBrightness(0 if self.strobe_state else self.brightness)
            self.strobe_state = not self.strobe_state
            self.last_time = time.time()

    def update(self) -> None:
        data = self.artnet_server.get_buffer(listener_id=self.listener)
        if len(data)>0:
            self.brightness = data[0]
            self.strobe_interval = data[1]
            offset = 2
            for segment in range(NUMBER_OF_SEGMENT):
                for led in range(LED_FOR_SEGMENT):
                    led_index = (segment*LED_FOR_SEGMENT)+led
                    self.strip.setPixelColorRGB(led_index, data[(3 * segment) + 0 + offset], data[(3 * segment) + 1 + offset], data[(3 * segment) + 2 + offset])
            # self.strip.setBrightness(self.brightness)
            self.strobe()
            self.strip.show()

    def run_forever(self):
        while True:
            self.update()



if __name__=="__main__":
    s = LedController()
    s.run_forever()




