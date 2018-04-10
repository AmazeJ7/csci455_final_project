from MockMaestro import Controller
from tkinter import *
import time
import os
import socket
import threading

# Maestro instantiation
controller = Controller()
for chan in range(len(controller.Targets)):
    controller.setTarget(chan, 6000)
controller.setAccel(0, 10)
controller.setAccel(1, 10)
controller.setAccel(2, 30)
controller.setAccel(3, 20)
controller.setAccel(3, 20)
os.system('xset r off')

# Global Variables
xpos = 0
ypos = 0
actions = []
actions_inv = []
pic_size = 40
port = 7777

# Main Tk window instantiation
root = Tk()
root.title('Robot Control GUI')

# Socket setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
temp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
temp_s.connect(('10.255.255.255', 1))
host = temp_s.getsockname()[0]
temp_s.close
print(host)
s.bind((host, port))
s.listen(5)

# Icon files and subsample
icons = [PhotoImage(file='icons/HeadTilt.png'), PhotoImage(file='icons/HeadRotate.png'),
         PhotoImage(file='icons/Move.png'), PhotoImage(file='icons/Rotate.png'),
         PhotoImage(file='icons/BodyRotate.png'), PhotoImage(file='icons/Wait.png'),
         PhotoImage(file='icons/STT.png'), PhotoImage(file='icons/TTS.png')]
for i in range(len(icons)):
    icons[i] = icons[i].subsample(5, 5)


# Function to initiate the socket
def init_socket():
    while True:
        global s_2
        print('Listening')
        s_2, ip = s.accept()
        print('Got a connection from %s' % str(ip))
        rt = threading.Thread(target=receive(s_2))
        rt.start()


# Function to receive STT commands
def receive(s_2):
    while True:
        global actions, actions_inv
        r = s_2.recv(1024)
        msg = r.decode('ascii')
        print('Received: ' + msg)
        msg_parts = msg.split()
        if msg_parts[0] == 'move':
            actions.append(Action('Move', icons[2], 1))
            actions_inv.append(Action('Move', icons[2], 0))
            if msg_parts[1] == 'for':
                actions[len(actions)-1].time = int(msg_parts[2])
                actions_inv[len(actions)-1].time = int(msg_parts[2])
            elif msg_parts[1] == 'forward':
                if len(msg_parts) > 2:
                    actions[len(actions)-1].time = int(msg_parts[3])
                    actions_inv[len(actions)-1].time = int(msg_parts[3])
                actions[len(actions)-1].pos = 1
                actions_inv[len(actions)-1].pos = 2
            elif msg_parts[1] == 'backward':
                if len(msg_parts) > 2:
                    actions[len(actions)-1].time = int(msg_parts[3])
                    actions_inv[len(actions)-1].time = int(msg_parts[3])
                actions[len(actions)-1].pos = 2
                actions_inv[len(actions)-1].pos = 2
        elif msg_parts[0] == 'run' or msg_parts[0] == 'go':
            if len(msg_parts) > 1:
                if msg_parts[1] == 'home':
                    time.sleep(1)
                    for x in range(len(actions_inv)):
                        actions.append(actions_inv[len(actions_inv)-x-1])
                    actions[0].time = int(actions[0].time/2)
                    run('andy')
                    del_all()
                    s_2.close()
            else:
                run('andy')
        elif msg_parts[0] == 'turn':
            actions.append(Action('Turn', icons[3], 1))
            actions_inv.append(Action('Turn', icons[3], 0))
            if msg_parts[1] == 'left':
                actions[len(actions)-1].pos = 1
                actions_inv[len(actions)-1].pos = 2
            elif msg_parts[1] == 'right':
                actions[len(actions)-1].pos = 2
                actions_inv[len(actions)-1].pos = 1
        elif msg_parts[0] == 'rotate':
            if msg_parts[1] == 'body':
                actions.append(Action('Body Rotate', icons[4], 1))
            elif msg_parts[1] == 'head':
                actions.append(Action('Head Rotate', icons[1], 1))
            if msg_parts[2] == 'left':
                actions[len(actions)-1].pos = 1
            elif msg_parts[2] == 'right':
                if msg_parts[1] == 'head':
                    actions[len(actions)-1].pos = 4
                else:
                    actions[len(actions)-1].pos = 2
        elif msg_parts[0] == 'tilt':
            actions.append(Action('Head Tilt', icons[0], 1))
            if msg_parts[2] == 'down':
                actions[len(actions)-1].pos = 1
            if msg_parts[2] == 'up':
                actions[len(actions)-1].pos = 4
        elif msg_parts[0] == 'wait':
            actions.append(Action('Wait', icons[5], 1))
            if len(msg_parts) > 2:
                if msg_parts[1] == 'for':
                    actions[len(actions)-1].time = int(msg_parts[2])
        elif msg == 'clear' or msg == 'delete all':
            del_all()
        if msg_parts[0] != 'go' and msg_parts[0] != 'run' and (msg_parts[len(msg_parts)-1] == 'run' or msg_parts[len(msg_parts)-1] == 'go'):
            run('andy')
        if msg_parts[0] != 'go' and msg_parts[0] != 'run':
            run('andy')


