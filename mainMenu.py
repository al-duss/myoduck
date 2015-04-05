import pygame
from pygame.locals import *
import sys
import os
import myo
from myo.lowlevel import pose_t, stream_emg
from myo.six import print_

pygame.init()
myo.init()
background_colour = (255,255,255)
display_width = 800
display_height = 500
black = (0,0,0)

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('The Myo Ducks')
screen.fill(background_colour)
clock = pygame.time.Clock()

def text_objects(text, font):
	textSurface = font.render(text, 1, black)
	return textSurface, textSurface.get_rect()
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
   #  	if pose == pose_t.wave_in:
			# os.system("python myoDucks.py") 
			print_('')     	
               
    def on_orientation_data(self, myo, timestamp, orientation):
        show_output('orientation', orientation)

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        show_output('acceleration', acceleration)

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
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

def show_output(message, data):
    '''if random.random() < 0.1: 
        print_(message + ':' + str(data))'''
hub = myo.Hub()
hub.set_locking_policy(myo.locking_policy.none)
hub.run(500, Listener())
def game_intro():

	intro = True
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_k:
					os.system("python GUI-2.py")
				if event.key == pygame.K_m:

					os.system("python myoDucks.py")
				if event.key == pygame.K_d:
					os.system("python rockPaperScissors.py")

		screen.fill(background_colour)
		largeText = pygame.font.Font('freesansbold.ttf',45)
		smallText = pygame.font.Font('freesansbold.ttf',30)
		TextSurf, TextRect = text_objects("The Myo Ducks", largeText)
		TextSurf2, TextRect2 = text_objects("Ducky Strikes Back: Press M for Myo, K for Keyboard", smallText)
		TextSurf3, TextRect3 = text_objects("Duck, Paper Scissors: Press D", smallText)
		TextRect.center = ((display_width/2),40)
		TextRect2.center = ((display_width/2),(display_height/2 + 100))
		TextRect3.center = ((display_width/2),(display_height/2 + 150))
		duck = pygame.image.load("assets/duck.png")
		duck = pygame.transform.scale(duck, (150, 150))
		screen.blit(duck, ((display_width/2-80),150))
		screen.blit(TextSurf, TextRect)
		screen.blit(TextSurf2, TextRect2)
		screen.blit(TextSurf3, TextRect3)
		pygame.display.update()
		clock.tick(15)

game_intro()
hub.stop(True)
pygame.quit()
quit()