#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from player import player

class druid(player):
	def heroPower(self):
		super(self.__class__, self).heroPower()
		self.modifyArmor(1)
		self.modifyAttack(1)

		def task(game):
			self.modifyAttack(-1)

		self.game.addTask(task,self.game.currentTime()+1)

class warlock(player):
	def __init__(self,name,deck):
		super(self.__class__, self).__init__(name,deck)
		self.healthCostHeroPower = 2
	def heroPower(self):
		super(self.__class__, self).heroPower()
		self.draw()
		self.modifyHealth(-self.healthCostHeroPower)
