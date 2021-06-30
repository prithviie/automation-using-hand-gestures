from tkinter import PhotoImage
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import os
import threading
import turtle
import random
# import pyfirmata


# turtle
win_x = 600
win_y = 400
wn = turtle.Screen()
wn.bgcolor('white')
wn.title('Home')
wn.setup(width=win_x+20, height=win_y+20)

red = (-250, 170, 60, 60)
red_state = 0

green = (-250, 50, 60, 60)
green_state = 0

rain = (-250, -70, 60, 60)
rain_state = False

fan = (-90, 100, 50)
fan_state = False
stop_thread = False

floor = (-80, -10, 300, 150)
floor_filling = False

gif_dir = 'gifs/'
gifs = os.listdir(gif_dir)
tv = (150, 90)
channel_count = 1


# pubnub
count = 0
msg_threshold = 15
msg_list = []
ENTRY = "GestureControl"
CHANNEL = "Detect"
KILL_CONNECTION = "exit"

pnconfig = PNConfiguration()
pnconfig.publish_key = 'your publisher key'
pnconfig.subscribe_key = 'your subscriber key'
pnconfig.uuid = "serverUUID-SUB"
pubnub = PubNub(pnconfig)


# arduino
# board = pyfirmata.Arduino("COM4")  # for arduino board

# configuring pins for sensors
# lenPin = board.get_pin('d:11:p')
# red_led = board.get_pin('d:5:p')  # digital pin 6
# green_led = board.get_pin('d:6:p')  # digital pin 7
# gas_sen = board.get_pin('a:0:i')  # analog input 0
# rain_sens = board.get_pin('a:1:i')  # analog input 1

# it = pyfirmata.util.Iterator(board)
# it.start()


def draw_border(l, b):
    border = turtle.Turtle()
    border.speed(0)
    border.penup()
    border.pensize(4)
    border.color('black')
    border.setposition(-l//2, -b//2)
    border.pendown()
    border.hideturtle()

    border.fd(l)
    border.lt(90)

    border.fd(b)
    border.lt(90)

    border.fd(l)
    border.lt(90)

    border.fd(b)


def draw_sq(pos, color='white', win_length=win_x, win_breadth=win_y):
    # (x, y) correspond to the top left corners for the rectangle

    x, y, length, breadth = pos

    rect = turtle.Turtle()
    rect.penup()
    rect.pensize(2)
    rect.speed(0)
    rect.setposition(x, y)
    rect.pendown()
    rect.hideturtle()
    rect.fillcolor(color)
    rect.begin_fill()

    for _ in range(4):
        rect.fd(length)
        rect.rt(90)

    rect.end_fill()


def draw_fan(pos):

    x, y, r = pos
    y -= r
    circle = turtle.Turtle()
    circle.hideturtle()
    circle.speed(0)
    circle.pensize(2)
    circle.penup()

    circle.setpos(x, y)
    circle.pendown()
    # circle.speed(5)
    # circle.showturtle()
    circle.circle(r)


def draw_tv(pos, image=gif_dir+'0.gif'):

    x, y = pos
    larger = PhotoImage(file=image).subsample(2, 2)
    wn.addshape("larger", turtle.Shape("image", larger))
    tv = turtle.Turtle("larger")
    tv.speed(0)
    tv.hideturtle()
    tv.penup()
    tv.setposition(x, y)
    tv.stamp()


def turn_fan():
    x, y, r = fan
    y -= r
    global fan_state
    global stop_thread

    if fan_state is False:
        fan_state = True

        circle = turtle.Turtle()
        circle.hideturtle()
        circle.speed(0)
        circle.pensize(2)
        circle.penup()

        circle.setpos(x, y)
        circle.pendown()
        circle.showturtle()

        while True:
            if stop_thread:
                stop_thread = False
                break

            circle.circle(r)
            circle.speed(5)


def fill_floor():
    global floor_filling

    if floor_filling is False:
        floor_filling = True
        x, y, w, h = floor

        x += 15
        y -= 15
        w -= 30
        step = 20

        filler = turtle.Turtle()
        filler.hideturtle()
        filler.penup()
        filler.setposition(x, y)
        filler.pendown()
        filler.pensize(25)
        filler.pencolor('white')

        for i in range(3):
            filler.fd(w)
            filler.setheading(270)
            filler.fd(step)

            filler.setheading(180)
            filler.fd(w)

            filler.setheading(270)
            filler.fd(step)
            filler.setheading(0)
        filler.fd(w)
    return


# triggering functions

def red_on():
    global red_state
    if red_state == 0 or red_state == 0.5:
        red_state = 1
        # red_led.write(0.999)
        draw_sq(red, 'red')
        print("----------------------------->> Red ON")
        return
    return


def red_half_on():
    global red_state
    if red_state == 1 or red_state == 0:
        red_state = 0.5
        # red_led.write(0.3)
        draw_sq(red, 'orange')
        print("----------------------------->> Red half ON")
        return
    return


def red_off():
    global red_state
    if red_state == 1 or red_state == 0.5:
        red_state = 0
        # red_led.write(0.001)
        draw_sq(red, 'white')
        print("----------------------------->> Red OFF")
        return
    return


def green_on():
    global green_state
    if green_state == 0 or green_state == 0.5:
        green_state = 1
        # green_led.write(0.999)
        draw_sq(green, 'green')
        print("----------------------------->> Green ON")
        return
    return


def green_half_on():
    global green_state
    if green_state == 1 or green_state == 0:
        green_state = 0.5
        # green_led.write(0.3)
        draw_sq(green, 'yellow')
        print("----------------------------->> Green Half ON")
        return
    return


def green_off():
    global green_state
    if green_state == 0.5 or green_state == 1:
        green_state = 0
        # green_led.write(0.001)
        draw_sq(green, 'white')
        print("----------------------------->> Green OFF")
        return
    return


def get_rainval():
    # rainval = 89.0678 #rain_sens.read()

    draw_sq(rain, color='white')

    num = random.randint(1, 100)

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    t.setposition(rain[0], rain[1])
    t.pendown()
    t.fillcolor('red')
    t.begin_fill()
    t.pensize(2)

    num = (rain[2]/100) * num

    t.fd(num)
    t.rt(90)
    t.fd(rain[2])
    t.rt(90)
    t.fd(num)
    t.rt(90)
    t.fd(rain[2])
    t.end_fill()

    print('----------------------------->> Rainval check')
    return


def fan_on():
    f = threading.Thread(target=turn_fan)
    f.start()
    print("----------------------------->> Fan ON")
    return


def fan_off():
    global stop_thread
    global fan_state

    stop_thread = True
    fan_state = False
    print("----------------------------->> Fan OFF")
    return


def change_channel():
    global channel_count

    if channel_count >= len(gifs):
        channel_count = 0

    draw_tv(tv, gif_dir + gifs[channel_count])
    print("----------------------------->> Channel change on TV")

    channel_count += 1
    return


def clean_floor():
    c = threading.Thread(target=fill_floor)
    c.start()
    print("----------------------------->> Floor cleaning")
    return


# 2 - 12
func_map = {
    '11': red_on,            # thumbs up
    '10': red_half_on,       # thumbs down
    '3': red_off,            # fist

    '12': green_on,          # two
    '9': green_half_on,      # three
    '5': green_off,          # four

    '6': get_rainval,        # ok

    '7': fan_on,             # one
    '8': fan_off,            # stop

    '2': change_channel,     # right

    '4': clean_floor         # palm-five
}


def most_frequent(List):
    return max(set(List), key=List.count)


class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, event):
        print("[PRESENCE: {}]".format(event.event))
        print("uuid: {}, channel: {}".format(event.uuid, event.channel))

    def status(self, pubnub, event):
        if event.category == PNStatusCategory.PNConnectedCategory:
            print("[STATUS: PNConnectedCategory]")
            print("connected to channels: {}".format(event.affected_channels))

    def message(self, pubnub, event):
        global count
        global msg_list
        print(f"Count = {count}")

        print("[MESSAGE received]")

        if event.message["update"] == KILL_CONNECTION:
            print("The publisher has ended the session.")
            os._exit(0)
        else:
            # print("{}: {}".format(
            #     event.message["entry"], event.message["update"]))

            recvd_msg = str(event.message["update"])
            print(f"Message = {recvd_msg}")

        #     if recvd_msg in func_map.keys():
        #         func_map[recvd_msg]()

        # count += 1

            msg_list.append(recvd_msg)
            print(msg_list)

            if len(msg_list) >= msg_threshold:
                actuate = most_frequent(msg_list)
                msg_list.clear()

                if actuate in func_map.keys():
                    func_map[actuate]()

        count += 1


