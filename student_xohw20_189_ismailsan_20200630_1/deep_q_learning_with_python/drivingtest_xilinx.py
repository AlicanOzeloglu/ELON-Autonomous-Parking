import pygame, time, sys
from pygame.locals import *
import math 
from numpy import asarray
from numpy import save
from numpy import load
import random
import pygame, time
import math 
import random
import numpy as np
import os
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import Adam
from collections import deque
from numpy import asarray
from numpy import save
from numpy import load
from keras.utils import normalize,np_utils
import timeit

PI = 3.1415 
WINDOWWIDTH = 1600
WINDOWHEIGHT = 1000
RED =   (255, 0,  0)
GREEN = (0,  255, 0)
BLUE =  (0,   0, 255)
WHITE   = (255, 255, 255)
BLACK =   (0, 0, 0)
parking_area_width = 100
pygame.init()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
car_speed = 10
angle = 100
sensor_range = 100
saved = False
action = 0
action_size = 4
state_size = 3
LEARNING_RATE= 0.001
reborn = [[90,1260,700], [90,1270,700], [90,1250,700], [90,1240,700], [90,1220,600], [90,1270,600],[90, 1250,500],[145, 1250, 400],[-180, 1250, 400],[180, 1100,400],[-180, 1100,410],[-180,1100,360],[-180,920,400],[-180,920,360],[-180,920,410]]
X = []
y = []
count = 0
a = 250
def environment1():   
	pygame.display.set_caption('CAR SIMULATION')
	BasicFont = pygame.font.Font('freesansbold.ttf', 20)  
	pygame.draw.line(screen, BLACK, (1400, 340), (1400, 800), 20)	#up
	pygame.draw.line(screen, BLACK, (1400, 340), (442, 340), 20)	#side
	pygame.draw.line(screen, BLACK, (1208, 800), (1208, 562), 20)
	pygame.draw.line(screen, BLACK, (442, 532), (442, 340), 20)
	pygame.draw.line(screen, BLACK, (442, 532), (562, 532), 20)
	pygame.draw.line(screen, BLACK, (552, 522), (587, 567), 20)
	pygame.draw.line(screen, BLACK, (587, 567), (587, 767), 20)
	pygame.draw.line(screen, BLACK, (587, 767), (744, 767), 20)
	pygame.draw.line(screen, BLACK, (744, 767), (744, 567), 20)
	pygame.draw.line(screen, BLACK, (743, 567), (779, 517), 20)
	pygame.draw.line(screen, BLACK, (769, 527), (812, 527), 20)
	pygame.draw.line(screen, BLACK, (552 + a, 522), (587+ a, 567), 20)
	pygame.draw.line(screen, BLACK, (587+ a, 567), (587+ a, 767), 20)
	pygame.draw.line(screen, BLACK, (587+ a, 767), (744+ a, 767), 20)
	pygame.draw.line(screen, BLACK, (744+ a, 767), (744+ a, 567), 20)
	pygame.draw.line(screen, BLACK, (743+ a, 567), (779+ a, 517), 20)
	pygame.draw.line(screen, BLACK, (769+ a, 527), (802+ a, 527), 20)
	pygame.draw.line(screen, BLACK, (802+ a, 527), (1178, 527), 20)
	pygame.draw.line(screen, BLACK, (1168, 517), (1208, 562), 20)
	pygame.draw.line(screen, BLACK, (5, 5), (1500,5), 80)
	pygame.draw.line(screen, BLACK, (1500, 5), (1500,900), 80)
	pygame.draw.line(screen, BLACK, (1500,900), (5,900), 80)
	pygame.draw.line(screen, BLACK, (5,900), (5,5), 60)
	pygame.draw.rect(screen,BLACK,(1300,1340,430,400))

def parking_area1():
	image = pygame.image.load("car_image.jpeg")
	rect = image.get_rect()
	image = pygame.transform.scale(image, (122, 85))
	rect.x,rect.y = (870,600)
	image = pygame.transform.rotate(image, -90)
	screen.blit(image,rect)

def parking_area2():
	image = pygame.image.load("car_image.jpeg")
	rect = image.get_rect()
	image = pygame.transform.scale(image, (122, 85))
	rect.x,rect.y = (620,600)
	image = pygame.transform.rotate(image, -90)
	screen.blit(image,rect)


