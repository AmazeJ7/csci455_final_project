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
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
temp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
temp_s.connect(('10.255.255.255', 1))
host = temp_s.getsockname()
temp_s.close()
print(str(host[0]))
sock.bind((str(host[0]), port))
sock.listen(5)


# Function to initiate the socket
def init_socket():
    while True:
        global s_2
        print('Listening')
        s_2, ip = sock.accept()
        print('Got a connection from %s' % str(ip))
        board.start()
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
        elif msg_parts[0] == 'North':
            board.move('n')
        elif msg_parts[0] == 'East':
            board.move('e')
        elif msg_parts[0] == 'South':
            board.move('s')
        elif msg_parts[0] == 'West':
            board.move('w')
        elif msg_parts[0] == 'fight':
            board.fight()
        elif msg_parts[0] == 'run':
            board.run()
        elif msg_parts[0] == 'Tango':
            board.dance_win()
        elif msg_parts[0] == 'end':
            board.end()
        else:
            print('Try again')
            send_stt()


# Function to move foreword
def move():
    controller.setTarget(1, 5000)
    time.sleep(2)
    controller.setTarget(1, 6000)


# Function to turn
def turn(d):
    if d == 'l':
        controller.setTarget(2, 7000)
        time.sleep(2)
        controller.setTarget(2, 6000)
    elif d == 'r':
        controller.setTarget(2, 5000)
        time.sleep(2)
        controller.setTarget(2, 6000)