def setup():
    # text and other setup

    # red led
    turtle.speed(0)
    turtle.hideturtle()
    turtle.penup()
    turtle.setpos(red[0]+2, red[1]-90)
    turtle.write('Red light', font=('Verdana', 10, 'normal'))

    # green led
    turtle.speed(0)
    turtle.hideturtle()
    turtle.penup()
    turtle.setpos(green[0]-5, green[1]-90)
    turtle.write('Green light', font=('Verdana', 10, 'normal'))

    # rain sensor
    turtle.speed(0)
    turtle.hideturtle()
    turtle.penup()
    turtle.setpos(rain[0]-5, rain[1]-90)
    turtle.write('Rain Sensor', font=('Verdana', 10, 'normal'))

    # fan
    turtle.speed(0)
    turtle.hideturtle()
    turtle.penup()
    turtle.setpos(fan[0]-10, fan[1]+60)
    turtle.write('Fan', font=('Verdana', 10, 'normal'))

    # tv
    tv_border = turtle.Turtle()
    tv_border.speed(0)
    tv_border.hideturtle()
    tv_border.pensize(2)
    tv_border.penup()
    tv_border.setposition(tv[0]-98, 160)
    tv_border.pendown()
    tv_border.fd(197)
    tv_border.rt(90)
    tv_border.fd(140)
    tv_border.rt(90)
    tv_border.fd(197)
    tv_border.rt(90)
    tv_border.fd(140)

    turtle.speed(0)
    turtle.hideturtle()
    turtle.penup()
    turtle.setpos(tv[0]-8, tv[1]+80)
    turtle.write('TV', font=('Verdana', 10, 'normal'))

    # floor
    f = turtle.Turtle()
    f.hideturtle()
    f.speed(0)
    f.penup()
    f.setposition(floor[0], floor[1])
    f.pendown()
    f.pensize(2)
    f.fillcolor('grey')
    f.begin_fill()
    f.fd(floor[2])
    f.rt(90)
    f.fd(floor[3])
    f.rt(90)
    f.fd(floor[2])
    f.rt(90)
    f.fd(floor[3])
    f.end_fill()

    turtle.speed(0)
    turtle.hideturtle()
    turtle.penup()
    turtle.setpos(floor[0]+floor[2]//2 - 15, floor[1]-floor[3]-20)
    turtle.write('Floor', font=('Verdana', 10, 'normal'))


draw_border(win_x, win_y)
draw_sq(red, color='white')
draw_sq(green, color='white')
draw_sq(rain, color='white')
draw_fan(fan)
draw_tv(tv)
setup()


pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(CHANNEL).with_presence().execute()

print("***************************************************")
print("* Waiting for updates to about {}...  *".format(ENTRY))
print("***************************************************")


turtle.done()
