import time
import digitalio
import board
import displayio
import adafruit_il0373
import busio
import terminalio
import adafruit_ccs811
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from adafruit_bme280 import basic as adafruit_bme280

led_green = digitalio.DigitalInOut(board.GP18)
led_green.direction = digitalio.Direction.OUTPUT
led_yellow = digitalio.DigitalInOut(board.GP19)
led_yellow.direction = digitalio.Direction.OUTPUT
led_red = digitalio.DigitalInOut(board.GP20)
led_red.direction = digitalio.Direction.OUTPUT

# Used to ensure the display is free in CircuitPython
displayio.release_displays()

DISPLAY_WIDTH = 212
DISPLAY_HEIGHT = 104

BLACK = 0x000000
WHITE = 0xFFFFFF
RED = 0xFF0000
COLORS = [BLACK, WHITE, RED]

palette = displayio.Palette(3)
palette[0] = COLORS[0]
palette[1] = COLORS[1]
palette[2] = COLORS[2]


display_background = None
last_co2_vals = []

CO2_BASELINE = 30554 #29908 #30884 #31092 #30772

header_group = displayio.Group(scale=1, x=5, y=5)
title_group = displayio.Group(scale=2, x=10, y=20)
body_group = displayio.Group(scale=1, x=10, y=40)
desc_sub_group = displayio.Group(scale=1, x=0, y=0)
val_sub_group = displayio.Group(scale=1, x=73, y=0)
line_graph_sub_group = displayio.Group(scale=1, x=138, y=0)
body_group.append(desc_sub_group)
body_group.append(val_sub_group)
body_group.append(line_graph_sub_group)

def setDisplayBackground(color_index, group):
    global display_background

    # Set a background
    background_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
    background_bitmap.fill(color_index)
    bg_tile = displayio.TileGrid(background_bitmap, pixel_shader=palette)

    if display_background is not None:
        bg_i = group.index(display_background)
        group.remove(display_background)
        group.insert(bg_i, bg_tile)
    else:
        group.append(bg_tile)

    display_background = bg_tile

def setTitle(text, colorIndex=0):
    title_label = label.Label(terminalio.FONT, text=text, color=COLORS[colorIndex])
    if len(title_group) > 0:
        title_group.pop(0)
    title_group.append(title_label)

def setHeader(text, index, x, colorIndex=0, lbl_direction="LTR"):
    text_label = label.Label(terminalio.FONT, x=x, y=2, text=text, color=COLORS[colorIndex], label_direction=lbl_direction)
    if len(header_group) > index:
        header_group.pop(index)
    header_group.insert(index, text_label)

def setMeasLabel(text, index, x, y, colorIndex=0):
    text_label = label.Label(terminalio.FONT, x=x, y=y, text=text, color=COLORS[colorIndex])
    if len(desc_sub_group) > index:
        desc_sub_group.pop(index)
    desc_sub_group.insert(index, text_label)

def setMeasValue(text, index, x, y, colorIndex=0):
    text_label = label.Label(terminalio.FONT, x=x, y=y, text=text, color=COLORS[colorIndex])
    if len(val_sub_group) > index:
        val_sub_group.pop(index)
    val_sub_group.insert(index, text_label)

def setTextToDisplay(text, x, y, parentGroup, colorIndex=0):
    # Draw simple text using the built-in font into a displayio group
    text_label = label.Label(terminalio.FONT, x=x, y=y, text=text, color=COLORS[colorIndex])
    parentGroup.append(text_label)

def setTextToDisplayRTL(text, x, y, parentGroup, colorIndex=0):
    # Draw simple text using the built-in font into a displayio group
    text_label = label.Label(terminalio.FONT,  x=x, y=y, text=text, color=COLORS[colorIndex], label_direction="RTL")
    parentGroup.append(text_label)

def drawLineChart():
    global last_co2_vals
    for line in line_graph_sub_group:
        line_graph_sub_group.remove(line)
    last_co2_vals = last_co2_vals[-9:]
    for idx, avg in enumerate(last_co2_vals):
        fill_color = 0xFF0000 if avg > 1000 else 0x000000
        width_px = int(max(5, min((avg - 400) * (63/(1500-400)),63)))
        rect = Rect(0, 7*idx, width_px, 5, fill=fill_color)
        line_graph_sub_group.append(rect)
        outline = Rect(0, 0, 63, 63, outline=0x000000)
        line_graph_sub_group.append(outline)
        warning_line = Rect(20, 0, 1, 63, outline=0x000000)
        line_graph_sub_group.append(warning_line)
        red_line = Rect(34, 0, 1, 63, outline=0xFF0000)
        line_graph_sub_group.append(red_line)

def reverse_number(n):
    r = 0
    while n > 0:
        r *= 10
        r += n % 10
        n //= 10
    return r

def setCO2LED(co2_value):
    led_green.value = False
    led_yellow.value = False
    led_red.value = False
    if co2_value < 750:
        print("setting green")
        led_green.value = True
    elif co2_value < 1200:
        print("setting yellow")
        led_yellow.value = True
    else:
        print("setting red")
        led_red.value = True