def environment2():   
	pygame.display.set_caption('CAR SIMULATION')
	BasicFont = pygame.font.Font('freesansbold.ttf', 20)  
	pygame.draw.line(screen, BLACK, (5, 5), (1500,5), 80)
	pygame.draw.line(screen, BLACK, (1500, 5), (1500,780), 80)
	pygame.draw.line(screen, BLACK, (1500,780), (250,780), 80)
	pygame.draw.line(screen, BLACK, (250,780), (250,5), 60)
	pygame.draw.line(screen, BLACK, (470, 230), (1230,230), 30)
	pygame.draw.line(screen, BLACK, (1200,230), (1200,570), 60)
	pygame.draw.line(screen, BLACK, (1200,550), (470,550), 30)
	pygame.draw.line(screen, BLACK, (500,550), (500, 230), 60)
	
def distance(x_current, y_current, x_target, y_target):
	return math.sqrt(math.pow((x_current-x_target),2) + math.pow((y_current-y_target),2))

pygame.key.set_repeat(40, 40)   
screen_rect = screen.get_rect()
image_orig = pygame.image.load("car_image.jpeg").convert()
image_orig = pygame.transform.scale(image_orig, (122, 85))
image = image_orig.copy()
agent = image_orig.get_rect(center=screen_rect.center)
agent.left = 1260
agent.top = 700
angle = 90
i = 0

def degtorad(derece):
	return ((derece * 2 * PI) / 360)  

def rear_sensor():
	a, b = agent.center
	angle_arka = angle + 180
	if(0 <= angle_arka <= 90):
		b -= int(math.sin(degtorad(abs(angle_arka))) * 85)
		a += int(math.cos(degtorad(abs(angle_arka))) * 85)
	elif(90 <= angle_arka <= 180):
		b -= int(math.sin(degtorad(abs(angle_arka))) * 85)
		a += int(math.cos(degtorad(abs(angle_arka))) * 85)
	elif(270 >= angle_arka >= 180):
		b -= int(math.sin(degtorad(180 - (angle_arka))) * 85)
		a -= int(math.cos(degtorad(180 - (angle_arka))) * 85)
	elif(360 >= angle_arka >= 270):
		b -= int(math.sin(degtorad(180 - (angle_arka))) * 85)
		a -= int(math.cos(degtorad(180 - (angle_arka))) * 85)
	
	x2,y2 = a,b
	for i in range(sensor_range):
		reference = (a,b)
		if (screen.get_at(reference) != (255, 255, 255, 255)):
			intersect = reference 
			break      
		else:
			if(0 <= angle_arka <= 90):
				b -= int(math.sin(degtorad(abs(angle_arka))) * 10)
				a += int(math.cos(degtorad(abs(angle_arka))) * 10)
			elif(90 <= angle_arka <= 180):
				b -= int(math.sin(degtorad(abs(angle_arka))) * 10)
				a += int(math.cos(degtorad(abs(angle_arka))) * 10)
			elif(270 >= angle_arka >= 180):
				b -= int(math.sin(degtorad(180 - (angle_arka))) * 10)
				a -= int(math.cos(degtorad(180 - (angle_arka))) * 10)
			elif(360 >= angle_arka >= 270):
				b -= int(math.sin(degtorad(180 - (angle_arka))) * 10)
				a -= int(math.cos(degtorad(180 - (angle_arka))) * 10)

	x1,y1 = reference
	pygame.draw.line(screen, BLACK, (x2,y2), (x1,y1), 2)  
	mesafe = math.sqrt(math.pow((x1-x2),2) + math.pow((y1 - y2),2))
	if mesafe < 0:
		mesafe = 0
	return round (mesafe, 5)

