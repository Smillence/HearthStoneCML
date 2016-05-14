#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import copy

class card(object):
	def __init__(self,data,player):# data is a dictionary
		self.data = copy.deepcopy(data)
		self.player = player
	def getID(self):
		return self.data['id']
	def getType(self):
		return self.data['type']
	def isSpell(self):
		if self.getType() == 'SPELL':
			return True
		else:
			return False
	def isBattlecry(self):
		if 'mechanics' in self.data and 'BATTLECRY' in self.data['mechanics']:
			return True
		else:
			return False
	def isChooseOne(self):
		if 'text' in self.data and 'Choose One' in self.data['text']:
			return True
		else:
			return False
	def isMinion(self):
		if self.getType() == 'MINION':
			return True
		else:
			return False
	def getCost(self):
		cost = self.data['cost']

		if self.isSpell():
			cost += self.player.getSpellCostAddOn()
			
		if cost < 0:
			return 0
		else:
			return cost
	def getName(self):
		return self.data['name']
	def getAttack(self):
		return self.data['attack']
	def getHealth(self):
		return self.data['health']
	def hasStealth(self):
		if 'mechanics' in self.data and 'STEALTH' in self.data['mechanics']:
			return True
		else:
			return False
	def hasDivineShield(self):
		if 'mechanics' in self.data and 'DIVINE_SHIELD' in self.data['mechanics']:
			return True
		else:
			return False
	def isTaunt(self):
		if 'mechanics' in self.data and 'TAUNT' in self.data['mechanics']:
			return True
		else:
			return False
	def removeDivineShield(self):
		if self.hasDivineShield():
			self.data['mechanics'].remove('DIVINE_SHIELD')
	def silence(self):
		self.data.pop("mechanics", None)
	def modifyCost(self,incremental):
		self.data['cost'] += incremental
	def getTargetMinAttack(self):
		return self.data['playRequirements']['REQ_TARGET_MIN_ATTACK']

class card_EX1_586(card):
	def getCost(self):
		newCost = self.data['cost'] - self.player.totalMinionNum() - \
			self.player.getComponent().totalMinionNum()
		if newCost < 0:
			newCost = 0
		return newCost