measurements = {}
measurements["temperature"] = []
measurements["rel_humidity"] = []
measurements["pressure"] = []
measurements["altitude"] = []
measurements["co2"] = []
measurements["voc"] = []

def calculateAverages(temp, humidity, pressure, altitude, co2, voc, finish=False):
    averages = {}
    measurements["temperature"].append(temp)
    measurements["rel_humidity"].append(humidity)
    measurements["pressure"].append(pressure)
    measurements["altitude"].append(altitude)
    measurements["co2"].append(co2)
    measurements["voc"].append(voc)
    if finish:
        for key in measurements:
            sum_of_elems = sum(measurements[key])
            num_of_elems = len(measurements[key])
            avg = round(sum_of_elems / num_of_elems, 1) if num_of_elems > 0 else 0.0
            print(f"Getting avg: key: {key}, sum {sum_of_elems}, count: {num_of_elems}, avg: {avg}")
            averages[key] = avg
            measurements[key].clear()
    return averages

def updateDisplay(temp, humidity, pressure, altitude, co2, voc, cycle, curr_baseline):
    setDisplayBackground(1, g)

    setHeader(f"BL: {curr_baseline}", 0, 0)

    setHeader("Display Cycle:", 1, 80)

    setHeader(f"{reverse_number(cycle)}", 2, DISPLAY_WIDTH - 10, colorIndex=2, lbl_direction="RTL")
    setTitle("Measurements")

    setMeasLabel("Temperature:", 0, 0, 0)
    setMeasValue(f"{temp} °", 0, 0, 0)

    setMeasLabel("Humidity:", 1, 0, 11)
    setMeasValue(f"{humidity} %", 1, 0, 11)

    setMeasLabel("Pressure:", 2, 0, 22)
    setMeasValue(f"{pressure} hPa", 2, 0, 22)

    setMeasLabel("Altitude:", 3, 0, 33)
    setMeasValue(f"{altitude} m", 3, 0, 33)

    setMeasLabel("CO2:", 4, 0, 44)
    setMeasValue(f"{co2} ppm", 4, 0, 44)

    setMeasLabel("TVOC:", 5, 0, 55)
    setMeasValue(f"{voc} ppb", 5, 0, 55)

    drawLineChart()

    display.show(g)

    # Refresh the display to have everything show on the display
    # NOTE: Do not refresh eInk displays more often than 180 seconds!
    display.refresh()

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
setDisplayBackground(1, g)


g.append(header_group)
g.append(title_group)
g.append(body_group)

setTitle("Starting up...")

display.show(g)
display.refresh()
print("Display initialized")

# Create I2C
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
ccs =  adafruit_ccs811.CCS811(i2c)

# bme280.overscan_temperature = adafruit_bme280.OVERSCAN_X1
# bme280.mode = adafruit_bme280.MODE_SLEEP

# print(f"BME280 Sensor {bme280.overscan_temperature}, time: {bme280.measurement_time_typical}, {bme280.measurement_time_max}, mode: {bme280.mode}")

# Set basevalue
ccs.baseline = CO2_BASELINE #31092 #30772

cycle = 1
main_loop_counter = 1
next_refresh_cycle = 300     #int(display.time_to_refresh) updates display every ~180 cycles
measuring_cycle = 10                                        # take a measurement every 10 cycles
print(f"Refreshing time initial: {next_refresh_cycle}")
while True:
    if main_loop_counter % next_refresh_cycle == 0:
        ccs.baseline = CO2_BASELINE
        print(f"Refreshing display, cycle: {cycle}")
        print(f"baseline co2-sensor: {ccs.baseline}")
        averages = calculateAverages(bme280.temperature, bme280.relative_humidity, bme280.pressure, bme280.altitude, ccs.eco2, ccs.tvoc, True)
        last_co2_vals.append(averages["co2"])

        updateDisplay(averages["temperature"], averages["rel_humidity"], averages["pressure"], averages["altitude"], averages["co2"], averages["voc"], cycle, ccs.baseline)
        setCO2LED(averages["co2"])
        cycle += 1
    elif main_loop_counter % measuring_cycle == 0:
        ccs.baseline = CO2_BASELINE
        temperature = bme280.temperature
        relative_humidity = bme280.relative_humidity
        pressure = bme280.pressure
        altitude = bme280.altitude
        co2 = ccs.eco2
        voc = ccs.tvoc
        print(f"Temp {temperature}, rel. Hum {relative_humidity}, pressure {pressure}, altitude {altitude}")
        print(f"CO2: {co2}, TVOC: {voc}")
        calculateAverages(temperature, relative_humidity, pressure, altitude, co2, voc)

        print(f"Display updates in {next_refresh_cycle - (main_loop_counter % next_refresh_cycle)} s")

    time.sleep(1)

    main_loop_counter += 1
