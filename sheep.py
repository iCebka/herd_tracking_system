import pygame
from tools import *
import random
import colorsys
import math
import sys
from constants import *
from matrix import *
pygame.init()
FONT = pygame.font.SysFont("times new roman", 12)

class Sheep:
	def __init__(self, x, y, iden):
		
		self.position = Vector(x,y)
		self.iden = iden
		#Velocity
		vec_x = random.uniform(-1,1)
		vec_y = random.uniform(-1,1)
		self.velocity = Vector(vec_x, vec_y)
		self.velocity.normalize()
		self.velocity = self.velocity * random.uniform(1.5, 4)

		#Acceleration
		self.acceleration = Vector()
		self.color = WHITE
		self.temp = self.color
		self.secondaryColor = (70,70,70)
		self.color_pam1 = 255#random.randint(15,255)
		self.color_pam2 = 255#random.randint(15,255)

		self.max_speed = 2
		self.max_length = 1
		self.size = 2
		self.stroke = 3
		self.angle = 0
		self.hue = 0
		self.radius = 400
		self.alive = True

		self.alert = False

	def limits(self, left, right, top, bottom):
		if self.position.x >= right or self.position.x <= left:
			#print(self.iden, " esta en (", self.position.x, ",", self.position.y, ") Ejecuta cambio en x")
			self.velocity.x *= -0.5
			if self.position.x > right:
				self.position.x -= 2
			elif self.position.x < left:
				self.position.x += 2

		if self.position.y >= bottom or self.position.y <= top:
			#print(self.iden, " esta en (", self.position.x, ",", self.position.y, ") Ejecuta cambio en x")
			self.velocity.y *= -0.5
			if self.position.y > bottom:
				self.position.y -= 2
			elif self.position.y < top:
				self.position.y += 2

	def death(self):
		self.velocity.reset()
		self.acceleration.reset()
		self.color_pam1 = 0
		self.color_pam2 = 0
		self.alive = False
		#self.position = self.position
		self.alert = False

	def behaviour(self, herd):

		self.acceleration.reset()
		if (self.alive):
			#Cohesion
			coh = self.cohesion(herd)
			coh = coh * 0.2
			self.acceleration.add(coh)

			#Alignment
			align = self.alignment(herd)
			align = align * 0.3
			self.acceleration.add(align)

			#Separation
			sep = self.separation(herd)
			sep = sep * 0.24
			self.acceleration.add(sep)

	def separation(self, herd):
		total = 0
		steering = Vector()

		for mate in herd:
			if (mate == self or mate.alive == False or self.alive == False):
				continue
			else:
				dist = getDistance(self.position, mate.position)
				if dist < self.radius:
					temp = SubVectors(self.position,mate.position)
					temp = temp/(dist ** 2)
					steering.add(temp)
					total += 1

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
			if (mate == self or mate.alive == False or self.alive == False):
				continue
			else:
				dist = getDistance(self.position, mate.position)
				if dist < self.radius:
					vel = mate.velocity.Normalize()
					steering.add(vel)
					mate.color = hsv_to_rgb( self.hue ,1, 1)
					total += 1

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
			if (mate == self or mate.alive == False or self.alive == False):
				continue
			else:
				dist = getDistance(self.position, mate.position)
				if (dist < self.radius):
					steering.add(mate.position)
					total += 1
		if total > 0:
			steering = steering / total
			steering = steering - self.position
			steering.normalize()
			steering = steering * self.max_speed
			steering = steering - self.velocity
			steering.limit(self.max_length)

		return steering

	def is_in_place(self, left, right, top, bottom):
		if (self.position.x < left or self.position.x > right or self.position.y > bottom or self.position.y < top):
			return True
		else:
			return False

	def update(self):
		if(self.alive):
			self.position = self.position + self.velocity
			self.velocity = self.velocity + self.acceleration
			self.velocity.limit(self.max_speed)
			self.angle = self.velocity.heading() + math.pi/2

	def draw(self, screen, distance, etiq, scale):
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

		pygame.draw.polygon(screen, (self.color_pam1, self.color_pam2, 0), ps)
		if (self.alert):
			pygame.draw.polygon(screen, RED, ps, self.stroke)
		#else:
		#	pygame.draw.polygon(screen,(0,0,0),ps, self.stroke)

		if etiq:
			id_text = FONT.render(f"{self.iden}", 1, WHITE)
			screen.blit(id_text, (x + id_text.get_width()/2, y - id_text.get_height()/2))