def rear_right_sensor():
	angle_sagarka = 45 + angle
	a, b = agent.center
	if(27 >= 27 + angle >= -63):
		b += int(math.sin(degtorad((27 + angle))) * 61.7)
		a -= int(math.cos(degtorad((27 + angle))) * 61.7)
	elif(-63 >= 27 + angle >= -153):
		b -= int(math.sin(degtorad(abs(27 + angle))) * 61.7)
		a -= int(math.cos(degtorad(abs(27 + angle))) * 61.7)
	elif(117 <= (27 + angle) <= 207):
		b += int(math.sin(degtorad(abs(27 + angle))) * 61.7)
		a -= int(math.cos(degtorad(abs(27 + angle))) * 61.7)
	elif(27 <= (27 + angle) <= 117):
		b += int(math.sin(degtorad(180 - abs(27 + angle))) * 61.7)
		a += int(math.cos(degtorad(180 - abs(27 + angle))) * 61.7)
	
	x2,y2 = a,b
	for i in range(sensor_range):
		reference = (a,b)
		if (screen.get_at(reference) != (255, 255, 255, 255)):
			intersect = reference 
			break      
		else:
			if(27 >= angle_sagarka >= -63):
				b += int(math.sin(degtorad((angle_sagarka))) * 10)
				a -= int(math.cos(degtorad((angle_sagarka))) * 10)
			elif(-63 >= angle_sagarka >= -153):
				b -= int(math.sin(degtorad(abs(angle_sagarka))) * 10)
				a -= int(math.cos(degtorad(abs(angle_sagarka))) * 10)
			elif(117 <= angle_sagarka <= 230):
				b += int(math.sin(degtorad(abs(angle_sagarka))) * 10)
				a -= int(math.cos(degtorad(abs(angle_sagarka))) * 10)
			elif(27 <= (angle_sagarka) <= 117):
				b += int(math.sin(degtorad(180 - abs(angle_sagarka))) * 10)
				a += int(math.cos(degtorad(180 - abs(angle_sagarka))) * 10)
	x1,y1 = reference
	pygame.draw.line(screen, BLACK, (x2,y2), (x1,y1), 2) 
	mesafe = math.sqrt(math.pow((x1-x2),2) + math.pow((y1-y2),2))
	if(mesafe < 0):
		mesafe = 0
	return round (mesafe, 5)

def rear_left_sensor():
	angle_solarka = 45 - angle
	a, b = agent.center
	if(0 <= (27 - angle) <= 117):
		b -= int(math.sin(degtorad(abs(27 - angle))) * 61.7)
		a -= int(math.cos(degtorad(abs(27 - angle))) * 61.7)
	elif(117 <= (27 - angle) <= 207):
		b -= int(math.sin(degtorad(abs(27 - angle))) * 61.7)
		a -= int(math.cos(degtorad(abs(27 - angle))) * 61.7)
	elif(-63 >= 27 - angle >= -153):
		b += int(math.sin(degtorad(abs(27 - angle))) * 61.7)
		a -= int(math.cos(degtorad(abs(27 - angle))) * 61.7)
	elif(27 >= (27 - angle) >= -63):
		b += int(math.sin(degtorad(180 - abs(27 - angle))) * 61.7)
		a += int(math.cos(degtorad(180 - abs(27 - angle))) * 61.7)
	
	x2,y2 = a,b
	for i in range(sensor_range):
		reference = (a,b)
		if (screen.get_at(reference) != (255, 255, 255, 255)):
			intersect = reference 
			break      
		else:
			if(0 <= angle_solarka <= 117):
				b -= int(math.sin(degtorad(abs(angle_solarka))) * 10)
				a -= int(math.cos(degtorad(abs(angle_solarka))) * 10)
			elif(117 <= angle_solarka <= 230):
				b -= int(math.sin(degtorad(abs(angle_solarka))) * 10)
				a -= int(math.cos(degtorad(abs(angle_solarka))) * 10)
			elif(-63 >= angle_solarka >= -153):
				b += int(math.sin(degtorad(abs(angle_solarka))) * 10)
				a -= int(math.cos(degtorad(abs(angle_solarka))) * 10)
			elif(27 >= angle_solarka >= -63):
				b += int(math.sin(degtorad(180 - abs(angle_solarka))) * 10)
				a += int(math.cos(degtorad(180 - abs(angle_solarka))) * 10)
	x1,y1 = reference
	pygame.draw.line(screen, BLACK, (x2,y2), (x1,y1), 2) 
	mesafe = math.sqrt(math.pow((x1-x2),2) + math.pow((y1-y2),2))
	if(mesafe < 0):
		mesafe = 0
	return round (mesafe, 5)

