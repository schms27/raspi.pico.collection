import time
import board
import displayio
import adafruit_il0373
import busio
import terminalio
from adafruit_display_text import label

# Used to ensure the display is free in CircuitPython
displayio.release_displays()

DISPLAY_WIDTH = 212
DISPLAY_HEIGHT = 104

BLACK = 0x000000
WHITE = 0xFFFFFF
RED = 0xFF0000
COLORS = [BLACK, WHITE, RED]


# Define the pins needed for display use
# This pinout is for a Feather M4 and may be different for other boards
epd_din_mosi = board.GP11
epd_clk = board.GP10
epd_cs = board.GP9
epd_dc = board.GP8
epd_reset = board.GP12
epd_busy = board.GP13
spi = busio.SPI(epd_clk, epd_din_mosi)

# Create the displayio connection to the display pins
display_bus = displayio.FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000
)
time.sleep(1)  # Wait a bit

# Create the display object - the third color is red (0xff0000)
display = adafruit_il0373.IL0373(
    display_bus,
    width=DISPLAY_WIDTH,
    height=DISPLAY_HEIGHT,
    rotation=90,
    busy_pin=epd_busy,
    highlight_color=RED,
)

# Create a display group for our screen objects
g = displayio.Group()

# Display a ruler graphic from the root directory of the CIRCUITPY drive
with open("/display-ruler.bmp", "rb") as f:
    pic = displayio.OnDiskBitmap(f)
    # Create a Tilegrid with the bitmap and put in the displayio group
    # CircuitPython 6 & 7 compatible
    t = displayio.TileGrid(
        pic, pixel_shader=getattr(pic, "pixel_shader", displayio.ColorConverter())
    )
    # CircuitPython 7 compatible only
    # t = displayio.TileGrid(pic, pixel_shader=pic.pixel_shader)
    g.append(t)

    # Place the display group on the screen
    display.show(g)

    # Refresh the display to have it actually show the image
    # NOTE: Do not refresh eInk displays sooner than 180 seconds
    display.refresh()
    print("refreshed")

    time.sleep(120)
  
cycle = 0
while True:
    print("Cycle: {0}".format(cycle))
    # Set a background
    background_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
    # Map colors in a palette
    palette = displayio.Palette(1)
    palette[0] = COLORS[cycle%3]

    # Create a Tilegrid with the background and put in the displayio group
    t = displayio.TileGrid(background_bitmap, pixel_shader=palette)
    g.append(t)
    
    # Draw simple text using the built-in font into a displayio group
    title_group = displayio.Group(scale=2, x=20, y=20)
    title = "Hello World!"
    title_area = label.Label(terminalio.FONT, text=title, color=COLORS[(cycle+1)%3])
    title_group.append(title_area)  # Add this text to the text group
    g.append(title_group)
    
    # Add counter
    cycle_group = displayio.Group(scale=2, x=20, y=40)
    cycle_text = "Cycle: {0}".format(cycle)
    cycle_area = label.Label(terminalio.FONT, text=cycle_text, color=COLORS[(cycle+2)%3])
    cycle_group.append(cycle_area)
    g.append(cycle_group)
    
    # Place the display group on the screen
    display.show(g)

    # Refresh the display to have everything show on the display
    # NOTE: Do not refresh eInk displays more often than 180 seconds!
    display.refresh()

    time.sleep(180)
    cycle += 1