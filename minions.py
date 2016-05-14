#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from Minion import Minion
import utils
import json
import random

with open('data/cards.json') as f:
	allCards = json.load(f)
with open('data/cards.collectible.json') as f:
	allCardsCollectible = json.load(f)

# Brann Bronzebeard
class LOE_077(Minion):
	pass 

# Darnassus Aspirant
class AT_038(Minion):
	def battlecry(self,pos):
		self.player.modifyMaxMana(1)
		return self,pos
	def deathrattle(self,pos):
		self.player.modifyMaxMana(-1)
		self.player.modifyMana(-1)

# Lance Carrier
class AT_084(Minion):
	def battlecry(self,pos):
		if self.target == None:
			self.target = utils.selectFriendlyMinion(self.player)
		if self.target != None:
			self.target.modifyAttack(2)
		return self,pos 

# Imp Gang Boss
class BRM_006(Minion):
	def modifyHealth(self,incremental):
		preHealth = self.getHealth()
		super(self.__class__, self).modifyHealth(incremental)
		if self.getHealth() < preHealth:
			for cardData in allCards:
				if cardData['id'] == 'BRM_006t':
					card = utils.createCard(cardData,self.player)
					imp = Minion(card,self.player,self.game)
					self.player.insertToBoard(imp,self.getBoardPos() + 1)
					return

# Emperor Thaurissan
class BRM_028(Minion):
	def endTurn(self):
		for card in self.player.getHand():
			card.modifyCost(-1)

# Voidwalker
class CS2_065(Minion):
	pass

# Abusive Sergeant
class CS2_188(Minion):
	def battlecry(self,pos):
		if self.target == None:
			self.target = utils.selectMinion(self.player)
		if self.target != None:
			self.target.modifyAttack(2)

			def minionTask(minion):
				minion.modifyAttack(-2)

			self.target.addTask(minionTask,self.game.currentTime() + 1)
		return self,pos 

# Ironbeak Owl
class CS2_203(Minion):
	def battlecry(self,pos):
		if self.target == None:
			self.target = utils.selectMinion(self.player)
		if self.target != None:
			utils.silence(self.target)
		return self,pos

# Big Game Hunter
class EX1_005(Minion):
	def battlecry(self,pos):
		if self.target == None:
			minAttack = self.getTargetMinAttack()
			self.target = utils.selectMinionWithMinAttack(self.player,minAttack)
			if self.target != None:
				self.target.die()
		return self,pos

# Argent Squire
class EX1_008(Minion):
	pass

# Defender of Argus
class EX1_093(Minion):
	def battlecry(self,pos):
		if pos > 1:
			leftMinion = self.game.getTarget(self.player,['L',str(pos-1)])

			leftMinion.setTaunt()
			leftMinion.modifyAttack(1)
			leftMinion.modifyMaxHealth(1)
			leftMinion.modifyHealth(1)

		if pos <= self.player.totalMinionNum():
			rightMinion = self.game.getTarget(self.player,['L',str(pos)])
			rightMinion.setTaunt()
			rightMinion.modifyAttack(1)
			rightMinion.modifyMaxHealth(1)
			rightMinion.modifyHealth(1)
		return self,pos
	
# Loot Hoarder
class EX1_096(Minion):
	def deathrattle(self,pos):
		self.player.draw()
 	
# Leeroy Jenkins
class EX1_116(Minion):
	def battlecry(self,pos):
		for cardData in allCards:
			if cardData['id'] == 'EX1_116t':
				card_1 = utils.createCard(cardData,self.player)
				card_2 = utils.createCard(cardData,self.player)
				owner = self.player.getComponent()
				whelp_1 = Minion(card_1,owner,self.game)
				whelp_2 = Minion(card_2,owner,self.game)
				whelpPos = owner.totalMinionNum() + 1
				owner.insertToBoard(whelp_1,whelpPos)
				owner.insertToBoard(whelp_2,whelpPos)
				break
		return self,pos

# Druid of the Claw
class EX1_165(Minion):
	def chooseOne(self):
		cmd = int(raw_input(self.player.getName() +\
		 ': Choose One: [1]Charge; or [2]+2 Health and Taunt: '))

		minion = None
		if cmd == 1:
			for cardData in allCards:
				if cardData['id'] == 'EX1_165t1':
					card = utils.createCard(cardData,self.player)
					minion = Minion(card,self.player,self.game)
		elif cmd == 2:
			for cardData in allCards:
				if cardData['id'] == 'EX1_165t2':
					card = utils.createCard(cardData,self.player)
					minion = Minion(card,self.player,self.game)
		return minion

# Keeper of the Grove
class EX1_166(Minion):
	def chooseOne(self):
		damage = 2
		cmd = int(raw_input(self.player.getName() + ': Choose One: [1]Deal ' + \
			str(damage) + ' damage; or [2]Silence a minion: '))

		if cmd == 1:
			target = utils.selectTarget(self.player)
			target.modifyHealth(-damage)
		elif cmd == 2:
			minion = utils.selectMinion(self.player)
			if minion != None:
				utils.silence(minion)
		return self