def left_sensor():
	angle_sol = angle + 90
	a, b =agent.center
	if(0 < (angle + 90) < 90):
		b -= int(math.sin(degtorad(abs(angle + 90))) * 42.5)
		a += int(math.cos(degtorad(abs(angle + 90))) * 42.5)
	elif(90 <= (angle + 90) <= 180):
		b -= int(math.sin(degtorad(abs(angle + 90))) * 42.5)
		a += int(math.cos(degtorad(abs(angle + 90))) * 42.5)
	elif(0 >= (angle + 90) > -90):
		b += int(math.sin(degtorad(abs(angle + 90))) * 42.5)
		a += int(math.cos(degtorad(abs(angle + 90))) * 42.5)
	elif(-90 >= (angle + 90) > -180):
		b += int(math.sin(degtorad(180 - abs(angle + 90))) * 42.5)
		a -= int(math.cos(degtorad(180 - abs(angle + 90))) * 42.5)

	x2,y2 = a,b
	for i in range(sensor_range):
		reference = (a,b)
		if (screen.get_at(reference) != (255, 255, 255, 255)):
			intersect = reference 
			break      
		else:
			if(0 <= angle_sol <= 90):
				b -= int(math.sin(degtorad(abs(angle_sol))) * 10)
				a += int(math.cos(degtorad(abs(angle_sol))) * 10)
			elif(180 <= angle_sol <= 270):
				b -= int(math.sin(degtorad(abs(angle_sol))) * 10)
				a += int(math.cos(degtorad(abs(angle_sol))) * 10)
			elif(0 >= angle_sol >= -90):
				b += int(math.sin(degtorad(abs(angle_sol))) * 10)
				a += int(math.cos(degtorad(abs(angle_sol))) * 10)
			elif(180 >= angle_sol >= 90):
				b += int(math.sin(degtorad(180 + abs(angle_sol))) * 10)
				a -= int(math.cos(degtorad(180 + abs(angle_sol))) * 10)
	x1,y1 = reference
	pygame.draw.line(screen, BLACK, (x2,y2), (x1,y1), 2) 
	mesafe = math.sqrt(math.pow((x1-x2),2) + math.pow((y1-y2),2))
	if(mesafe < 0):
		mesafe = 0
	return round (mesafe, 5)

def right_sensor():
	angle_sag = angle - 90
	a, b =agent.center
	if(0 < (angle - 90) < 90):
		b -= int(math.sin(degtorad(abs(angle - 90))) * 42.5)
		a += int(math.cos(degtorad(abs(angle - 90))) * 42.5)
	elif(90 <= (angle - 90) <= 180):
		b -= int(math.sin(degtorad(abs(angle - 90))) * 42.5)
		a += int(math.cos(degtorad(abs(angle - 90))) * 42.5)
	elif(0 >= (angle - 90) > -90):
		b += int(math.sin(degtorad(abs(angle - 90))) * 42.5)
		a += int(math.cos(degtorad(abs(angle - 90))) * 42.5)
	elif(-90 >= (angle - 90) > -180):
		b += int(math.sin(degtorad(180 - abs(angle - 90))) * 42.5)
		a -= int(math.cos(degtorad(180 - abs(angle - 90))) * 42.5)

	x2,y2 = a,b
	for i in range(sensor_range):
		reference = (a,b)
		if (screen.get_at(reference) != (255, 255, 255, 255)):
			intersect = reference 
			break      
		else:
			if(0 <= angle_sag <= 90):
				b -= int(math.sin(degtorad(abs(angle_sag))) * 10)
				a += int(math.cos(degtorad(abs(angle_sag))) * 10)
			elif(-270 <= angle_sag <= -180):
				b -= int(math.sin(degtorad(-abs(angle_sag))) * 10)
				a += int(math.cos(degtorad(-abs(angle_sag))) * 10)
			elif(0 >= angle_sag >= -90):
				b += int(math.sin(degtorad(abs(angle_sag))) * 10)
				a += int(math.cos(degtorad(abs(angle_sag))) * 10)
			elif(-90 >= angle_sag >= -180):
				b += int(math.sin(degtorad(180 - abs(angle_sag))) * 10)
				a -= int(math.cos(degtorad(180 - abs(angle_sag))) * 10)
	x1,y1 = reference
	pygame.draw.line(screen, BLACK, (x2,y2), (x1,y1), 2) 
	mesafe = math.sqrt(math.pow((x1-x2),2) + math.pow((y1-y2),2))
	if(mesafe < 0):
		mesafe = 0
	return round (mesafe, 5)

