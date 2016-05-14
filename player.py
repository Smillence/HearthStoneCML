#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import json
import copy
import sys
from utils import *
import random

with open('data/cards.collectible.json') as f:
	allCardsCollectible = json.load(f)

class player(object):
	def __init__(self,name,deckPath):
		self.heroPowerCost = 2
		self.name = name
		self.maxHealth = 30
		self.health = self.maxHealth
		self.attack = 0
		self.maxMana = 0
		self.mana = self.maxMana
		self.hand = [] # [card1,card2, ...]
		self.board = [] # [minion1, minion2, ...]
		self.spellDamage = 0
		self.buffs = {'attack':0,'armor':0,'spellDamage':0, 'spellCostAddOn':0}
		self.game = None

		self.deck = []
		self.readDeck(deckPath)
	def readDeck(self,deckPath):
		cardNames = []
		with open(deckPath) as f:
			cardNames = f.readlines()
		cardNames = [x.strip('\n') for x in cardNames]

		for card in allCardsCollectible:
			for cardName in cardNames:
				if card['name'] == cardName:
					cardInstance = createCard(card,self)
					self.deck.append(cardInstance)
	def getAttack(self):
		atk = self.attack + self.buffs['attack']
		if atk < 0:
			atk = 0
		return atk
	def getHealth(self):
		return self.health
	def getArmor(self):
		return self.buffs['armor']
	def getMaxHealth(self):
		return self.maxHealth
	def getSpellDamage(self):
		return self.spellDamage + self.buffs['spellDamage']
	def getSpellCostAddOn(self):
		return self.buffs['spellCostAddOn']
	def modifyHealth(self,incremental):
		if incremental < 0:
			self.buffs['armor'] += incremental
			if self.buffs['armor'] < 0:
				self.health += self.buffs['armor']
				self.buffs['armor'] = 0
		else:
			self.health += incremental
			if self.health > self.getMaxHealth():
				self.health = self.getMaxHealth()

		if self.health <= 0:
			print self.game.getComponent(self).getName(), 'won the game!'
			sys.exit()
	def heroPower(self):
		self.mana -= 2
	def getComponent(self):
		return self.game.getComponent(self)
	def modifyArmor(self,incremental):
		self.buffs['armor'] += incremental
	def modifyAttack(self,incremental):
		self.buffs['attack'] += incremental
	def modifySpellDamage(self,incremental):
		self.buffs['spellDamage'] += incremental
	def modifySpellCostAddOn(self,incremental):
		self.buffs['spellCostAddOn'] += incremental
	def totalMinionNum(self):
		return len(self.board)
	def killMinion(self,minion):
		self.board.remove(minion)
	def getName(self):
		return self.name
	def insertToBoard(self,minion,pos):
		self.board.insert(pos-1,minion) 
	def modifyMana(self,incremental):
		self.mana += incremental
		if self.mana > 10:
			self.mana = 10
	def modifyMaxMana(self,incremental):
		self.maxMana += incremental
		if self.maxMana > 10:
			self.maxMana = 10
		if self.maxMana < 0:
			self.maxMana = 0
	def getMana(self):
		return self.mana
	def getMaxMana(self):
		return self.maxMana
	def refillMana(self):
		self.mana = self.getMaxMana()
	def getAllMinions(self):
		return self.board
	def getMinionAtPos(self,pos):
		return self.board[pos-1]
	def getHand(self):
		return self.hand
	def getCardsInHandNum(self):
		return len(self.hand)
	def draw(self):# cannot handle fatigue right now
		card = self.popCardFromDeck()
		self.hand.append(card)
		print self.getName() + ': You have drew card ' + card.getName()
	def shuffle(self):
		random.shuffle(self.deck)
	def popCardFromDeck(self):
		return self.deck.pop()
	def popCardFromHand(self,pos):
		return self.hand.pop(pos)
	def addToDeck(self,card):
		self.deck.append(card)
		self.shuffle()
	def initHand(self,cards):
		self.hand = cards
	def addToHand(self,card):
		self.hand.append(card)

