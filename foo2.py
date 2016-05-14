#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import random
import json
import sys
from minions import *
from spells import *
import utils
from careers import *
import copy

# ### For testing piloted shredder ####
# for card in allCardsCollectible:
# 	if 'cost' in card and card['cost'] == 2 and card['type'] == 'MINION':
# 		print str(card['attack'])
# 		#print '# ' + card['name'] + str(card['attack']) + str(card['health'])
# 		#print 'class ' + card['id'] + '(Minion):'

# sys.exit()


with open('data/cards.json') as f:
	allCards = json.load(f)

class game(object):
	def __init__(self,player1,player2):
		self.firstPlayer = player1
		self.secondPlayer = player2
		player1.game = self
		player2.game = self
		# for timers; increase by one whenever a turn starts or ends
		self.time = 0
		self.timerTasks = {} # e.g. {13:[t1,t2], 25:[t3]}
	def start(self):
		self.firstPlayer.shuffle()
		self.secondPlayer.shuffle()
		self.initialSelect()
		self.startTurn(self.firstPlayer)
	def printStatus(self,player):
		if player == self.firstPlayer:
			component = self.secondPlayer
		else:
			component = self.firstPlayer
		print player.getName() + ': You have ' + str(player.getMana()) + '/'+ \
			str(player.getMaxMana()) + ' mana, ' + str(player.getHealth()) + \
			' health, ' + str(player.getArmor()) + ' armor, ' + \
			str(player.getAttack()) + ' attack.'
		print player.getName() + ': Your component has ' + \
			str(component.getMaxMana()) + ' mana, ' + \
			str(component.getHealth()) + ' health, ' + \
			str(component.getArmor()) + ' armor, ' + \
			str(component.getCardsInHandNum()) + ' cards in hand.'

		handStr = player.getName() + ': You have '
		for i in range(player.getCardsInHandNum()):
			card = player.getHand()[i]
			handStr += '[' + str(i+1) + ']' + card.getName() + '(' +  \
				str(card.getCost()) + ')' + ' '
		if player.getCardsInHandNum() == 0:
			handStr += 'no cards in hand!'
		print handStr
	def printBoard(self, player):
		print player.getName() + ': Below is the board:'
		print "**************************************************************"+\
			"*********************************"
		if player == self.firstPlayer:
			self.printBoardHelper(self.secondPlayer)
			print "**********************************************************"+\
				"***************************************"
			self.printBoardHelper(player)
		else:
			self.printBoardHelper(self.firstPlayer)
			print "**********************************************************"+\
				"***************************************"
			self.printBoardHelper(player)
		print "**************************************************************"+\
			"*********************************"
	def printBoardHelper(self,player):
		line1 = ''
		line2 = ''
		for minion in player.getAllMinions():
			buffStr = ''
			if minion.isTaunt():
				buffStr += '(T)'
			if minion.hasDivineShield():
				buffStr += '(D)'
			if minion.isStealth():
				buffStr += '(S)'

			line1 += '[{0:^}]{1:^25}'.format(str(minion.getBoardPos()), \
				minion.card.getName() + buffStr)

			line2 += '{:^25}'.format(str(minion.getAttack())+' '\
				+str(minion.getHealth())+'/'+str(minion.getMaxHealth()))
		print line1
		print line2
	def initialSelectHelper(self,player,numOfCardsToSelect):
		print player.getName() + ": please select cards from:"

		hand = []
		for i in range(numOfCardsToSelect):
			hand.append(player.popCardFromDeck())
		selectStr = player.getName() + ': '

		for i in range(len(hand)):
			card = hand[i]
			selectStr += '[' + str(i+1) + ']:' + card.getName() + ' '

		print  selectStr
		numbers = raw_input(player.getName() + \
			': Select the cards you dont want (e.g. 1,3):').split()

		# shuffle the cards not desired to the deck
		for num in numbers:
			index = int(num) - 1
			player.addToDeck(hand[index])
			hand[index] = None

		# re-draw cards from the deck
		for i in range(len(hand)):
			if hand[i] == None:
				hand[i] = player.popCardFromDeck()

		player.initHand(hand)

		handStr = player.getName() + ': Now you will start with cards: '
		playerHand = player.getHand()
		for i in range(len(playerHand)):
			card = playerHand[i]
			handStr += '[' + str(i+1) + ']' + card.getName() + '(' +  \
				str(card.getCost()) + ')' + ' '
		print handStr + '\n'

	def initialSelect(self):
		self.initialSelectHelper(self.firstPlayer,3)
		self.initialSelectHelper(self.secondPlayer,4)
		# add coin to the second component's hand
		for cardData in allCards:
			if cardData['id'] == 'GAME_005':
				card = utils.createCard(cardData,self.secondPlayer)
				self.secondPlayer.addToHand(card)
				break			

	def startTurn(self, player):
		self.time += 1
		self.doTasks()

		# grow mana at the start of each turn
		player.modifyMaxMana(1)

		# refill mana
		player.refillMana()

		# draw card
		player.draw()

		for minion in player.getComponent().getAllMinions():
			minion.doTasks()

		# start turn effects for certain minoins
		boardCopy = player.getAllMinions()[:]
		for minion in boardCopy:
			minion.doTasks()
			minion.startTurn()

		# print status and board information
		print player.getName() + ': It\'s your turn!'
		self.printStatus(player)
		self.printBoard(player)

		# listen to command input
		while True:
			cmd = raw_input(player.getName() + ': please input command:')
			self.processCommand(player,cmd)
			if cmd.startswith('ET'):
				return
		
	def doTasks(self):
		if self.time in self.timerTasks:
			tasks = self.timerTasks[self.time]
			for task in tasks:
				task(self)
			del self.timerTasks[self.time]

	def endTurn(self,player):
		self.time += 1
		self.doTasks()

		for minion in player.getComponent().getAllMinions():
			minion.doTasks()

		# end turn effects for certain minoins
		boardCopy = player.getAllMinions()[:]
		for minion in boardCopy:
			minion.doTasks()
			minion.endTurn()

		print
		self.startTurn(self.getComponent(player))
		

	def processCommand(self, player, cmd):
		cmd = cmd.split()
		if cmd[0] == 'ET': # end turn
			self.endTurn(player)
		elif cmd[0] == 'PS': # print status
			self.printStatus(player)
		elif cmd[0] == 'PB': # print board
			self.printBoard(player)
		elif cmd[0] == 'DC': # draw card
			player.draw()
		# play card. e.g. P 2 3 - play the second and third cards in hand
		elif cmd[0] == 'PC': 
			self.playCards(player,cmd[1:])
		# modify health. e.g. MH U 1 1 - increase uppper board, 
		# 	the first minion's health by 1
		elif cmd[0] == 'MH': 
			self.modifyHealth(player,cmd[1:])
		elif cmd[0] == 'K': # kill minion
			self.kill(player,cmd[1:])
		# attack. A 2 0 e.g. your second minion attack the hero
		elif cmd[0] == 'A': 
			self.attack(player,cmd[1:])
		# play hero power
		elif cmd[0] == 'H':
			player.heroPower()
		# play a minion card to a specified position
		elif cmd[0] == 'PM':
			self.playCard(player,int(cmd[1])-1,int(cmd[2]))

		self.printBoard(player)
		self.printStatus(player)

	def playCards(self,player,cmd):
		cmd = [int(x)-1 for x in cmd]
		cmd.sort(reverse=True)
		for pos in cmd:
			self.playCard(player,pos)

	def playCard(self,player,pos,minionPos=1):
		card = player.popCardFromHand(pos)

		# deduce mana
		player.modifyMana(-card.getCost())

		if card.isMinion():
			# ToDo: for now always add to the left of the board
			self.addMinionFromCard(player,card,minionPos)
		elif card.isSpell():
			globals()[card.getID()](card,player,self)

	# add minion object to board from hand
	def addMinionFromCard(self,player,card,pos=1):
		minion = globals()[card.getID()](card,player,self)

		if card.isBattlecry():
			for m in player.getAllMinions():
				if m.getName() == 'Brann Bronzebeard':
					minion.battlecry(pos)
					break
			minion,pos = minion.battlecry(pos)
		elif card.isChooseOne():
			minion = minion.chooseOne()
			pos = player.totalMinionNum()+1

		player.insertToBoard(minion,pos)

	def modifyHealth(self,player,cmd):
		'''
		 typical command can be: 
		 	U 1 -1 - deduce uppper board, the first minion's health by 1
		 	L 0 4 - increase your hero's health by 4
		'''
		pos = int(cmd[1])
		incremental = int(cmd[2])

		target = self.getTarget(player,cmd[:-1])
		target.modifyHealth(incremental)

	# cmd is a list of strings. e.g. ['U','1']
	def kill(self,player,cmd):
		'''
		 typical command can be: 
		 	U 1 - kill the first minion in uppper board
		'''
		minion = self.getTarget(player,cmd)
		minion.die()
	
	# command can be e.g. ['U','0']
	def getTarget(self,player,cmd):
		pos = int(cmd[1])
		if (player == self.firstPlayer and cmd[0] == 'L') or \
			(player == self.secondPlayer and cmd[0] == 'U'):
			if pos == 0:
				return self.firstPlayer
			else:
				return self.firstPlayer.getMinionAtPos(pos)
		else:
			if pos == 0:
				return self.secondPlayer
			else:
				return self.secondPlayer.getMinionAtPos(pos)

	def getComponent(self,player):
		if player == self.firstPlayer:
			return self.secondPlayer
		else:
			return self.firstPlayer

	def getSpellDamage(self,player):
		spellDamage = player.getSpellDamage()
		for minion in player.getAllMinions():
			spellDamage += minion.getSpellDamage()
		return spellDamage

	def attack(self,player,cmd):
		attackerNum = cmd[0]
		targetNum = cmd[1]

		attacker = self.getTarget(player,['L',attackerNum])
		target = self.getTarget(player,['U',targetNum])

		self.modifyHealth(player,['U',targetNum,str(-attacker.getAttack())],)
		self.modifyHealth(player,['L',attackerNum,str(-target.getAttack())],)

	def addTask(self,task,scheduledTime):
		if scheduledTime not in self.timerTasks:
			self.timerTasks[scheduledTime] = []
		self.timerTasks[scheduledTime].append(task)
	def currentTime(self):
		return self.time
	def getFirstPlayer(self):
		return self.firstPlayer
	def getSecondPlayer(self):
		return self.secondPlayer




if __name__ == '__main__':
	p1 = druid("zzd","decks/midRangeDruid.txt")
	p2 = druid("smi","decks/midRangeDruid.txt")#test

	# p1 = warlock("zzd","decks/zoolock.txt")
	# p2 = warlock("smi","decks/zoolock.txt")

	g = game(p1,p2) 
	g.start()