# Function to ask for speech
def send_stt():
    send_message = 'get speech\r\n'
    s_2.send(send_message.encode('ascii'))


# Function to run all actions
def run(who):
    global actions, xpos, ypos
    print('Running...')
    for x in range(len(actions)):
        actions[x].who = who
    for x in range(len(actions)):
        if actions[x].name == 'Head Tilt':
            send_message = 'tilting head\r\n'
            s_2.send(send_message.encode('ascii'))
            if actions[x].pos == 1:
                controller.setTarget(4, 4000)
            elif actions[x].pos == 2:
                controller.setTarget(4, 5000)
            elif actions[x].pos == 3:
                controller.setTarget(4, 7000)
            elif actions[x].pos == 4:
                controller.setTarget(4, 8000)
            elif actions[x].pos == 0:
                controller.setTarget(4, 6000)
            actions[x].animate()
            controller.setTarget(4, 6000)
        elif actions[x].name == 'Head Rotate':
            send_message = 'rotating head\r\n'
            s_2.send(send_message.encode('ascii'))
            if actions[x].pos == 1:
                controller.setTarget(3, 4000)
            elif actions[x].pos == 2:
                controller.setTarget(3, 5000)
            elif actions[x].pos == 3:
                controller.setTarget(3, 7000)
            elif actions[x].pos == 4:
                controller.setTarget(3, 8000)
            elif actions[x].pos == 0:
                controller.setTarget(3, 6000)
            actions[x].animate()
            controller.setTarget(3, 6000)
        elif actions[x].name == 'Move':
            send_message = 'moving\r\n'
            s_2.send(send_message.encode('ascii'))
            if actions[x].pos == 1:
                controller.setTarget(1, 5000)
            elif actions[x].pos == 2:
                controller.setTarget(1, 7000)
            elif actions[x].pos == 0:
                controller.setTarget(1, 6000)
            actions[x].animate()
            controller.setTarget(1, 6000)
        elif actions[x].name == 'Turn':
            send_message = 'turning\r\n'
            s_2.send(send_message.encode('ascii'))
            if actions[x].pos == 1:
                controller.setTarget(2, 7000)
            elif actions[x].pos == 2:
                controller.setTarget(2, 5000)
            elif actions[x].pos == 0:
                controller.setTarget(2, 6000)
            actions[x].animate()
            controller.setTarget(2, 6000)
        elif actions[x].name == 'Body Rotate':
            send_message = 'rotating body\r\n'
            s_2.send(send_message.encode('ascii'))
            if actions[x].pos == 1:
                controller.setTarget(0, 4250)
            elif actions[x].pos == 2:
                controller.setTarget(0, 7750)
            elif actions[x].pos == 0:
                controller.setTarget(0, 6000)
            actions[x].animate()
            controller.setTarget(0, 6000)
        elif actions[x].name == 'Wait':
            send_message = 'waiting\r\n'
            s_2.send(send_message.encode('ascii'))
            actions[x].animate()
        elif actions[x].name == 'TTS':
            send_message = 'nothing here\r\n'
            if actions[x].pos == 1:
                send_message = 'nothing here\r\n'
            elif actions[x].pos == 2:
                send_message = 'something here\r\n'
            elif actions[x].pos == 3:
                send_message = 'you are not nice\r\n'
            elif actions[x].pos == 4:
                send_message = 'hello friend\r\n'
            elif actions[x].pos == 4:
                send_message = 'kill humans\r\n'
            elif actions[x].pos == 4:
                send_message = 'I do not like you\r\n'
            s_2.send(send_message.encode('ascii'))
            actions[x].animate()
        elif actions[x].name == 'STT':
            actions[x].animate()
    posx = 25
    posy = 25
    for x in range(len(actions)):
        if posx < 700:
            canvas.create_image(posx, posy, image=actions[x].icon)
            posx += 55
        else:
            posy += 55
            posx = 25
            canvas.create_image(posx, posy, image=actions[x].icon)
            posx += 55