def front_right_sensor():
	angle_sagon = angle - 45
	a, b = agent.center
	if(0 < (angle - 27) < 90 ):
		b -= int(math.sin(degtorad(abs(angle - 27))) * 60.1)
		a += int(math.cos(degtorad(abs(angle - 27))) * 60.1)
	elif(90 <= (angle - 27) <= 180 ):
		b -= int(math.sin(degtorad(abs(angle - 27))) * 60.1)
		a += int(math.cos(degtorad(abs(angle - 27))) * 60.1)
	elif(0 >= (angle - 27) > -90):
		b += int(math.sin(degtorad(abs(angle - 27))) * 60.1)
		a += int(math.cos(degtorad(abs(angle - 27))) * 60.1)
	elif(-90 >= (angle - 27) >= -207):
		b += int(math.sin(degtorad(180 - abs(angle - 27))) * 60.1)
		a -= int(math.cos(degtorad(180 - abs(angle - 27))) * 60.1)
	
	x2,y2 = a,b
	for i in range(sensor_range):
		reference = (a,b)
		if (screen.get_at(reference) != (255, 255, 255, 255)):
			intersect = reference 
			break      
		else:
			if(0 <= angle_sagon <= 90):
				b -= int(math.sin(degtorad(abs(angle_sagon))) * 10)
				a += int(math.cos(degtorad(abs(angle_sagon))) * 10)
			elif(90 <= angle_sagon <= 180 ):
				b -= int(math.sin(degtorad(abs(angle_sagon))) * 10)
				a += int(math.cos(degtorad(abs(angle_sagon))) * 10)
			elif(0 >= angle_sagon >= -90 or -215 >= angle_sagon >= -225):
				b += int(math.sin(degtorad(abs(angle_sagon))) * 10)
				a += int(math.cos(degtorad(abs(angle_sagon))) * 10)
			elif(-90 >= angle_sagon >= -207):
				b += int(math.sin(degtorad(180 - abs(angle_sagon))) * 10)
				a -= int(math.cos(degtorad(180 - abs(angle_sagon))) * 10)
	x1,y1 = reference
	pygame.draw.line(screen, BLACK, (x2,y2), (x1,y1), 2) 
	mesafe = math.sqrt(math.pow((x1-x2),2) + math.pow((y1-y2),2))
	if(mesafe < 0):
		mesafe = 0
	return round (mesafe, 5)
	

def front_sensor():
	a, b = agent.center
	if(0 <= angle <= 90):
		b -= int(math.sin(degtorad(abs(angle))) * 61)
		a += int(math.cos(degtorad(abs(angle))) * 61)
	elif(90 <= angle <= 180):
		b -= int(math.sin(degtorad(abs(angle))) * 61)
		a += int(math.cos(degtorad(abs(angle))) * 61)
	elif(0 >= angle >= -90):
		b += int(math.sin(degtorad(abs(angle))) * 61)
		a += int(math.cos(degtorad(abs(angle))) * 61)
	elif(-90 >= angle >= -180):
		b += int(math.sin(degtorad(180 - abs(angle))) * 61)
		a -= int(math.cos(degtorad(180 - abs(angle))) * 61)
	
	x2,y2 = a,b
	for i in range(sensor_range):
		reference = (a,b)
		if (screen.get_at(reference) != (255, 255, 255, 255)):
			intersect = reference 
			break      
		else:
			if(0 <= angle <= 90):
				b -= int(math.sin(degtorad(abs(angle))) * 10)
				a += int(math.cos(degtorad(abs(angle))) * 10)
			elif(90 <= angle <= 180):
				b -= int(math.sin(degtorad(abs(angle))) * 10)
				a += int(math.cos(degtorad(abs(angle))) * 10)
			elif(0 >= angle >= -90):
				b += int(math.sin(degtorad(abs(angle))) * 10)
				a += int(math.cos(degtorad(abs(angle))) * 10)
			elif(-90 >= angle >= -180):
				b += int(math.sin(degtorad(180 - abs(angle))) * 10)
				a -= int(math.cos(degtorad(180 - abs(angle))) * 10)

	x1,y1 = reference
	pygame.draw.line(screen, BLACK, (x2,y2), (x1,y1), 2)  
	mesafe = math.sqrt(math.pow((x1-x2),2) + math.pow((y1 - y2),2))
	if mesafe < 0:
		mesafe = 0
	return round (mesafe, 5)