# Class to represent the board
class Board:
    def __init__(self):
        self.map = []
        self.temp_map = []
        for i in [self.map, self.temp_map]:
            i.append(Location(1, 0, 1, 0, 0))
            i.append(Location(2, 0, 1, 1, 1))
            i.append(Location(3, 0, 0, 1, 1))
            i.append(Location(4, 0, 1, 0, 0))
            i.append(Location(5, 0, 0, 1, 1))
            i.append(Location(6, 0, 1, 1, 0))
            i.append(Location(7, 1, 0, 1, 1))
            i.append(Location(8, 1, 0, 0, 0))
            i.append(Location(9, 0, 1, 1, 0))
            i.append(Location(10, 1, 0, 1, 1))
            i.append(Location(11, 1, 0, 1, 0))
            i.append(Location(12, 1, 1, 0, 0))
            i.append(Location(13, 0, 1, 0, 1))
            i.append(Location(14, 1, 0, 1, 1))
            i.append(Location(15, 1, 0, 1, 0))
            i.append(Location(16, 1, 1, 0, 0))
            i.append(Location(17, 0, 0, 1, 1))
            i.append(Location(18, 0, 0, 1, 0))
            i.append(Location(19, 1, 1, 1, 0))
            i.append(Location(20, 1, 0, 0, 1))
            i.append(Location(21, 0, 1, 0, 0))
            i.append(Location(22, 1, 1, 0, 1))
            i.append(Location(23, 1, 0, 0, 1))
            i.append(Location(24, 1, 1, 0, 0))
            i.append(Location(25, 0, 0, 0, 1))
        # Nodes
        self.end = Location
        self.pos = Location
        self.charging_stations = []
        self.coffee_shops = []
        self.eb = []
        self.mb = []
        self.hb = []
        self.db = []
        # Fight Stats
        self.hp = 25
        self.e_hp = 0
        self.dance_index = 0

    # Function to print out the board
    def print_board(self):
        for i in range(5):
            for j in range(5):
                self.map[i * 5 + j].print_top()
            print()
            for j in range(5):
                self.map[i * 5 + j].print_mid()
            print()
            for j in range(5):
                self.map[i * 5 + j].print_bot()
            print()

    # Function to initialize the board and locations
    def start(self):
        # Start and end positions
        items = [1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25]
        random.shuffle(items)
        for i in self.map:
            if items[0] == i.num:
                i.type = 'ST'
                self.pos = i
                self.temp_map.pop(i.num - 1)
        if 0 < items[0] < 6:
            self.end = self.map[random.randint(20, 24)]
            self.pos.facing = 's'
        elif items[0] == 6 or items[0] == 11 or items[0] == 16:
            locations = [self.map[9], self.map[14], self.map[19]]
            random.shuffle(locations)
            self.end = locations[0]
            self.pos.facing = 'e'
        elif items[0] == 10 or items[0] == 15 or items[0] == 20:
            locations = [self.map[5], self.map[10], self.map[15]]
            random.shuffle(locations)
            self.end = locations[0]
            self.pos.facing = 'w'
        elif 20 < items[0] < 26:
            self.end = self.map[random.randint(0, 4)]
            self.pos.facing = 'n'
        self.end.type = 'TE'
        if self.pos.num > self.end.num:
            self.temp_map.pop(self.end.num - 1)
        else:
            self.temp_map.pop(self.end.num - 2)
        # Charging stations
        for i in range(3):
            random.shuffle(self.temp_map)
            self.charging_stations.append(self.map[self.temp_map[0].num - 1])
            self.temp_map.pop(0)
            self.charging_stations[i].type = 'CH'
        # Coffee shops
        for i in range(3):
            random.shuffle(self.temp_map)
            self.coffee_shops.append(self.map[self.temp_map[0].num - 1])
            self.temp_map.pop(0)
            self.coffee_shops[i].type = 'CO'
        # Easy battles
        for i in range(6):
            random.shuffle(self.temp_map)
            self.eb.append(self.map[self.temp_map[0].num - 1])
            self.temp_map.pop(0)
            self.eb[i].type = 'EB'
        # Medium battles
        for i in range(5):
            random.shuffle(self.temp_map)
            self.mb.append(self.map[self.temp_map[0].num - 1])
            self.temp_map.pop(0)
            self.mb[i].type = 'MB'
        # Hard battles
        for i in range(3):
            random.shuffle(self.temp_map)
            self.hb.append(self.map[self.temp_map[0].num - 1])
            self.temp_map.pop(0)
            self.hb[i].type = 'HB'
        # Dance Battles
        for i in range(3):
            random.shuffle(self.temp_map)
            self.db.append(self.map[self.temp_map[0].num - 1])
            self.temp_map.pop(0)
            self.db[i].type = 'DB'

        board.print_board()
        board.ask_dir()

    # Function to move the board location and robot
    def move(self, s):
        cont = 1
        if s == 'n' and self.pos.n:
            self.animate('n')
            self.pos = self.map[self.pos.num - 6]
            self.pos.facing = 'n'
        elif s == 'e' and self.pos.e:
            self.animate('e')
            self.pos = self.map[self.pos.num]
            self.pos.facing = 'e'
        elif s == 's' and self.pos.s:
            self.animate('s')
            self.pos = self.map[self.pos.num + 4]
            self.pos.facing = 's'
        elif s == 'w' and self.pos.w:
            self.animate('w')
            self.pos = self.map[self.pos.num - 2]
            self.pos.facing = 'w'
        else:
            print('\nThere is a mountain in the way. Try again')
            self.animate('no')
            cont = 0
            send_stt()
        if cont:
            if self.pos.type == 'EB':
                board.enter_battle(random.randint(3, 6))
            elif self.pos.type == 'MB':
                board.enter_battle(random.randint(7, 9))
            elif self.pos.type == 'HB':
                board.enter_battle(random.randint(10, 12))
            elif self.pos.type == 'CO':
                if self.end.num > self.pos.num:
                    print('\nThe end is to the south or east...')
                elif self.end.num < self.pos.num:
                    print('\nThe end is to the north or west...')
                board.ask_dir()
            elif self.pos.type == 'CH':
                self.hp = 25
                print('\nHealth Replenished')
                board.ask_dir()
            elif self.pos.type == 'DB':
                board.dance_battle()
            elif self.pos.type == 'TE':
                print('YOU WIN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                sock.close()

    # Function to ask the user for directions
    def ask_dir(self):
        text = '\nSelect one:'
        if self.pos.n:
            text += '\nNorth'
        if self.pos.e:
            text += '\nEast'
        if self.pos.s:
            text += '\nSouth'
        if self.pos.w:
            text += '\nWest'
        print(text)
        send_stt()

    # Function to enter battle with enemies
    def enter_battle(self, bad_guys):
        if self.e_hp == 0:
            self.e_hp = bad_guys
        print('\n' + str(self.e_hp) + ' bad guys showed up!\nFight or run?')
        send_stt()

    # Function to enter battle with dancers
    def dance_battle(self):
        prompts = ['Salsa', 'Tango', 'Merengue']
        print('\nDancers showed up using the ' + prompts[self.dance_index])
        self.dance_index = self.dance_index + 1
        print('What dance will you use to defeat them?')
        send_stt()

    # Function to represent a dance off win
    def dance_win(self):
        print('You won the dance off')
        board.ask_dir()

    # Function to run away from enemies
    def run(self):
        time.sleep(1)
        if random.randint(0, 3) != 0:
            locations = ['n', 'e', 's', 'w']
            random.shuffle(locations)
            for i in range(len(locations)):
                if locations[i] == 'n' and self.pos.n:
                    self.pos = self.map[self.pos.num - 6]
                elif locations[i] == 'e' and self.pos.e:
                    self.pos = self.map[self.pos.num]
                elif locations[i] == 's' and self.pos.s:
                    self.pos = self.map[self.pos.num + 4]
                elif locations[i] == 'w' and self.pos.w:
                    self.pos = self.map[self.pos.num - 2]
            board.ask_dir()
        else:
            print('Run failed :(')
            self.hp = self.hp - random.randint(2, 4)
            if self.hp <= 0:
                print('You died a tragic death')
                sock.close()
            send_stt()

    # Function to fight enemies
    def fight(self):
        cont = 0
        self.e_hp = self.e_hp - random.randint(1, 3)
        self.hp = self.hp - random.randint(2, 4)
        controller.setTarget(0, 5000)
        controller.setTarget(3, 5000)
        controller.setTarget(4, 5000)
        time.sleep(1)
        controller.setTarget(0, 5000)
        controller.setTarget(3, 7000)
        controller.setTarget(4, 7000)
        time.sleep(1)
        controller.setTarget(0, 5000)
        controller.setTarget(3, 6000)
        controller.setTarget(4, 6000)
        if self.e_hp <= 0:
            print('You won the fight')
            board.ask_dir()
        elif self.hp <= 0:
            print('You died a tragic death')
            sock.close()
        else:
            cont = 1
        if cont:
            print('Enemy health:' + str(self.e_hp) + ' Your health: ' + str(self.hp))
            if self.e_hp <= 0:
                print('You won the fight')
                board.ask_dir()
            elif self.hp <= 0:
                print('You died a tragic death')
            else:
                print('Fight or run?')
                send_stt()

    # Function to animate movement
    def animate(self, s):
        if s == 'n':
            if self.pos.facing == 'n':
                move()
            elif self.pos.facing == 'e':
                turn('l')
                move()
            elif self.pos.facing == 's':
                turn('l')
                turn('l')
                move()
            elif self.pos.facing == 'w':
                turn('r')
                move()
        elif s == 'e':
            if self.pos.facing == 'n':
                turn('r')
                move()
            elif self.pos.facing == 'e':
                move()
            elif self.pos.facing == 's':
                turn('l')
                move()
            elif self.pos.facing == 'w':
                turn('r')
                turn('r')
                move()
        elif s == 's':
            if self.pos.facing == 'n':
                turn('r')
                turn('r')
                move()
            elif self.pos.facing == 'e':
                turn('r')
                move()
            elif self.pos.facing == 's':
                move()
            elif self.pos.facing == 'w':
                turn('l')
                move()
        elif s == 'w':
            if self.pos.facing == 'n':
                turn('l')
                move()
            elif self.pos.facing == 'e':
                turn('l')
                turn('l')
                move()
            elif self.pos.facing == 's':
                turn('r')
                move()
            elif self.pos.facing == 'w':
                move()
        elif s == 'no':
            controller.setTarget(3, 4000)
            time.sleep(1)
            controller.setTarget(3, 8000)
            time.sleep(1)
            controller.setTarget(3, 6000)

    # Function to close out the sockets
    def end(self):
        print("Bye")
        sock.close()


# Class to hold locations on the map
class Location:
    def __init__(self, num, n, e, s, w):
        self.num = num
        self.facing = ''
        self.n = n
        self.e = e
        self.s = s
        self.w = w
        self.type = str(self.num)

    # Function to print out the top row of a location
    def print_top(self):
        if self.n:
            print('   |  ', end='')
        else:
            print('      ', end='')

    # Function to print out the middle row of a location
    def print_mid(self):
        if self.w:
            print('--' + str(self.type), end='')
        else:
            print('  ' + str(self.type), end='')
        if self.e:
            print('--', end='')
        else:
            print('  ', end='')

    # Function to print out the bottom row of a location
    def print_bot(self):
        if self.s:
            print('   |  ', end='')
        else:
            print('      ', end='')


# Board init
board = Board()

# Socket thread init
init_socket_thread = threading.Thread(target=init_socket)
init_socket_thread.start()

os.system('xset r on')
