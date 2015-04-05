import pygame
from pygame.locals import *
import sys
import os
import time
import myo
from myo.lowlevel import pose_t, stream_emg
from myo.six import print_
import random

pygame.init()
myo.init()
background_colour = (255,255,255)
black = (0,0,0)
display_width = 800
display_height = 500
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Duck, Paper, Scissors')
screen.fill(background_colour)
clock = pygame.time.Clock()

def write_message(text, me, opponent):
    screen.fill(background_colour)
    largeText = pygame.font.Font('freesansbold.ttf',45)
    smallText = pygame.font.Font('freesansbold.ttf',30)
    smallerText = pygame.fond.Font('freesansbold.ttf', 20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextSurf2, TextRect2 = text_objects("Me: "+str(GAME.me)+", Opponent: " +str(GAME.opponent), smallText)
    TextSurf3, TextRect3 = text_objects("Duck, Paper, Scissors", largeText)
    TextSurf4, TextRect4 = text_objects("Exit: Rotate left", smallerText)
    TextRect.center = ((display_width/2),(display_height/2))
    TextRect2.center = ((display_width/2),(display_height/2 + 150))
    TextRect3.center = ((display_width/2),40)
    TextRect4.center = (30,display_height-20)
    screen.blit(TextSurf, TextRect)
    screen.blit(TextSurf2, TextRect2)
    screen.blit(TextSurf3, TextRect3)
    screen.blit(TextSurf4, TextRect4)
    pygame.display.update()
    clock.tick(15)

def text_objects(text, font):
    textSurface = font.render(text, 1, black)
    return textSurface, textSurface.get_rect()

SHOW_OUTPUT_CHANCE = 0.01
r"""
There can be a lot of output from certain data like acceleration and orientation.
This parameter controls the percent of times that data is shown.
"""
class State:
    def __init__(self):
        self.me = 0
        self.opponent = 0
        self.running=True
GAME=State()

class Listener(myo.DeviceListener):
    # return False from any method to stop the Hub

    def on_connect(self, myo, timestamp):
        print_("Connected to Myo")
        myo.vibrate('short')
        myo.request_rssi()

    def on_rssi(self, myo, timestamp, rssi):
        #print_("RSSI:", rssi)
        print_('');

    def on_event(self, event):
        r""" Called before any of the event callbacks. """

    def on_event_finished(self, event):
        r""" Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub. """

    def on_pair(self, myo, timestamp):
        print_('Paired')
        print_("If you don't see any responses to your movements, try re-running the program or making sure the Myo works with Myo Connect (from Thalmic Labs).")
        print_("Double tap enables EMG.")
        print_("Spreading fingers disables EMG.\n")

    def on_disconnect(self, myo, timestamp):
        print_('on_disconnect')

    def on_pose(self, myo, timestamp, pose):
        if pose == pose_t.wave_in:
            #print_('on_pose', pose)
            print_("You chose Scissors!")
            opponentChoice(1,myo)
            myo.set_stream_emg(stream_emg.disabled)
        elif pose == pose_t.fingers_spread:
            #print_('on_pose', pose)
            print_("You chose Paper!")
            opponentChoice(2,myo)
            myo.set_stream_emg(stream_emg.disabled)
        elif pose == pose_t.fist:
            #print_('on_pose', pose)
            print_("You chose Rock!")
            opponentChoice(3,myo)
            myo.set_stream_emg(stream_emg.disabled)
        
    def on_orientation_data(self, myo, timestamp, orientation):
        show_output('orientation', orientation)

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        show_output('acceleration', acceleration)

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        if gyroscope[0]>80:
            GAME.running=False
        show_output('gyroscope', gyroscope)

    def on_unlock(self, myo, timestamp):
        print_('unlocked')

    def on_lock(self, myo, timestamp):
        print_('locked')

    def on_sync(self, myo, timestamp, arm, x_direction):
        print_('synced', arm, x_direction)

    def on_unsync(self, myo, timestamp):
        print_('unsynced')
        
    def on_emg(self, myo, timestamp, emg):
        show_output('emg', emg)

c_scissors = pygame.image.load("assets/computer_scissors.jpg")
c_scissors = pygame.transform.scale(c_scissors, (200, 200))
c_paper = pygame.image.load("assets/computer_paper.jpg")
c_paper = pygame.transform.scale(c_paper, (200, 200))
c_rock = pygame.image.load("assets/computer_rock.jpg")
c_rock = pygame.transform.scale(c_rock, (200, 200))
scissors = pygame.image.load("assets/human_scissors.png")
scissors = pygame.transform.scale(scissors, (150, 150))
paper = pygame.image.load("assets/human_paper.png")
paper = pygame.transform.scale(paper, (150, 150))
rock = pygame.image.load("assets/human_rock.png")
rock = pygame.transform.scale(rock, (150, 150))

def print_paper(x,y):
    screen.blit(paper, (x,y))
    pygame.display.update()
def print_scissors(x,y):
    screen.blit(scissors, (x,y))
    pygame.display.update()
def print_rock(x,y):
    screen.blit(rock, (x,y))
    pygame.display.update()
def print_c_paper(x,y):
    screen.blit(c_paper, (x,y))
    pygame.display.update()
def print_c_scissors(x,y):
    screen.blit(c_scissors, (x,y))
    pygame.display.update()
def print_c_rock(x,y):
    screen.blit(c_rock, (x,y))
    pygame.display.update()
def opponentChoice(userChoice,myo):
    choice=random.randint(1,3)
    if choice==1:
        print_("Opponent chose Scissors!")
        if choice==userChoice:
            write_message("Tie!", GAME.me, GAME.opponent)
            print_c_scissors(display_width-250, 150)
            print_scissors(75, 150)
        elif 2==userChoice:
            GAME.opponent+=1
            write_message("You Lose!", GAME.me, GAME.opponent)
            print_c_scissors(display_width-250, 150)
            print_paper(75, 150)
            myo.vibrate('long')
        else:
            GAME.me+=1
            write_message("You Win!", GAME.me, GAME.opponent)
            print_c_scissors(display_width-250, 150)
            print_rock(75, 150)
    elif choice==2:
        print_("Opponent chose Paper!")
        if choice==userChoice:
            write_message("Tie!", GAME.me, GAME.opponent)
            print_c_paper(display_width-250, 150)
            print_paper(75, 150)
        elif 1==userChoice:
            GAME.me+=1
            write_message("You Win!", GAME.me, GAME.opponent)
            print_c_paper(display_width-250, 150)
            print_scissors(75, 150)
        else:
            GAME.opponent+=1
            write_message("You Lose!", GAME.me, GAME.opponent)
            print_c_paper(display_width-250, 150)
            print_rock(75, 150)
            myo.vibrate('long')
    else:
        print_("Opoonent chose Rock!")
        if choice==userChoice:
            write_message("Tie!", GAME.me, GAME.opponent)
            print_c_rock(display_width-250, 150)
            print_rock(75, 150)
        elif 2==userChoice:
            GAME.me+=1
            write_message("You Win!", GAME.me, GAME.opponent)
            print_c_rock(display_width-250, 150)
            print_paper(75, 150)
        else:
            GAME.opponent+=1
            write_message("You Lose!", GAME.me, GAME.opponent)
            print_c_rock(display_width-250, 150)
            print_scissors(75, 150)
            myo.vibrate('long')

def show_output(message, data):
    '''if random.random() < SHOW_OUTPUT_CHANCE: 
        print_(message + ':' + str(data))'''

hub = myo.Hub()
hub.set_locking_policy(myo.locking_policy.none)
hub.run(3000, Listener())


def game_loop():
    while GAME.running:
        for event in pygame.event.get():
            if event.type == QUIT:
                GAME.running = False 
        pygame.display.update()
        clock.tick(60)


game_loop()
pygame.quit()
hub.stop(True)
quit()