def front_left_sensor():
	angle_solon = angle + 45
	a, b = agent.center
	if(0 < (angle + 27) < 90):
		b -= int(math.sin(degtorad(abs(angle + 27))) * 60.1)
		a += int(math.cos(degtorad(abs(angle + 27))) * 60.1)
	elif(90 <= (angle + 27) <= 207):
		b -= int(math.sin(degtorad(abs(angle + 27))) * 60.1)
		a += int(math.cos(degtorad(abs(angle + 27))) * 60.1)
	elif(0 >= (angle + 27) > -90):
		b += int(math.sin(degtorad(abs(angle + 27))) * 60.1)
		a += int(math.cos(degtorad(abs(angle + 27))) * 60.1)
	elif(-90 >= (angle + 27) > -180):
		b += int(math.sin(degtorad(180 - abs(angle + 27))) * 60.1)
		a -= int(math.cos(degtorad(180 - abs(angle + 27))) * 60.1)
	
	x2,y2 = a,b
	for i in range(sensor_range):
		reference = (a,b)
		if (screen.get_at(reference) != (255, 255, 255, 255)):
			intersect = reference 
			break      
		else:
			if(0 <= angle_solon <= 90):
				b -= int(math.sin(degtorad(abs(angle_solon))) * 10)
				a += int(math.cos(degtorad(abs(angle_solon))) * 10)
			elif(90 <= angle_solon <= 225):
				b -= int(math.sin(degtorad(abs(angle_solon))) * 10)
				a += int(math.cos(degtorad(abs(angle_solon))) * 10)
			elif(0 >= angle_solon >= -90):
				b += int(math.sin(degtorad(abs(angle_solon))) * 10)
				a += int(math.cos(degtorad(abs(angle_solon))) * 10)
			elif(-90 >= angle_solon >= -180):
				b += int(math.sin(degtorad(180 - abs(angle_solon))) * 10)
				a -= int(math.cos(degtorad(180 - abs(angle_solon))) * 10)
	x1,y1 = reference
	pygame.draw.line(screen, BLACK, (x2,y2), (x1,y1), 2) 
	mesafe = math.sqrt(math.pow((x1-x2),2) + math.pow((y1-y2),2))
	if(mesafe < 0):
		mesafe = 0
	return round (mesafe, 5)
	
park1_empty = True
park2_empty = True
model = load_model('model_xilinx_searching')

