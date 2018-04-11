from MockMaestro import Controller
from tkinter import *
import time
import os
import socket
import threading
import random

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
port = 7777

# Socket setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
temp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
temp_s.connect(('10.255.255.255', 1))
host = temp_s.getsockname()
temp_s.close
print(str(host[0]))
s.bind((str(host[0]), port))
s.listen(5)


# Function to initiate the socket
def init_socket():
    while True:
        global s_2
        print('Listening')
        s_2, ip = s.accept()
        print('Got a connection from %s' % str(ip))
        rt = threading.Thread(target=receive(s_2))
        rt.start()


# Function to ask for speech
def send_stt():
    send_message = 'get speech\r\n'
    s_2.send(send_message.encode('ascii'))


# Function to receive STT commands
def receive(r_s):
    while True:
        r = r_s.recv(1024)
        msg = r.decode('ascii')
        print('Received: ' + msg)
        msg_parts = msg.split()
        if msg_parts[0] == 'start':
            board.start()


# Class to represent the board
class Board:
    def __init__(self):
        self.map = []
        self.map.append(Location(1, 0, 1, 0, 0))
        self.map.append(Location(2, 0, 1, 1, 1))
        self.map.append(Location(3, 0, 0, 1, 1))
        self.map.append(Location(4, 0, 1, 0, 0))
        self.map.append(Location(5, 0, 0, 1, 1))

        self.map.append(Location(6, 0, 1, 1, 0))
        self.map.append(Location(7, 1, 0, 1, 1))
        self.map.append(Location(8, 1, 0, 0, 0))
        self.map.append(Location(9, 0, 1, 1, 0))
        self.map.append(Location(10, 1, 0, 1, 1))

        self.map.append(Location(11, 1, 0, 1, 0))
        self.map.append(Location(12, 1, 1, 0, 0))
        self.map.append(Location(13, 0, 1, 0, 1))
        self.map.append(Location(14, 1, 0, 1, 1))
        self.map.append(Location(15, 1, 0, 1, 0))

        self.map.append(Location(16, 1, 1, 0, 0))
        self.map.append(Location(17, 0, 0, 1, 1))
        self.map.append(Location(18, 0, 0, 1, 0))
        self.map.append(Location(19, 1, 1, 1, 0))
        self.map.append(Location(20, 1, 0, 0, 1))

        self.map.append(Location(21, 0, 1, 0, 0))
        self.map.append(Location(22, 1, 1, 0, 1))
        self.map.append(Location(23, 1, 0, 0, 1))
        self.map.append(Location(24, 1, 1, 0, 0))
        self.map.append(Location(25, 0, 0, 0, 1))

    def print_board(self):
        for i in range(5):
            for j in range(5):
                self.map[i*5+j].print_top()
            print()
            for j in range(5):
                self.map[i*5+j].print_mid()
            print()
            for j in range(5):
                self.map[i*5+j].print_bot()
            print()

    def start(self):
        start = Location
        end = Location
        items = [1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25]
        random.shuffle(items)
        for i in self.map:
            if items[0] == i.num:
                start = i
        if 0 < items[0] < 6:
            end = self.map[random.randint(20, 24)]
        elif items[0] == 6 or items[0] == 11 or items[0] == 16:
            locations = [self.map[5], self.map[11], self.map[16]]
            random.shuffle(locations)
            end = locations[0]
        elif items[0] == 10 or items[0] == 15 or items[0] == 20:
            locations = [self.map[9], self.map[14], self.map[19]]
            random.shuffle(locations)
            end = locations[0]
        elif 20 < items[0] < 26:
            end = self.map[random.randint(0, 4)]
        print('Starting at '+str(items[0]))
        s_2.send(('Starting at '+str(items[0])).encode('ascii'))
        time.sleep(3)
        s_2.send('Where to?'.encode('ascii'))


class Location:
    def __init__(self, num, n, e, s, w):
        self.num = num
        self.n = n
        self.e = e
        self.s = s
        self.w = w

    def print_top(self):
        if self.n:
            print('   |  ', end='')
        else:
            print('      ', end='')

    def print_mid(self):
        if self.num < 10:
            if self.w:
                print('---' + str(self.num), end='')
            else:
                print('   ' + str(self.num), end='')
        else:
            if self.w:
                print('--' + str(self.num), end='')
            else:
                print('  ' + str(self.num), end='')
        if self.e:
            print('--', end='')
        else:
            print('  ', end='')

    def print_bot(self):
        if self.s:
            print('   |  ', end='')
        else:
            print('      ', end='')