# Azure Drake
class EX1_284(Minion):
	def battlecry(self,pos):
		self.spellDamage = 1
		self.player.draw()
		return self,pos

# Sea Giant
class EX1_586(Minion):
	pass

# Treant (Charge. At the end of the turn, destroy this minion)
class EX1_tk9(Minion):
	def __init__(self,card,player,game):
		super(self.__class__, self).__init__(card,player,game)

		def task(game):
			self.die()
		self.addTask(task,game.currentTime() + 1)

# Haunted Creeper
class FP1_002(Minion):
	def deathrattle(self,pos):
		for cardData in allCards:
			if cardData['id'] == 'FP1_002t':
				card_1 = utils.createCard(cardData,self.player)
				card_2 = utils.createCard(cardData,self.player)
				spider_1 = Minion(card_1,self.player,self.game)
				spider_2 = Minion(card_2,self.player,self.game)
				self.player.insertToBoard(spider_1,pos)
				self.player.insertToBoard(spider_2,pos)
				return

# Shade of Naxxramas
class FP1_005(Minion):
	def startTurn(self):
		self.modifyAttack(1)
		self.modifyMaxHealth(1)
		self.modifyHealth(1)

# Nerubian Egg
class FP1_007(Minion):
	def deathrattle(self,pos):
		for cardData in allCards:
			if cardData['id'] == 'FP1_007t':
				card = utils.createCard(cardData,self.player)
				nerubian = Minion(card,self.player,self.game)
				self.player.insertToBoard(nerubian,pos)
				return

# Sludge Belcher
class FP1_012(Minion):
	def deathrattle(self,pos):
		for cardData in allCards:
			if cardData['id'] == 'FP1_012t':
				card = utils.createCard(cardData,self.player)
				minion = Minion(card,self.player,self.game)
				self.player.insertToBoard(minion,pos)
				return

# Unstable Ghoul
class FP1_024(Minion):
	def deathrattle(self,pos):
		for minion in self.game.getFirstPlayer().getAllMinions() + \
			self.game.getSecondPlayer().getAllMinions():
			minion.modifyHealth(-1)

# Loatheb
class FP1_030(Minion):
	def battlecry(self,pos):
		scheduledTime = self.game.currentTime() + 3
		component = self.player.getComponent()
		component.modifySpellCostAddOn(5)

		def task(game):
			component.modifySpellCostAddOn(-5)

		self.game.addTask(task,scheduledTime)

		return self,pos

# Vitality Totem
class GVG_039(Minion):
	def endTurn(self):
		self.player.modifyHealth(4)

# Shielded Minibot
class GVG_058(Minion):
	pass

# Gilblin Stalker
class GVG_081(Minion):
	pass

# Piloted Shredder
class GVG_096(Minion):
	def deathrattle(self,pos):

		#### This is for testing use ####
		# for cardData in allCardsCollectible:
		# 	if cardData['id'] == 'GVG_058':
		#       card = utils.createCard(cardData,self.player)
		# 		minion = GVG_058(card,self.player,self.game)
		#       self.player.insertToBoard(minion,self.getBoardPos())
		# 		return

		cardNamePool = []
		for card in allCardsCollectible:
			if 'cost' in card and card['cost'] == 2 and card['type'] == \
				'MINION' and card['id'] in globals():
				cardNamePool.append(card)
			
		cardData = random.choice(cardNamePool)	
		card = utils.createCard(cardData,self.player)
		minion = globals()[cardData['id']](card,self.player,self.game)
		self.player.insertToBoard(minion,pos)
		return

# Dr. Boom
class GVG_110(Minion):
	def battlecry(self,pos):
		for cardData in allCards:
			if cardData['id'] == 'GVG_110t':
				card_1 = utils.createCard(cardData,self.player)
				card_2 = utils.createCard(cardData,self.player)
				boom_1 = GVG_110t(card_1,self.player,self.game)
				boom_2 = GVG_110t(card_2,self.player,self.game)
				self.player.insertToBoard(boom_1,pos)
				self.player.insertToBoard(boom_2,pos+1)
				break
		return self,pos+1

# Boom Bot
class GVG_110t(Minion):
	def deathrattle(self,pos):
		numberOfEnemies = self.player.getComponent().totalMinionNum() + 1

		target = random.randint(0,numberOfEnemies-1)
		damage = random.randint(1,4)

		command = ['U',str(target),str(-damage)]
		self.game.modifyHealth(self.player, command)

# Dark Peddler
class LOE_023(Minion):
	def battlecry(self,pos):
		return self,pos

# Ancient of Lore
class NEW1_008(Minion):
	def chooseOne(self):
		cmd = int(raw_input(self.player.getName() +\
		 ': Choose One: [1]Draw a card; or [2]Restore 5 Health: '))

		if cmd == 1:
			self.player.draw()
		elif cmd == 2:
			target = utils.selectTarget(self.player)
			target.modifyHealth(5)
		return self