while True: 
	environment1()
	if(not park1_empty):
		parking_area1()
	if(not park2_empty):
		parking_area2()
	sensor_front_right = front_right_sensor()
	sensor_front = front_sensor()
	sensor_front_left = front_left_sensor()


	state = [sensor_front_left / 900, sensor_front / 900, sensor_front_right / 900]
	image = pygame.transform.rotate(image_orig, angle)
	agent = image.get_rect(center=agent.center)
	screen.blit(image, agent)
	pygame.display.update()
	screen.fill(WHITE)
	x1,y1 = agent.center
	state = np.reshape(state, [1, state_size])   
	action_values = model.predict(state)
	print(f"Neural Network Outputs: {action_values}")
	action = np.argmax(action_values[0])

	if(action == 0):
		print("Selected Action: Forward")
	elif(action == 1):
		print("Selected Action: Turn Left")
	elif(action == 2):
		print("Selected Action: Turn Right")
	else:
		print("Selected Action: Stop!")

	#print(action_values)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:     
			if event.key == pygame.K_LEFT:     
				action = 1
				if(angle >= 180):
					angle = -170
				else:
					angle += 10
				if(0 <= angle <= 90):
					agent.top -= math.sin(degtorad(abs(angle))) * car_speed
					agent.right += math.cos(degtorad(abs(angle))) * car_speed
				elif(90 <= angle <= 180):
					agent.top -= math.sin(degtorad(abs(angle))) * car_speed
					agent.right += math.cos(degtorad(abs(angle))) * car_speed
				elif(0 >= angle >= -90):
					agent.top += math.sin(degtorad(abs(angle))) * car_speed
					agent.right += math.cos(degtorad(abs(angle))) * car_speed
				elif(-90 >= angle >= -180):
					agent.top += math.sin(degtorad(180 - abs(angle))) * car_speed
					agent.right -= math.cos(degtorad(180 - abs(angle))) * car_speed
			elif event.key == pygame.K_RIGHT:   
				action = 2
				if(angle <= -180):
					angle = 170
				else:
					angle += -10
				if(0 <= angle <= 90):
					agent.top -= math.sin(degtorad(abs(angle))) * car_speed
					agent.right += math.cos(degtorad(abs(angle))) * car_speed
				elif(90 <= angle <= 180):
					agent.top -= math.sin(degtorad(abs(angle))) * car_speed
					agent.right += math.cos(degtorad(abs(angle))) * car_speed
				elif(0 >= angle >= -90):
					agent.top += math.sin(degtorad(abs(angle))) * car_speed
					agent.right += math.cos(degtorad(abs(angle))) * car_speed
				elif(-90 >= angle >= -180):
					agent.top += math.sin(degtorad(180 - abs(angle))) * car_speed
					agent.right -= math.cos(degtorad(180 - abs(angle))) * car_speed
			elif event.key == pygame.K_UP:   
				action = 0
				if(0 <= angle <= 90):
					agent.top -= math.sin(degtorad(abs(angle))) * car_speed
					agent.right += math.cos(degtorad(abs(angle))) * car_speed
				elif(90 <= angle < 180):
					agent.top -= math.sin(degtorad(abs(angle))) * car_speed
					agent.right += math.cos(degtorad(abs(angle))) * car_speed
				elif(0 >= angle >= -90):
					agent.top += math.sin(degtorad(abs(angle))) * car_speed
					agent.right += math.cos(degtorad(abs(angle))) * car_speed
				elif(-90 >= angle >= -180 or angle == 180):
					agent.top += math.sin(degtorad(180 - abs(angle))) * car_speed
					agent.right -= math.cos(degtorad(180 - abs(angle))) * car_speed
			elif event.key == pygame.K_a:    
				if(True):
					park1_empty = not park1_empty
				else:
					if(angle <= -180):
						angle = 170
					else:
						angle += -10
					if(0 <= angle <= 90):
						agent.top += math.sin(degtorad(abs(angle))) * car_speed
						agent.right -= math.cos(degtorad(abs(angle))) * car_speed
					elif(90 <= angle <= 180):
						agent.top += math.sin(degtorad(abs(angle))) * car_speed
						agent.right -= math.cos(degtorad(abs(angle))) * car_speed
					elif(0 >= angle >= -90):
						agent.top -= math.sin(degtorad(abs(angle))) * car_speed
						agent.right -= math.cos(degtorad(abs(angle))) * car_speed
					elif(-90 >= angle >= -180):
						agent.top -= math.sin(degtorad(180 - abs(angle))) * car_speed
						agent.right += math.cos(degtorad(180 - abs(angle))) * car_speed
			elif event.key == pygame.K_d:    
				if(True):
					park2_empty = not park2_empty
				else:
					if(angle <= -180):
						angle = 170
					else:
						if(angle >= 180):
							angle = -170
						else:
							angle += 10
						if(0 <= angle <= 90):
							agent.top += math.sin(degtorad(abs(angle))) * car_speed
							agent.right -= math.cos(degtorad(abs(angle))) * car_speed
						elif(90 <= angle <= 180):
							agent.top += math.sin(degtorad(abs(angle))) * car_speed
							agent.right -= math.cos(degtorad(abs(angle))) * car_speed
						elif(0 >= angle >= -90):
							agent.top -= math.sin(degtorad(abs(angle))) * car_speed
							agent.right -= math.cos(degtorad(abs(angle))) * car_speed
						elif(-90 >= angle >= -180):
							agent.top -= math.sin(degtorad(180 - abs(angle))) * car_speed
							agent.right += math.cos(degtorad(180 - abs(angle))) * car_speed
			elif event.key == pygame.K_DOWN:       
				saved = True
				if(0 <= angle <= 90):
					agent.top += math.sin(degtorad(abs(angle))) * car_speed
					if(angle != 90):
						agent.right -= math.cos(degtorad(abs(angle))) * car_speed
				elif(90 <= angle <= 180):
					agent.top += math.sin(degtorad(abs(angle))) * car_speed
					agent.right -= math.cos(degtorad(abs(angle))) * car_speed
				elif(0 >= angle > -90):
					agent.top -= math.sin(degtorad(abs(angle))) * car_speed
					agent.right -= math.cos(degtorad(abs(angle))) * car_speed
				elif(-90 >= angle >= -180):
					agent.top -= math.sin(degtorad(180 - abs(angle))) * car_speed
					agent.right += math.cos(degtorad(180 - abs(angle))) * car_speed
			elif event.key == pygame.K_p:    
				action = 3
				print("heyyo")
			elif event.key == pygame.K_r:      
				rand = random.randint(0, 4) 
				angle = reborn[rand][0]
				agent.left = reborn[rand][1]
				agent.top = reborn[rand][2]
				