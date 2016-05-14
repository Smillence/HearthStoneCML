#!/usr/bin/env python
# -*- coding: utf-8 -*- 

class Minion(object):
	def __init__(self,card,player,game):
		self.card = card
		#self.maxHealth = card['health']
		#self.attack = card['attack']
		self.buffs = {'attack':0,'health':0,'spellDamage':0,'taunt':False,\
			'divineShield':False,'stealth':False}
		self.health = self.getMaxHealth()
		self.player = player
		self.game = game
		self.spellDamage = 0
		self.timerTasks = {}
		self.target = None
	def getAttack(self):
		return self.card.getAttack() + self.buffs['attack']
	def getHealth(self):
		if self.health > self.getMaxHealth():
			self.health = self.getMaxHealth()
		return self.health
	def getMaxHealth(self):
		return self.card.getHealth() + self.buffs['health']
	def getSpellDamage(self):
		return self.spellDamage + self.buffs['spellDamage']
	def battlecry(self,pos):
		return self,pos
	def chooseOne(self):
		return self
	def deathrattle(self,pos):# the position where the minions dies at
		pass
	def startTurn(self):
		pass
	def endTurn(self):
		pass
	def setSpellDamage(self,val):
		self.spellDamage = val
	def getBoardPos(self):
		return self.player.getAllMinions().index(self)+1
	def modifyAttack(self,incremental):
		self.buffs['attack'] += incremental
	def modifyMaxHealth(self,incremental):
		self.buffs['health'] += incremental
	def modifyHealth(self,incremental):
		if incremental < 0 and self.hasDivineShield():
			self.buffs['divineShield'] = False
			self.card.removeDivineShield()
			return

		self.health += incremental
		if self.health > self.getMaxHealth():
			self.health = self.getMaxHealth()
		if self.health <= 0:
			self.die()
	def die(self):
		pos = self.getBoardPos()
		self.player.killMinion(self)
		# trigger deathrattle effect if any
		self.deathrattle(pos)
	def addTask(self,task,scheduledTime):
		if scheduledTime not in self.timerTasks:
			self.timerTasks[scheduledTime] = []
		self.timerTasks[scheduledTime].append(task)
	def doTasks(self):
		time = self.game.currentTime()
		if time in self.timerTasks:
			tasks = self.timerTasks[time]
			for task in tasks:
				task(self)
			del self.timerTasks[time]
	def isTaunt(self):
		if self.buffs['taunt'] or self.card.isTaunt():
			return True
		else:
			return False 
	def setTaunt(self):
		self.buffs['taunt'] = True
	def hasDivineShield(self):
		if self.buffs['divineShield'] or self.card.hasDivineShield():
			return True
		else:
			return False 
	def isStealth(self):
		if self.buffs['stealth'] or self.card.hasStealth():
			return True
		else:
			return False
	def silence(self):
		self.setSpellDamage(0)
		self.timerTasks = {}

		for key, value in self.buffs.iteritems():
			if value == True:
				self.buffs[key] = False
			elif value != 0:
				self.buffs[key] = 0

		self.card.silence()
	def getTargetMinAttack(self):
		return self.card.getTargetMinAttack()
	def getName(self):
		return self.card.getName()