# Function to delete all actions and reset canvas
def del_all():
    global xpos, ypos, actions
    canvas.delete('all')
    xpos = 0
    ypos = 0
    actions = []


# Function to add actions
def add_to_actions(action):
    if action == 'Move':
        actions.append(Action('Move', icons[2], 1))
        actions_inv.append(Action('Move', icons[2], 0))
    elif action == 'Turn':
        actions.append(Action('Turn', icons[3], 1))
        actions_inv.append(Action('Turn', icons[3], 0))


# Class to represent an action to be run
class Action:
    def __init__(self, name, icon, show):
        global xpos, ypos, stt_thread, actions
        self.name = name
        self.icon = icon
        if show:
            if xpos < 700:
                canvas.create_image(25 + xpos, 25 + ypos, image=self.icon)
            else:
                ypos += 55
                xpos = 0
                canvas.create_image(25 + xpos, 25 + ypos, image=self.icon)
            xpos += 55
        self.time = 2
        self.pos = 0
        self.settings_tk = ''
        self.animate_tk = ''
        self.who = ''

    # Animation function!
    def animate(self):
        canvas.delete('all')
        if self.name == 'STT':
            self.time = 1000
            send_stt()
            del_all()
        rect = []
        if self.name != 'STT':
            canvas.create_text(100, 130, text=self.name + ' : ' + str(self.time) + ' seconds', fill='white')
        else:
            canvas.create_text(100, 130, text=self.name, fill='white')
        if self.pos == 0:
            canvas.create_text(100, 150, text='Waiting...', fill='white')
        else:
            canvas.create_text(100, 150, text='Position : ' + str(self.pos), fill='white')
        if self.name != 'STT':
            for x in range(self.time):
                rect.append(canvas.create_image(25 + 55 * x, 200, image=self.icon))
        if self.who == 'andy':
            for x in range(self.time):
                time.sleep(1)
                canvas.update()
                if self.name != 'STT':
                    canvas.delete(rect[self.time - x - 1])
        elif self.who == 'button':
            for x in range(self.time):
                canvas.update()
                if self.name != 'STT':
                    canvas.delete(rect[self.time - x - 1])
                time.sleep(1)
        canvas.delete('all')

    # Function to edit settings or remove instance
    def open_settings(self):
        def save_val():
            self.time = time_scale.get()
            if self.name != 'Wait' and self.name != 'STT':
                self.pos = position.get()
            if self.name == 'Move' or self.name == 'Turn':
                actions_inv[len(actions)-1].pos = 3-self.pos
            self.settings_tk.destroy()

        self.settings_tk = Tk()
        self.settings_tk.title('Settings')
        label1 = Label(self.settings_tk, text='Time (S)')
        label1.pack()
        time_scale = Scale(self.settings_tk, from_=1, to=10, orient=HORIZONTAL)
        time_scale.set(self.time)
        time_scale.pack()
        if self.name == 'Head Tilt':
            label1 = Label(self.settings_tk, text='Head Tilt Position (Top to Bottom)')
            position = Scale(self.settings_tk, from_=1, to=4, orient=HORIZONTAL)
        elif self.name == 'Head Rotate':
            label1 = Label(self.settings_tk, text='Head Rotate Position (Left to Right)')
            position = Scale(self.settings_tk, from_=1, to=4, orient=HORIZONTAL)
        elif self.name == 'Turn':
            label1 = Label(self.settings_tk, text='Turning Direction (Left or Right)')
            position = Scale(self.settings_tk, from_=1, to=2, orient=HORIZONTAL)
        elif self.name == 'Move':
            label1 = Label(self.settings_tk, text='Movement Direction (Foreword or Backward)')
            position = Scale(self.settings_tk, from_=1, to=2, orient=HORIZONTAL)
        elif self.name == 'Body Rotate':
            label1 = Label(self.settings_tk, text='Body Rotate Position (Left to Right)')
            position = Scale(self.settings_tk, from_=1, to=2, orient=HORIZONTAL)
        elif self.name == 'TTS':
            label1 = Label(self.settings_tk, text='Text to Say')
            position = Scale(self.settings_tk, from_=1, to=6, orient=HORIZONTAL)
        if self.name != 'Wait' and self.name != 'STT':
            position.set(self.pos)
            position.pack()
        label1.pack()
        save_values = Button(self.settings_tk, text='Save Values', command=save_val)
        save_values.pack()
        delete = Button(self.settings_tk, text='Delete', command=self.__delete__)
        delete.pack()
        self.settings_tk.mainloop()

    def __delete__(self):
        global xpos, actions
        self.time = 0
        self.pos = 0
        canvas.delete('all')
        xpos -= 55
        posx = 25
        posy = 25
        actions.remove(self)
        self.settings_tk.destroy()
        for x in range(len(actions)):
            if posx < 700:
                canvas.create_image(posx, posy, image=actions[x].icon)
                posx += 55
            else:
                posy += 55
                posx = 25
                canvas.create_image(posx, posy, image=actions[x].icon)
                posx += 55