board = Board()
board.print_board()
# Socket thread init
init_socket_thread = threading.Thread(target=init_socket)
init_socket_thread.start()







# # Function to run all actions
# def run(who):
#     global actions, xpos, ypos
#     print('Running...')
#     for x in range(len(actions)):
#         actions[x].who = who
#     for x in range(len(actions)):
#         if actions[x].name == 'Head Tilt':
#             send_message = 'tilting head\r\n'
#             s_2.send(send_message.encode('ascii'))
#             if actions[x].pos == 1:
#                 controller.setTarget(4, 4000)
#             elif actions[x].pos == 2:
#                 controller.setTarget(4, 5000)
#             elif actions[x].pos == 3:
#                 controller.setTarget(4, 7000)
#             elif actions[x].pos == 4:
#                 controller.setTarget(4, 8000)
#             elif actions[x].pos == 0:
#                 controller.setTarget(4, 6000)
#             actions[x].animate()
#             controller.setTarget(4, 6000)
#         elif actions[x].name == 'Head Rotate':
#             send_message = 'rotating head\r\n'
#             s_2.send(send_message.encode('ascii'))
#             if actions[x].pos == 1:
#                 controller.setTarget(3, 4000)
#             elif actions[x].pos == 2:
#                 controller.setTarget(3, 5000)
#             elif actions[x].pos == 3:
#                 controller.setTarget(3, 7000)
#             elif actions[x].pos == 4:
#                 controller.setTarget(3, 8000)
#             elif actions[x].pos == 0:
#                 controller.setTarget(3, 6000)
#             actions[x].animate()
#             controller.setTarget(3, 6000)
#         elif actions[x].name == 'Move':
#             send_message = 'moving\r\n'
#             s_2.send(send_message.encode('ascii'))
#             if actions[x].pos == 1:
#                 controller.setTarget(1, 5000)
#             elif actions[x].pos == 2:
#                 controller.setTarget(1, 7000)
#             elif actions[x].pos == 0:
#                 controller.setTarget(1, 6000)
#             actions[x].animate()
#             controller.setTarget(1, 6000)
#         elif actions[x].name == 'Turn':
#             send_message = 'turning\r\n'
#             s_2.send(send_message.encode('ascii'))
#             if actions[x].pos == 1:
#                 controller.setTarget(2, 7000)
#             elif actions[x].pos == 2:
#                 controller.setTarget(2, 5000)
#             elif actions[x].pos == 0:
#                 controller.setTarget(2, 6000)
#             actions[x].animate()
#             controller.setTarget(2, 6000)
#         elif actions[x].name == 'Body Rotate':
#             send_message = 'rotating body\r\n'
#             s_2.send(send_message.encode('ascii'))
#             if actions[x].pos == 1:
#                 controller.setTarget(0, 4250)
#             elif actions[x].pos == 2:
#                 controller.setTarget(0, 7750)
#             elif actions[x].pos == 0:
#                 controller.setTarget(0, 6000)
#             actions[x].animate()
#             controller.setTarget(0, 6000)
#         elif actions[x].name == 'Wait':
#             send_message = 'waiting\r\n'
#             s_2.send(send_message.encode('ascii'))
#             actions[x].animate()
#         elif actions[x].name == 'TTS':
#             send_message = 'nothing here\r\n'
#             if actions[x].pos == 1:
#                 send_message = 'nothing here\r\n'
#             elif actions[x].pos == 2:
#                 send_message = 'something here\r\n'
#             elif actions[x].pos == 3:
#                 send_message = 'you are not nice\r\n'
#             elif actions[x].pos == 4:
#                 send_message = 'hello friend\r\n'
#             elif actions[x].pos == 4:
#                 send_message = 'kill humans\r\n'
#             elif actions[x].pos == 4:
#                 send_message = 'I do not like you\r\n'
#             s_2.send(send_message.encode('ascii'))
#             actions[x].animate()
#         elif actions[x].name == 'STT':
#             actions[x].animate()
#     posx = 25
#     posy = 25
#     for x in range(len(actions)):
#         if posx < 700:
#             canvas.create_image(posx, posy, image=actions[x].icon)
#             posx += 55
#         else:
#             posy += 55
#             posx = 25
#             canvas.create_image(posx, posy, image=actions[x].icon)
#             posx += 55
#
#
# # Function to delete all actions and reset canvas
# def del_all():
#     global xpos, ypos, actions
#     canvas.delete('all')
#     xpos = 0
#     ypos = 0
#     actions = []
#
#
# # Function to add actions
# def add_to_actions(action):
#     if action == 'Move':
#         actions.append(Action('Move', icons, 1))
#         actions_inv.append(Action('Move', icons, 0))
#     elif action == 'Turn':
#         actions.append(Action('Turn', icons, 1))
#         actions_inv.append(Action('Turn', icons, 0))
#
#
# # Class to represent an action to be run
# class Action:
#     def __init__(self, name, icon, show):
#         global xpos, ypos, stt_thread, actions
#         self.name = name
#         self.icon = icon
#         if show:
#             if xpos < 700:
#                 canvas.create_image(25 + xpos, 25 + ypos, image=self.icon)
#             else:
#                 ypos += 55
#                 xpos = 0
#                 canvas.create_image(25 + xpos, 25 + ypos, image=self.icon)
#             xpos += 55
#         self.time = 2
#         self.pos = 0
#         self.settings_tk = ''
#         self.animate_tk = ''
#         self.who = ''
#
#     # Animation function!
#     def animate(self):
#         canvas.delete('all')
#         if self.name == 'STT':
#             self.time = 1000
#             send_stt()
#             del_all()
#         rect = []
#         if self.name != 'STT':
#             canvas.create_text(100, 130, text=self.name + ' : ' + str(self.time) + ' seconds', fill='white')
#         else:
#             canvas.create_text(100, 130, text=self.name, fill='white')
#         if self.pos == 0:
#             canvas.create_text(100, 150, text='Waiting...', fill='white')
#         else:
#             canvas.create_text(100, 150, text='Position : ' + str(self.pos), fill='white')
#         if self.name != 'STT':
#             for x in range(self.time):
#                 rect.append(canvas.create_image(25 + 55 * x, 200, image=self.icon))
#         if self.who == 'andy':
#             for x in range(self.time):
#                 time.sleep(1)
#                 canvas.update()
#                 if self.name != 'STT':
#                     canvas.delete(rect[self.time - x - 1])
#         elif self.who == 'button':
#             for x in range(self.time):
#                 canvas.update()
#                 if self.name != 'STT':
#                     canvas.delete(rect[self.time - x - 1])
#                 time.sleep(1)
#         canvas.delete('all')
#
#     # Function to edit settings or remove instance
#     def open_settings(self):
#         def save_val():
#             self.time = time_scale.get()
#             if self.name != 'Wait' and self.name != 'STT':
#                 self.pos = position.get()
#             if self.name == 'Move' or self.name == 'Turn':
#                 actions_inv[len(actions)-1].pos = 3-self.pos
#             self.settings_tk.destroy()
#
#         self.settings_tk = Tk()
#         self.settings_tk.title('Settings')
#         label1 = Label(self.settings_tk, text='Time (S)')
#         label1.pack()
#         time_scale = Scale(self.settings_tk, from_=1, to=10, orient=HORIZONTAL)
#         time_scale.set(self.time)
#         time_scale.pack()
#         if self.name == 'Head Tilt':
#             label1 = Label(self.settings_tk, text='Head Tilt Position (Top to Bottom)')
#             position = Scale(self.settings_tk, from_=1, to=4, orient=HORIZONTAL)
#         elif self.name == 'Head Rotate':
#             label1 = Label(self.settings_tk, text='Head Rotate Position (Left to Right)')
#             position = Scale(self.settings_tk, from_=1, to=4, orient=HORIZONTAL)
#         elif self.name == 'Turn':
#             label1 = Label(self.settings_tk, text='Turning Direction (Left or Right)')
#             position = Scale(self.settings_tk, from_=1, to=2, orient=HORIZONTAL)
#         elif self.name == 'Move':
#             label1 = Label(self.settings_tk, text='Movement Direction (Foreword or Backward)')
#             position = Scale(self.settings_tk, from_=1, to=2, orient=HORIZONTAL)
#         elif self.name == 'Body Rotate':
#             label1 = Label(self.settings_tk, text='Body Rotate Position (Left to Right)')
#             position = Scale(self.settings_tk, from_=1, to=2, orient=HORIZONTAL)
#         elif self.name == 'TTS':
#             label1 = Label(self.settings_tk, text='Text to Say')
#             position = Scale(self.settings_tk, from_=1, to=6, orient=HORIZONTAL)
#         if self.name != 'Wait' and self.name != 'STT':
#             position.set(self.pos)
#             position.pack()
#         label1.pack()
#         save_values = Button(self.settings_tk, text='Save Values', command=save_val)
#         save_values.pack()
#         delete = Button(self.settings_tk, text='Delete', command=self.__delete__)
#         delete.pack()
#         self.settings_tk.mainloop()
#
#     def __delete__(self):
#         global xpos, actions
#         self.time = 0
#         self.pos = 0
#         canvas.delete('all')
#         xpos -= 55
#         posx = 25
#         posy = 25
#         actions.remove(self)
#         self.settings_tk.destroy()
#         for x in range(len(actions)):
#             if posx < 700:
#                 canvas.create_image(posx, posy, image=actions[x].icon)
#                 posx += 55
#             else:
#                 posy += 55
#                 posx = 25
#                 canvas.create_image(posx, posy, image=actions[x].icon)
#                 posx += 55
#
#
# # Mouse movement class
# class MouseMovement:
#     def __init__(self):
#         self.flag = False
#
#     def mouse_pressed(self, event):
#         global actions
#         y = 0
#         for x in range(len(actions)):
#             if x == 13 * (y + 1):
#                 y += 1
#             if x * 55 + 50 - 715 * y > event.x > x * 55 - 715 * y and y * 55 < event.y < y * 55 + 50:
#                 self.flag = True
#                 actions[x].open_settings()
#
#     def mouse_release(self, event):
#         if self.flag:
#             self.flag = False
#
#
# # Mouse movement class instantiation
# m = MouseMovement()
#
# # Root's canvas
# canvas = Canvas(root, bg='#1F1F1F', width='750', height='443')
# canvas.pack(side=RIGHT)
# canvas.bind('<ButtonPress-1>', m.mouse_pressed)
# canvas.bind('<ButtonRelease-1>', m.mouse_release)
#
# # Root's buttons
# go = Button(root, height=1, width=5, text='GO!', bg='black', fg='white', command=lambda: run('button'))
# go.pack(side=TOP)
# ht = Button(root, command=lambda: actions.append(Action('Head Tilt', icons, 1)), image=icons, width=pic_size, height=pic_size)
# ht.pack(side=TOP)
# hr = Button(root, command=lambda: actions.append(Action('Head Rotate', icons, 1)), image=icons, width=pic_size, height=pic_size)
# hr.pack(side=TOP)
# move = Button(root, command=lambda: add_to_actions('Move'), image=icons, width=pic_size, height=pic_size)
# move.pack(side=TOP)
# turn = Button(root, command=lambda: add_to_actions('Turn'), image=icons, width=pic_size, height=pic_size)
# turn.pack(side=TOP)
# br = Button(root, command=lambda: actions.append(Action('Body Rotate', icons, 1)), image=icons, width=pic_size, height=pic_size)
# br.pack(side=TOP)
# wait = Button(root, command=lambda: actions.append(Action('Wait', icons, 1)), image=icons, width=pic_size, height=pic_size)
# wait.pack(side=TOP)
# stt_button = Button(root, command=lambda: actions.append(Action('STT', icons, 1)), image=icons, width=pic_size, height=pic_size)
# stt_button.pack(side=TOP)
# tts_button = Button(root, command=lambda: actions.append(Action('TTS', icons, 1)), image=icons, width=pic_size, height=pic_size)
# tts_button.pack(side=TOP)
# del_all_button = Button(root, height=1, width=5, text='Clear', bg='black', fg='white', command=del_all)
# del_all_button.pack(side=TOP)
# stt_button_2 = Button(root, height=1, width=5, text='STT', bg='black', fg='white', command=send_stt)
# stt_button_2.pack(side=TOP)

#
# # Main tk loop and geometry
# root.geometry('800x450')
# root.mainloop()
# os.system('xset r on')
