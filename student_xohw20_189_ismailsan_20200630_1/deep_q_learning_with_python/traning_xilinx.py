import pygame, time
import math 
import random
import numpy as np
import os
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from collections import deque

PI = 3.1415
WINDOWWIDTH = 1600
WINDOWHEIGHT = 1000
RED =   (255, 0,  0)
GREEN = (0,  255, 0)
BLUE =  (0,   0, 255)
WHITE   = (255, 255, 255)
BLACK =   (0, 0, 0)
otoparkgenisligi = 100
car_speed = 20
LEARNING_RATE = 0.001
DISCOUNT = 0.9
EPISODES = 9999999999
epsilon = 1.0
epsilon_decay = 0.99
epsilon_min = 0.01
otopark_variable = 250
state_size = 3
action_size = 3
batch_size = 32
n_episodes = 100001
score = 0
save = 0
egitim = 1
timesayac = 0
sensor_range = 100
sayac = 0

reborn = [[0,400,40], [0,600,40], [0,900,40], [0,1200,40],[-45, 1200,50],[-90, 1300, 350],[-145, 1200, 600],[180, 900,600],[180, 600,600],[135,350,600],[180,350,600],[90,300,300]]

pygame.init()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

def nesneler():   
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
	pygame.draw.line(screen, BLACK, (552 + otopark_variable, 522), (587+ otopark_variable, 567), 20)
	pygame.draw.line(screen, BLACK, (587+ otopark_variable, 567), (587+ otopark_variable, 767), 20)
	pygame.draw.line(screen, BLACK, (587+ otopark_variable, 767), (744+ otopark_variable, 767), 20)
	pygame.draw.line(screen, BLACK, (744+ otopark_variable, 767), (744+ otopark_variable, 567), 20)
	pygame.draw.line(screen, BLACK, (743+ otopark_variable, 567), (779+ otopark_variable, 517), 20)
	pygame.draw.line(screen, BLACK, (769+ otopark_variable, 527), (802+ otopark_variable, 527), 20)
	pygame.draw.line(screen, BLACK, (802+ otopark_variable, 527), (1178, 527), 20)
	pygame.draw.line(screen, BLACK, (1168, 517), (1208, 562), 20)
	pygame.draw.line(screen, BLACK, (5, 5), (1500,5), 80)
	pygame.draw.line(screen, BLACK, (1500, 5), (1500,900), 80)
	pygame.draw.line(screen, BLACK, (1500,900), (5,900), 80)
	pygame.draw.line(screen, BLACK, (5,900), (5,5), 60)
	pygame.draw.rect(screen,BLACK,(1300,1340,430,400))

clock = pygame.time.Clock()
screen_rect = screen.get_rect()
image_orig = pygame.image.load("car_image.jpeg").convert()
image_orig = pygame.transform.scale(image_orig, (122, 85))
image = image_orig.copy()
agent = image_orig.get_rect(center=screen_rect.center)
agent.left = 700
agent.top = 350
angle = 180

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

def distance(x_current, y_current, x_target, y_target):
	return math.sqrt(math.pow((x_current-x_target),2) + math.pow((y_current-y_target),2))

scores = [0,0,0,0,0,0,0,0,0,0]
memory = deque(maxlen=500)
##BUILD MODEL
model = Sequential()
model.add(Dense(32, input_dim = state_size, activation = 'linear'))
model.add(Dense(64, activation='linear'))
model.add(Dense(32, activation='linear'))
model.add(Dense(action_size, activation='linear'))
model.compile(loss = 'mse', optimizer=Adam(lr=LEARNING_RATE), metrics=['accuracy'])

done=False

current_state = [0,0,0]
next_state = [0,0,0]
for time in range(0,EPISODES):
    image = pygame.transform.rotate(image_orig, angle)
    agent = image.get_rect(center=agent.center)
    screen.blit(image, agent)
    pygame.display.update()
    screen.fill(WHITE)
    nesneler()

    sensor_front_right_current = front_right_sensor()
    sensor_front_current = front_sensor()
    sensor_front_left_current = front_left_sensor()
    current_state = [sensor_front_left_current / 900, sensor_front_current / 900, sensor_front_right_current / 900]
    a, b = agent.center
    current_state = np.reshape(current_state, [1, state_size])   

    ##SELECT ACTION
    action_values = model.predict(current_state)
    if(np.random.rand() <= epsilon):
        action = random.randrange(action_size)
    else:      
        action = np.argmax(action_values[0])
             
    if (action == 1):     #FORWARD LEFT - ILERI SOL
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
    elif (action == 2):      #FORWARD RIGHT - ILERI SAG
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
    elif (action == 0):     #FORWARD - ILERI
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
    elif (action == 6):       #BACKWARD LEFT - GERI SOL
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
    elif (action == 4):       #BACKWARD RIGHT - GERI SAG
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
    elif (action == 5):        #BACKWARD
        if(0 <= angle <= 90):
            agent.top += math.sin(degtorad(abs(angle))) * car_speed
            if ( angle != 0):
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
    elif (action == 3):         #DO NOT MOVE - SABIT KAL
        pass


    a, b = agent.center
    sensor_front_right = front_right_sensor()
    sensor_front = front_sensor()
    sensor_front_left = front_left_sensor()
    next_state = [sensor_front_left / 900, sensor_front / 900, sensor_front_right]
    next_state = np.reshape(next_state, [1, state_size]) 
    
    score+=1
    timesayac+=1

    if(score == 80):
        model.save("model_80")
    if(score == 400):
    	model.save("model_400")
    if(score == 600):
    	model.save("model_600")

    if(sensor_front_left_current < (1/500) or sensor_front_current < (1/500) or sensor_front_right_current < (1/500)):
        done = True
        if(timesayac > 500):
            timesayac = 0
        a = random.randint(0,10)
        print(f"episode : {sayac} - score : {score}")
        scores[sayac] = score
        sayac+=1
        if(sayac == 10):
        	ssum = 0
        	sayac = 0
        	for ss in range(0,10):
        		ssum += scores[ss]
        	print(f"average : {ssum / 10}")
        agent.left = 1260
        agent.top = 700
        angle = 90
        reward = -2  #crash-carpma
        score = 0
        egitim = 1
    elif(action == 0): #sag sol on 
    	reward = 0.1
    else:
    	reward = 0

    ##REMEMBER
    memory.append((current_state, action, reward, next_state, done))

    if done:
        #print("episode: {}/{}".format(time, n_episodes))  
        done = False   
    
    if(epsilon > epsilon_min):
        epsilon *= epsilon_decay 
   

    if len(memory) > batch_size:
        minibatch = random.sample(memory, batch_size)
        for current_state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + DISCOUNT * np.amax(model.predict(next_state)[0]))
            target_f = model.predict(current_state)
            target_f[0][action] = target
            model.fit(current_state, target_f, epochs=1, verbose = 0)