# Mouse movement class
class MouseMovement:
    def __init__(self):
        self.flag = False

    def mouse_pressed(self, event):
        global actions
        y = 0
        for x in range(len(actions)):
            if x == 13 * (y + 1):
                y += 1
            if x * 55 + 50 - 715 * y > event.x > x * 55 - 715 * y and y * 55 < event.y < y * 55 + 50:
                self.flag = True
                actions[x].open_settings()

    def mouse_release(self, event):
        if self.flag:
            self.flag = False


# Mouse movement class instantiation
m = MouseMovement()

# Root's canvas
canvas = Canvas(root, bg='#1F1F1F', width='750', height='443')
canvas.pack(side=RIGHT)
canvas.bind('<ButtonPress-1>', m.mouse_pressed)
canvas.bind('<ButtonRelease-1>', m.mouse_release)

# Root's buttons
go = Button(root, height=1, width=5, text='GO!', bg='black', fg='white', command=lambda: run('button'))
go.pack(side=TOP)
ht = Button(root, command=lambda: actions.append(Action('Head Tilt', icons[0], 1)), image=icons[0], width=pic_size, height=pic_size)
ht.pack(side=TOP)
hr = Button(root, command=lambda: actions.append(Action('Head Rotate', icons[1], 1)), image=icons[1], width=pic_size, height=pic_size)
hr.pack(side=TOP)
move = Button(root, command=lambda: add_to_actions('Move'), image=icons[2], width=pic_size, height=pic_size)
move.pack(side=TOP)
turn = Button(root, command=lambda: add_to_actions('Turn'), image=icons[3], width=pic_size, height=pic_size)
turn.pack(side=TOP)
br = Button(root, command=lambda: actions.append(Action('Body Rotate', icons[4], 1)), image=icons[4], width=pic_size, height=pic_size)
br.pack(side=TOP)
wait = Button(root, command=lambda: actions.append(Action('Wait', icons[5], 1)), image=icons[5], width=pic_size, height=pic_size)
wait.pack(side=TOP)
stt_button = Button(root, command=lambda: actions.append(Action('STT', icons[6], 1)), image=icons[6], width=pic_size, height=pic_size)
stt_button.pack(side=TOP)
tts_button = Button(root, command=lambda: actions.append(Action('TTS', icons[7], 1)), image=icons[7], width=pic_size, height=pic_size)
tts_button.pack(side=TOP)
del_all_button = Button(root, height=1, width=5, text='Clear', bg='black', fg='white', command=del_all)
del_all_button.pack(side=TOP)
stt_button_2 = Button(root, height=1, width=5, text='STT', bg='black', fg='white', command=send_stt)
stt_button_2.pack(side=TOP)

# Socket thread init
init_socket_thread = threading.Thread(target=init_socket)
init_socket_thread.start()

# Main tk loop and geometry
root.geometry('800x450')
root.mainloop()
os.system('xset r on')
