import pygame
from tools import *
import random
import colorsys
import math
import sys
from constants import *
from matrix import *
#from environment import Wolf
pygame.init()
FONT = pygame.font.SysFont("times new roman", 12)

#This class defines an approximation to the behavior of a sheep
class Sheep:

	def __init__(self, x, y, iden):
		
		self.position = Vector(x,y)
		self.iden = iden
		
		vec_x = random.uniform(-1,1)
		vec_y = random.uniform(-1,1)
		self.velocity = Vector(vec_x, vec_y)
		self.velocity.normalize()
		self.velocity = self.velocity * random.uniform(1.5, 4)

		self.acceleration = Vector()
		self.color = WHITE
		self.temp = self.color
		self.secondaryColor = (70,70,70)
		self.color_pam1 = 255#random.randint(15,255)
		self.color_pam2 = 255#random.randint(15,255)
		self.color_pam3 = 255

		self.max_speed = 2
		self.max_length = 1
		self.size = 2
		self.stroke = 3
		self.angle = 0
		self.hue = 0
		self.radius = 120
		self.alive = True
		self.scared = False
		self.alert = False
		self.icon_original = pygame.image.load('assets/icon.png')
		self.icon_scale = (1,1)

		self.isStuck = False
		self.stuckCounter = 0
        #self.icon_scale = icon_scale

	#To avoid moving out the screen
	def limits(self, left, right, top, bottom):
		if self.position.x >= right or self.position.x <= left:
			self.velocity.x *= -0.5
			if self.position.x > right:
				self.position.x -= 2
			elif self.position.x < left:
				self.position.x += 2

		if self.position.y >= bottom or self.position.y <= top:
			self.velocity.y *= -0.5
			if self.position.y > bottom:
				self.position.y -= 2
			elif self.position.y < top:
				self.position.y += 2

	#To provoke deaths
	def death(self):
		self.velocity.reset()
		self.acceleration.reset()
		self.color_pam1 = 0
		self.color_pam2 = 0
		self.color_pam3 = 0
		self.alive = False
		self.alert = False

	#To react to the presence of other sheeps
	#Boids model was supposed, so the main contributions of other sheeps are separation, cohesion and alignment
	def behaviour(self, herd):
		self.acceleration.reset()
		if (self.alive and not self.scared):
			#Cohesion
			coh = self.cohesion(herd)
			coh = coh * 0.16
			self.acceleration.add(coh)

			#Alignment
			align = self.alignment(herd)
			align = align * 0.16
			self.acceleration.add(align)

			#Separation
			sep = self.separation(herd)
			sep = sep * 0.16
			self.acceleration.add(sep)
		elif (self.alive and self.scared):
			#Separation
			sep = self.separation(herd)
			self.max_speed = 3
			sep = sep * 0.6
			self.acceleration.add(sep)
		elif (self.isStuck):
			self.acceleration.reset()
			#self.velocity.reset()

	def separation(self, herd):
		total = 0
		wolfFlag = False
		steering = Vector()

		for mate in herd:
			if (mate == self or (mate.alive == False and not isinstance(mate, Hole) ) or self.alive == False):
				continue
			elif isinstance(mate, Sheep):
				dist = getDistance(self.position, mate.position)
				if dist < self.radius:
					temp = SubVectors(self.position,mate.position)
					temp = temp/(dist ** 2)
					steering.add(temp)
					total += 1
			elif isinstance(mate, Wolf):
				dist = getDistance(self.position, mate.position)
				if dist < self.radius and dist > 10:
					wolfFlag = True
					temp = SubVectors(self.position, mate. position)
					temp = temp/(dist**2)
					steering.add(temp*5)
					total += 1
				elif dist < 10:
					self.death()
					mate.eatCounter += 1
			elif isinstance(mate, Hole):
				dist = getDistance(self.position, mate.position)
				if (dist < 10 and self.stuckCounter < 1):
					self.isStuck = True

		if not wolfFlag:
			self.scared = False
			self.max_speed = 2	

		if wolfFlag:
			self.scared = True
			wolfFlag = False

		if total > 0:
			steering = steering / total
			# steering = steering - self.position
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity
			steering.limit(self.max_length)

		return steering

	def alignment(self, herd):
		total = 0
		steering = Vector()
		# hue = uniform(0, 0.5)
		for mate in herd:
			if (mate == self or (mate.alive == False and not isinstance(mate, Hole) ) or self.alive == False):
				continue
			elif isinstance(mate, Sheep):
				dist = getDistance(self.position, mate.position)
				if dist < self.radius:
					vel = mate.velocity.Normalize()
					steering.add(vel)
					mate.color = hsv_to_rgb( self.hue ,1, 1)
					total += 1
			elif isinstance(mate, Hole):
				dist = getDistance(self.position, mate.position)
				if (dist < 10 and self.stuckCounter < 1):
					self.isStuck = True

		if total > 0:
			steering = steering / total
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity.Normalize()
			steering.limit(self.max_length)
		return steering

	def cohesion(self, herd):
		total = 0
		steering = Vector()

		for mate in herd:
			if (mate == self or (mate.alive == False and not isinstance(mate, Hole) ) or self.alive == False):
				continue
			elif isinstance(mate, Sheep):
				dist = getDistance(self.position, mate.position)
				if (dist < self.radius):
					steering.add(mate.position)
					total += 1
			elif isinstance(mate, Hole):
				dist = getDistance(self.position, mate.position)
				if (dist < 10 and self.stuckCounter < 1):
					self.isStuck = True

		if total > 0:
			steering = steering / total
			steering = steering - self.position
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity
			steering.limit(self.max_length)

		return steering

	#To verify if it is out the protected area
	def is_in_place(self, left, right, top, bottom):
		if (self.position.x < left or self.position.x > right or self.position.y > bottom or self.position.y < top):
			return True
		else:
			return False

	#To update position
	def update(self):
		if (self.scared):
			self.acceleration.add( Vector(random.uniform(-1.00, 1.00),random.uniform(-1.00, 1.00)) )
		if(self.alive):
			self.position = self.position + self.velocity
			self.velocity = self.velocity + self.acceleration
			self.velocity.limit(self.max_speed)
			self.angle = self.velocity.heading() + math.pi/2
		if (self.isStuck):
			if (self.stuckCounter < 1):
				self.velocity.reset()
				self.acceleration.reset()
				self.position = self.position
				self.stuckCounter += 1
			else:
				self.acceleration = Vector(0.5, 0.5)
				self.position = self.position + self.velocity
				self.velocity = self.velocity + self.acceleration
				self.velocity.limit(self.max_speed)
				self.angle = self.velocity.heading() + math.pi/2
				self.stuckCounter = 0
				self.isStuck = False

	#To draw sheeps
	def draw(self, screen, distance, etiq, scale):
		ps = []
		points = [None for _ in range(3)]

		points[0] = [[0],[-self.size],[0]]
		points[1] = [[self.size//2],[self.size//2],[0]]
		points[2] = [[-self.size//2],[self.size//2],[0]]

		for point in points:
			rotated = matrix_multiplication(rotationZ(self.angle), point)
			z = 1 / (distance - rotated[2][0])

			projection_matrix = [[z, 0, 0], [0, z, 0]]
			projected_2d = matrix_multiplication(projection_matrix, rotated)

			x = int(projected_2d[0][0] * scale) + self.position.x
			y = int(projected_2d[1][0] * scale) + self.position.y

			ps.append((x, y))


		if (not self.is_in_place(LEFT, RIGHT, TOP, BOTTOM) and not self.isStuck):#self.alert == False:
			self.icon_original = pygame.image.load('assets/icon.png')
		
		if (self.is_in_place(LEFT, RIGHT, TOP, BOTTOM) and not self.isStuck):
			self.icon_original = pygame.image.load('assets/yellow_icon.png')

		if self.isStuck:
			self.icon_original = pygame.image.load('assets/green_icon.png')

		if self.scared:
			self.icon_original = pygame.image.load('assets/red_icon.png')

		if not self.alive:
			self.icon_original = pygame.image.load('assets/black_icon.png')


		#if not self.is_in_place(LEFT, RIGHT, TOP, BOTTOM):
		#	self.icon_orignal = pygame.image.load('assets/yellow_icon.png')

		#if self.alert:
		#	self.icon_original = pygame.image.load('assets/yellow_icon.png')
			#pygame.draw.polygon(screen, RED, ps, self.stroke


		# Calcular el ángulo de rotación en función de los puntos
		if len(ps) >= 2:
			dx = ps[1][0] - ps[0][0]
			dy = ps[1][1] - ps[0][1]
			angle = math.degrees(math.atan2(dy, dx))
		else:
			angle = 0

		# Escalar la imagen en función de scale
		scaled_icon = pygame.transform.scale(self.icon_original, (int(self.icon_scale[0] * scale), int(self.icon_scale[1] * scale)*0.65))

		# Rotar la imagen escalada
		rotated_icon = pygame.transform.rotate(scaled_icon, -angle)  # El ángulo se invierte para la rotación correcta

		# Obtener el rectángulo de la imagen rotada y centrarlo en la posición (x, y)
		icon_rect = rotated_icon.get_rect(center=(self.position.x, self.position.y))

		# Dibujar la imagen rotada
		screen.blit(rotated_icon, icon_rect.topleft)

		if etiq:
			id_text = FONT.render(f"{self.iden}", 1, WHITE)
			screen.blit(id_text, (x + id_text.get_width() / 2, y - id_text.get_height() / 2))

		'''
		ps = []
		points = [None for _ in range(3)]

		points[0] = [[0],[-self.size],[0]]
		points[1] = [[self.size//2],[self.size//2],[0]]
		points[2] = [[-self.size//2],[self.size//2],[0]]

		for point in points:
			rotated = matrix_multiplication(rotationZ(self.angle) , point)
			z = 1/(distance - rotated[2][0])

			projection_matrix = [[z, 0, 0], [0, z, 0]]
			projected_2d = matrix_multiplication(projection_matrix, rotated)

			x = int(projected_2d[0][0] * scale) + self.position.x
			y = int(projected_2d[1][0] * scale) + self.position.y
			ps.append((x, y))

		pygame.draw.polygon(screen, (self.color_pam1, self.color_pam2, self.color_pam3), ps)
		if (self.alert):
			pygame.draw.polygon(screen, RED, ps, self.stroke)
		#else:
		#	pygame.draw.polygon(screen,(0,0,0),ps, self.stroke)

		if etiq:
			id_text = FONT.render(f"{self.iden}", 1, WHITE)
			screen.blit(id_text, (x + id_text.get_width()/2, y - id_text.get_height()/2))
		'''

class Wolf:

	def __init__(self, x, y):
		self.position = Vector(x,y)
		
		vec_x = random.uniform(-1,1)
		vec_y = random.uniform(-1,1)

		self.velocity = Vector(vec_x, vec_y)
		self.velocity.normalize()
		self.velocity = self.velocity * random.uniform(1.5, 4)

		self.acceleration = Vector()
		self.color = LIGHT_GREY

		self.max_speed = 4
		self.max_length = 1
		self.alive = True
		self.size = 2
		self.stroke = 3
		self.angle = 0
		self.hue = 0
		self.radius = 150

		self.icon_original = pygame.image.load('assets/wolf.png')
		self.icon_scale = (1.2,1.2)

		self.eatCounter = 0

	def limits(self,left, right, top, bottom):
		if self.position.x >= right or self.position.x <= left:
			self.velocity.x *= -1
			if self.position.x > right:
				self.position.x -= 2
			elif self.position.x < left:
				self.position.x += 2

		if self.position.y >= bottom or self.position.y <= top:
			self.velocity.y *= -1
			if self.position.y < top:
				self.position.y += 2

	def behaviour(self, others):
		if (self.alive and self.eatCounter < 2):
			self.acceleration.reset()
			coh = self.cohesion(others)
			coh = coh * 0.16
			self.acceleration.add(coh)

			align = self.alignment(others)
			align = align * 0.16
			self.acceleration.add(align)

			sep = self.separation(others)
			sep = sep * 0.16
			self.acceleration.add(sep)
		elif (self.eatCounter >= 2):
			self.acceleration = Vector(1,0)

	def separation(self, others):
		total = 0
		steering = Vector()

		for mate in others:
			if (mate == self or mate.alive == False or self.alive == False):
				continue
			elif isinstance(mate, Wolf):
				dist = getDistance(self.position, mate.position)
				if dist < self.radius:
					temp = SubVectors(self.position, mate.position)
					temp = temp/(dist ** 2)
					steering.add(temp)
					total += 1

		if total > 0:
			steering = steering / total
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity
			steering.limit(self.max_length)

		return steering

	def alignment(self, others):
		total = 0 
		steering = Vector()

		for mate in others:
			if (mate == self or mate.alive == False or self.alive == False):
				continue
			elif isinstance(mate, Wolf):
				dist = getDistance(self.position, mate.position)
				if dist < self.radius:
					vel = mate.velocity.Normalize()
					steering.add(vel)
					mate.color = hsv_to_rgb( self.hue, 1, 1 )
					total += 1
			elif isinstance(mate, Sheep):
				dist = getDistance(self.position, mate.position)
				if dist < self.radius:
					vel = mate.velocity.Normalize()
					steering.add(vel)
					mate.color = hsv_to_rgb( self.hue, 1, 1 )
					total += 1

		if total > 0:
			steering = steering / total
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity.Normalize()
			steering.limit(self.max_length)
		return steering

	def cohesion(self, others):
		total = 0
		sheepFlag = False
		steering = Vector()

		for mate in others:
			if (mate == self or mate.alive == False or self.alive == False):
				continue
			elif isinstance(mate, Wolf):
				dist = getDistance(self.position, mate.position)
				if (dist < self.radius):
					steering.add(mate.position)
					total += 1
			elif isinstance(mate, Sheep):
				dist = getDistance(self.position, mate.position)
				if ( dist < self.radius):
					sheepFlag = True
					self.max_speed = 2.5
					steering.add(mate.position)
					total += 1

		if not sheepFlag:
			self.max_speed = 2

		if sheepFlag:
			sheepFlag = False

		if total > 0:
			steering = steering / total
			steering = steering - self.position
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity
			steering.limit(self.max_length)

		return steering

	def update(self):
		if (self.alive):
			self.position = self.position + self.velocity
			self.velocity = self.velocity + self.acceleration
			self.velocity.limit(self.max_speed)
			self.angle = self.velocity.heading() + math.pi/2

	def draw(self, screen, distance, scale):
		'''
		ps = []
		points = [None for _ in range(3)]

		points[0] = [[0],[-self.size],[0]]
		points[1] = [[self.size//2],[self.size//2],[0]]
		points[2] = [[-self.size//2],[self.size//2],[0]]

		for point in points:
			rotated = matrix_multiplication(rotationZ(self.angle) , point)
			z = 1/(distance - rotated[2][0])

			projection_matrix = [[z, 0, 0], [0, z, 0]]
			projected_2d = matrix_multiplication(projection_matrix, rotated)

			x = int(projected_2d[0][0] * scale) + self.position.x
			y = int(projected_2d[1][0] * scale) + self.position.y
			ps.append((x, y))

		pygame.draw.polygon(screen, LIGHT_GREY, ps, self.stroke)
		#else:
		#	pygame.draw.polygon(screen,(0,0,0),ps, self.stroke)
		
		'''
		ps = []
		points = [None for _ in range(3)]

		points[0] = [ [0], [-self.size], [0] ]
		points[1] = [ [self.size//2], [self.size//2], [0] ]
		points[2] = [ [-self.size//2], [self.size//2], [0] ]

		for point in points:
			rotated = matrix_multiplication( rotationZ(self.angle), point )
			z = 1 / ( distance - rotated[2][0] ) 

			projection_matrix = [ [z,0,0], [0,z,0] ]
			projected_2d = matrix_multiplication(projection_matrix, rotated)

			x = int(projected_2d[0][0] * scale ) + self.position.x
			y = int(projected_2d[1][0] * scale ) + self.position.y

			ps.append( (x,y) )

		if len(ps) >= 2:
			dx = ps[1][0] - ps[0][0]
			dy = ps[1][1] - ps[0][1]
			angle = math.degrees(math.atan2(dy,dx))
		else:
			angle = 0

		scaled_icon = pygame.transform.scale(self.icon_original, (int(self.icon_scale[0] * scale), int(self.icon_scale[1] * scale)/2))

		# Rotar la imagen escalada
		rotated_icon = pygame.transform.rotate(scaled_icon, -angle)  # El ángulo se invierte para la rotación correcta

		# Obtener el rectángulo de la imagen rotada y centrarlo en la posición (x, y)
		icon_rect = rotated_icon.get_rect(center=(self.position.x, self.position.y))

		# Dibujar la imagen rotada
		screen.blit(rotated_icon, icon_rect.topleft)
		
	def is_in_place(self, left, right, top, bottom):
			if (self.position.x < left or self.position.x > right or self.position.y > bottom or self.position.y < top):
				return True
			else:
				return False


class Hole:

	def __init__(self, x, y):
		self.position = Vector(x,y)
		
		self.radius = 500
		self.size = 2
		self.icon_original = pygame.image.load('assets/hole.png')
		self.icon_scale = (1,1)

		self.angle = 0
		self.fallCounter = 0

		self.alive = False

	def draw(self, screen, distance, scale):
		'''
		ps = []
		points = [None for _ in range(3)]

		points[0] = [[0],[-self.size],[0]]
		points[1] = [[self.size//2],[self.size//2],[0]]
		points[2] = [[-self.size//2],[self.size//2],[0]]

		for point in points:
			rotated = matrix_multiplication(rotationZ(self.angle) , point)
			z = 1/(distance - rotated[2][0])

			projection_matrix = [[z, 0, 0], [0, z, 0]]
			projected_2d = matrix_multiplication(projection_matrix, rotated)

			x = int(projected_2d[0][0] * scale) + self.position.x
			y = int(projected_2d[1][0] * scale) + self.position.y
			ps.append((x, y))

		pygame.draw.polygon(screen, LIGHT_GREY, ps, self.stroke)
		#else:
		#	pygame.draw.polygon(screen,(0,0,0),ps, self.stroke)
		
		'''
		ps = []
		points = [None for _ in range(3)]

		points[0] = [ [0], [-self.size], [0] ]
		points[1] = [ [self.size//2], [self.size//2], [0] ]
		points[2] = [ [-self.size//2], [self.size//2], [0] ]

		for point in points:
			rotated = matrix_multiplication( rotationZ(self.angle), point )
			z = 1 / ( distance - rotated[2][0] ) 

			projection_matrix = [ [z,0,0], [0,z,0] ]
			projected_2d = matrix_multiplication(projection_matrix, rotated)

			x = int(projected_2d[0][0] * scale ) + self.position.x
			y = int(projected_2d[1][0] * scale ) + self.position.y

			ps.append( (x,y) )


		scaled_icon = pygame.transform.scale(self.icon_original, (int(self.icon_scale[0] * scale), int(self.icon_scale[1] * scale)/2))

		# Obtener el rectángulo de la imagen rotada y centrarlo en la posición (x, y)
		icon_rect = scaled_icon.get_rect(center=(self.position.x, self.position.y))

		# Dibujar la imagen rotada
		screen.blit(scaled_icon, icon_rect.topleft)
