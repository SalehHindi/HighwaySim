import matplotlib.pyplot as plt
import pdb
import math
import time
import random

class Simulation(object):
	def __init__(self, numberOfLanes, numberOfCars, graphing = True):
		self.graphing = graphing
		self.numberOfLanes = numberOfLanes
		self.numberOfCars = numberOfCars

	def run(self):
		initTime = time.time()

		SIM = Highway()
		for x in range(self.numberOfLanes):
			SIM.addLane()

		if self.graphing:
			fig = plt.figure()
			plt.ion()

		# Make this loop "While there are cars on the highway"
		for x in range(17 * 5):
			if x < self.numberOfCars*5 and x % 5 == 0:
				for lane in SIM.lanes:
					lane.addCar()

			SIM.updateHighway()

			for i in range(len(SIM.lanes)):
				positionData = SIM.lanes[i].printLane()
				if self.graphing: 
					plt.plot(positionData, [i*3]*(len(positionData)), 'ro')

			if self.graphing:
				plt.ylabel('SIM')
				fig.canvas.draw()
				plt.show()
				plt.clf()
				plt.axis([0, 50, 0, 50])
				time.sleep(.1)	
		finalTime = time.time()
		return finalTime - initTime		

	def createHighway(self):
		pass		

class Highway(object):
	def __init__(self):
		self.lanes = []
		self.speedLimit = 7.5
		self.aboveSpeedFactor = 2.0 # How fast people will go over the speed limit
		self.gap = .8
		self.aggressiveness = 1.0
		self.highwayLength = 30

	def addLane(self):
		newLane = Lane(gap = self.gap, speedLimit = self.speedLimit, highwayLength = self.highwayLength, speedLogFunction = self.logisticFunction, aboveSpeedFactor = self.aboveSpeedFactor)
		self.lanes.append(newLane)

	def updateHighway(self):
		for lane in self.lanes:
			lane.update()

	def logisticFunction(self, x, L, x0, k):
		L=self.speedLimit + self.aboveSpeedFactor
		x0=self.gap
		k=self.aggressiveness

		# return L/(1.0 + math.exp( (-k)*(x-x0) ))
		return (k*L*math.exp((-k)*(x-x0)))/((math.exp((-k)*(x-x0)) + 1)**2)

class Lane(object):
	def __init__(self, gap, speedLimit, highwayLength, speedLogFunction, aboveSpeedFactor):
		self.carId = 1
		self.head = None
		self.butt = None
		self.highwayLength= highwayLength
		self.timeStep = .17
		self.aggressiveness = 1.0
		self.gap = gap
		self.speedLimit = speedLimit
		self.speedLogFunction = speedLogFunction
		self.aboveSpeedFactor = aboveSpeedFactor

	def update(self):
		self.updateVelocity()
		self.updatePosition()

	def checkForAccidents(self, current):
		# Make this a function. I don't know which one though......
		chanceOfAccident = .000
		randomNumber = random.random()
		if randomNumber < chanceOfAccident:
			return -1.3
		else:
			return 0.0

	def checkAheadForCars(self, current):
		current = current
		# if current.getNextCar() == None:
			# return current.velocity
		# elif (current.getNextCar().position-current.position) < self.gap:
		if current.getNextCar() == None:
			x=1
			gapMeasure = self.gap * 2.7
			# 2.7 is currently a magic number.... make this more precise...
		else:			
			x=2
			p2 = current.position
			p1 = current.getNextCar().position
			gapMeasure = (p1-p2) - self.gap


		if gapMeasure < -1.0:
			pdb.set_trace()

		y = self.logisticFunction(x = gapMeasure)
		print str(current.carId), "GapM:", str(gapMeasure), "V:", str(y), "Pos:", str(current.position)
		if y == None:
			x=4
			pdb.set_trace()
		return y

	def updateVelocity(self):
		current = self.head
		while current != None:
			accelerationDueToAccidents = self.checkForAccidents(current)
			accelerationDueToNoCars = self.checkAheadForCars(current)

			if accelerationDueToAccidents != 0:
				current.velocity = current.velocity + current.velocity * accelerationDueToAccidents
				if current.velocity == None:
					x=1
					pdb.set_trace()
			else: # elif accelerationDueToNoCars != None:
				current.velocity = accelerationDueToNoCars
				if current.velocity == None:
					x=2
					pdb.set_trace()

			current = current.getPreviousCar()		

	def updatePosition(self):
		print ''
		current = self.head
		while current != None:
			print('Car: ', current.carId, 'Position: ', current.position, 'Velocity:', current.velocity)
			current.setPosition(current.position + current.velocity * self.timeStep)

			if current.position > self.highwayLength:
				current = current.getPreviousCar()	
				self.popHead()
			else:
				current = current.getPreviousCar()	

	def addCar(self):
		newCar = Car()
		if self.head == None:
			self.head = newCar
			self.butt = self.head
		else:
			newCar.setNextCar(self.butt)
			self.butt.setPreviousCar(newCar)
			self.butt = self.butt.getPreviousCar()

		self.butt.carId = self.carId
		self.carId += 1	
		# print('Butt car: ', str(self.butt.carId))

	def popHead(self):
		oldHead = self.head
		if self.head != self.butt:
			self.head = self.head.getPreviousCar()
			self.head.setNextCar(None)
		elif self.head == self.butt:
			self.head = None

	def printLane(self):
		current = self.head
		carPosition = []

		while current != None:
			carPosition.append(current.position)
			current = current.getPreviousCar()	

		return carPosition

	def logisticFunction(self, x):
		L=self.speedLimit + self.aboveSpeedFactor
		x0=self.gap
		k=self.aggressiveness

		# return L/(1.0 + math.exp( (-k)*(x-x0) ))
		return L/(1.0 + math.exp( (-k)*(x-x0) ))

class Car(object):
	# Should be a propert of the lane so we can have the Xth car in every lane

	def __init__(self):
		self.carId = 0

		self.position = 0.0
		self.velocity = 2.5
		self.acceleration = 0.0

		self.nextCar = None
		self.previousCar = None

	def update(self):
		# update will be called on every car
		pass

	def setPosition(self, newPosition):
		self.position = newPosition

	def getNextCar(self):
		return self.nextCar

	def getPreviousCar(self):
		return self.previousCar

	def setNextCar(self, car):
		self.nextCar = car

	def setPreviousCar(self, car):
		self.previousCar = car		

#################################
a = Simulation(numberOfLanes = 5, numberOfCars = 12, graphing = True)
print a.run()

