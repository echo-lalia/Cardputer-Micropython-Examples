
from machine import Pin, SPI
import st7789py as st7789
import random
from font import vga2_16x32 as font



#this example uses the "st7789py" driver along with the "vga2_16x32" file to draw some random colorful boxes on the display. 



tft = st7789.ST7789(
    SPI(2, baudrate=40000000, sck=Pin(36), mosi=Pin(35), miso=None),
    135,
    240,
    reset=Pin(33, Pin.OUT),
    cs=Pin(37, Pin.OUT),
    dc=Pin(34, Pin.OUT),
    backlight=Pin(38, Pin.OUT),
    rotation=0,
    color_order=st7789.BGR
    )




def main():
    """
    The big show!
    """

    while True:
        for rotation in range(4):
            tft.rotation(rotation)
            tft.fill(0)
            col_max = tft.width - font.WIDTH * 5
            row_max = tft.height - font.HEIGHT
            if col_max < 0 or row_max < 0:
                raise RuntimeError(
                    "This font is too big to display on this screen."
                )

            for _ in range(100):
                tft.text(
                    font,
                    "Cardputer",
                    random.randint(0, col_max),
                    random.randint(0, row_max),
                    st7789.color565(
                        random.getrandbits(8),
                        random.getrandbits(8),
                        random.getrandbits(8),
                    ),
                    st7789.color565(
                        random.getrandbits(8),
                        random.getrandbits(8),
                        random.getrandbits(8),
                    ),
                )


main()