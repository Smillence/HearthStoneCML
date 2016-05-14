#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import random
import json

deck1 = [
['激活',0],
['激活',0],
['活体根须',1],
['成长',2],
['成长',2],
['豹骑士',2],
['愤怒',2],
['愤怒',2],
['咆哮',3],
['咆哮',3],
['王牌猎人',3],
['影子',3],
['影子',3],
['横扫',4],
['横扫',4],
['老鹿',4],
['老鹿',4],
['收割机',4],
['收割机',4],
['熊德',5],
['熊德',5],
['塞布',5],
['淤泥',5],
['蓝龙',5],
['自然之力',6],
['自然之力',6],
['大帝',6],
['古树',7],
['古树',7],
['博士',7],
]

deck2 = [
('激活',0),
('激活',0),
('活体根须',1),
('成长',2),
('成长',2),
('豹骑士',2),
('愤怒',2),
('愤怒',2),
('咆哮',3),
('咆哮',3),
('Big Game Hunter',3),
('影子',3),
('影子',3),
('横扫',4),
('横扫',4),
('老鹿',4),
('老鹿',4),
('收割机',4),
('收割机',4),
('熊德',5),
('熊德',5),
('塞布',5),
('淤泥',5),
('蓝龙',5),
('自然之力',6),
('自然之力',6),
('大帝',6),
('古树',7),
('古树',7),
('博士',7),
]

# deck22 = []

# with open('cards.json') as f:
# 	cards = json.load(f)

# for card in cards:
# 	card['name']


# 所有二费生物
twoManaMinions = [
['刃牙德鲁伊',2,1],
['电镀机械熊仔',2,2],
['豹骑士',2,3],
['热砂港狙击手',2,3],
['皇家雷象',3,2],
['食腐土狼',2,2],
['巫师学徒',3,2],
['碎雪机器人',2,3],
['英雄之魂',3,2],
['护盾机器人',2,2],
['银色保卫者',2,2],
['光明之泉',0,5],
['博物馆馆长',1,2],
['暗影打击装甲',2,3],
['缩小射线工程师',3,2],
['龙眠教官',1,4],
['地精理发',3,2],
['幽暗城勇士',3,2],
['独眼欺诈者',4,1],
['窃贼',2,2],
['耐心的刺客',1,1],
['迪菲亚头目',2,2],
['图腾魔像',3,4],
['活力图腾',0,3],
['火舌图腾',0,3],
['自动漩涡打击装置',3,2],
['小鬼骑士',3,2],
['愤怒卫士',4,3],
['痛苦女王',1,4],

]


# only for druid
class player:
	def __init__(self,name,deck):
		self.name = name
		self.health = 30
		self.heroPower = "变脸"
		self.mana = 0
		self.deck = deck
		self.hand = []
	def playHeroPower(self):
		self.health += 1


class game:
	def __init__(self,player1,player2):
		self.firstPlayer = player1
		self.secondPlayer = player2
		self.boardP1 = [] # board for player 1. (e.g. [('大帝(沉默)',5,5),('熊德(嘲讽)',4,6),('蓝龙(法伤+1)',4,4)])
		self.boardP2 = []
	def shuffle(self):
		random.shuffle(self.firstPlayer.deck)
		random.shuffle(self.secondPlayer.deck)
	def draw(self,player):# cannot handle fatigue right now
		card = player.deck.pop()
		player.hand.append(card)
		print player.name + ': You have drew card ' + card[0]
	def start(self):
		self.shuffle()
		self.initialSelect(self.firstPlayer)
		self.initialSelect(self.secondPlayer)
		self.startTurn(self.firstPlayer)
	def printStatus(self,player):
		if player == self.firstPlayer:
			component = self.secondPlayer
		else:
			component = self.firstPlayer
		print player.name + ': You have ' + str(player.mana) + ' mana, ' + str(player.health) + ' health.'
		print player.name + ': Your component has ' + str(component.mana) + \
		' mana, ' + str(component.health) + ' health, ' + str(len(component.hand)) + ' cards in hand.'
		handStr = player.name + ': You have '
		for i in range(len(player.hand)):
			handStr += '[' + str(i+1) + ']' + player.hand[i][0] + '(' +  str(player.hand[i][1]) + ')' + ' '
		print handStr
	def initialSelect(self,player):
		print player.name + ": please select cards from:"
		if player == self.firstPlayer:
			c1 = player.deck.pop()
			c2 = player.deck.pop()
			c3 = player.deck.pop()
			hand = [c1,c2,c3]
			print player.name + ': [1]:' + c1[0] + ', [2]:' + c2[0] + ', [3]:', c3[0]
			numbers = raw_input(player.name + ': Select the cards you dont want (e.g. 1,3):')
			if '1' in numbers:
				player.deck.append(c1)
				hand[0] = None
			if '2' in numbers:
				player.deck.append(c2)
				hand[1] = None
			if '3' in numbers:
				player.deck.append(c3)
				hand[2] = None
			random.shuffle(player.deck)
			for i in range(len(hand)):
				if hand[i] == None:
					hand[i] = player.deck.pop()
			player.hand = hand
			print player.name + ": Now you will start with cards: " + hand[0][0] + \
			', ' + hand[1][0] + ', ' + hand[2][0]
			print
		if player == self.secondPlayer:
			c1 = player.deck.pop()
			c2 = player.deck.pop()
			c3 = player.deck.pop()
			c4 = player.deck.pop()
			hand = [c1,c2,c3,c4]
			print player.name + ': [1]:' + c1[0] + ', [2]:' + c2[0] + ', [3]:', c3[0] + ', [4]:', c4[0]
			numbers = raw_input(player.name + ': Select the cards you dont want (e.g. 1,3):')
			if '1' in numbers:
				player.deck.append(c1)
				hand[0] = None
			if '2' in numbers:
				player.deck.append(c2)
				hand[1] = None
			if '3' in numbers:
				player.deck.append(c3)
				hand[2] = None
			if '4' in numbers:
				player.deck.append(c4)
				hand[3] = None
			random.shuffle(player.deck)
			for i in range(len(hand)):
				if hand[i] == None:
					hand[i] = player.deck.pop()
			player.hand = hand
			print player.name + ": Now you will start with cards: " + hand[0][0] + \
			', ' + hand[1][0] + ', ' + hand[2][0] + ', ' + hand[3][0]
			player.hand.append(['硬币',0])
			print

	def startTurn(self, player):
		if player == self.firstPlayer:
			board = self.boardP1
		else:
			board = self.boardP2

		# check for 影子
		for i in range(len(board)):
			if '影子' in board[i][0]:
				board[i][1] += 1
				board[i][2] += 1

		# grow mana at the start of each turn
		if player.mana < 10:
			player.mana += 1

		# draw card
		self.draw(player)

		print '\n' + player.name + ': Its your turn!'
		self.printStatus(player)


		# self.boardP1 = [['大帝(沉默)',5,5],['熊德(嘲讽)',4,6],['蓝龙(法伤+1)',4,4]]
		# self.boardP2 = [['熊德(嘲讽)',4,6],['蓝龙(法伤+1)',4,4]]
		self.printBoard(player)
		#plan = raw_input(player.name + ': what do you want to do?: (e.g. heroPower; play card 1 and 4; minion attack: 1->2, 2->face, 3->1)')
		while True:
			cmd = raw_input(player.name + ': please input command:')
			self.processCommand(player,cmd)
			if cmd.startswith('ET'):
				return
		
	def endTurn(self,player):
		if player == self.firstPlayer:
			board = self.boardP1
			component = self.secondPlayer
		else:
			board = self.boardP2
			component = self.firstPlayer
		
		for i in range(len(board)):
			# if 大帝 exists, decrease cost of all cards in hand by 1
			if '大帝' in board[i][0]:
				for i in range(len(player.hand)):
					if player.hand[i][1] > 0:
						player.hand[i][1] -= 1
			elif '活力图腾' in board[i][0]:
				player.health += 4
				if player.health > 30:
					player.health = 30

		self.startTurn(component)

	def processCommand(self, player, cmd):
		cmd = cmd.split()
		if cmd[0] == 'ET': # end turn
			self.endTurn(player)
		elif cmd[0] == 'PS': # print status
			self.printStatus(player)
		elif cmd[0] == 'PB': # print board
			self.printBoard(player)
		elif cmd[0] == 'DC': # draw card
			self.draw(player)
		elif cmd[0] == 'PC': # play card. e.g. P 2 3 - play the second and third cards in hand
			self.playCards(player,cmd[1:])
		elif cmd[0] == 'A': # add minion. e.g. A 大帝 5 5 1 L
			self.addMinion(player,cmd[1:])
		elif cmd[0] == 'MH': # modify health. e.g. MH U 1 5 - modify uppper board, the first minion's health to 5
			self.modifyHealth(player,cmd[1:])
		elif cmd[0] == 'K': # die
			self.kill(player,cmd[1:])
		print 

	def playCards(self,player,cmd):
		cmd = [int(x)-1 for x in cmd]
		cmd.sort(reverse=True)
		for pos in cmd:
			self.playCard(player,pos)

		self.printStatus(player)

	def playCard(self,player,pos):
		card = player.hand.pop(pos)
		if card[0] == '成长':
			if player.mana < 10:
				player.mana += 1
			else:
				self.draw(player)
	
	def addMinion(self,player,cmd):
		'''
		 typical command can be: 
		 	大帝 5 5 1 L
		 	大帝 5 5 1
		 	大帝 5 5
		 	Note: the last two parameter can be ignored, the default values are 1 and L
		'''
		if len(cmd) == 3:
			cmd.append('1')
			cmd.append('L')
		elif len(cmd) == 4:
			cmd.append('L')

		if (player == self.firstPlayer and cmd[4] == 'L') or (player == self.secondPlayer and cmd[4] == 'U'):
			board = self.boardP1
		else:
			board = self.boardP2

		minion = [cmd[0],int(cmd[1]),int(cmd[2])]
		pos = int(cmd[3]) - 1
		board.insert(pos, minion)

		# 豹骑士
		if minion[0] == '豹骑士' and player.mana < 10:
			player.mana += 1
	
	def modifyHealth(self,player,cmd):
		'''
		 typical command can be: 
		 	U 1 5 - modify uppper board, the first minion's health to 5
		 	L 0 29 - modify your hero's health to 29
		'''
		pos = int(cmd[1])
		health = int(cmd[2])
		if (player == self.firstPlayer and cmd[0] == 'L') or (player == self.secondPlayer and cmd[0] == 'U'):
			if pos == 0:
				self.firstPlayer.health = health
			else:
				self.boardP1[pos - 1][2] = health
		else:
			if pos == 0:
				self.secondPlayer.health = health
			else:
				self.boardP2[pos - 1][2] = health

	def kill(self,player,cmd):
		'''
		 typical command can be: 
		 	U 1 - kill the first minion in uppper board
		'''
		pos = int(cmd[1])
		if (player == self.firstPlayer and cmd[0] == 'L') or (player == self.secondPlayer and cmd[0] == 'U'):
			self.die(self.boardP1, pos - 1)
		else:
			self.die(self.boardP2, pos - 1)
	def die(self,board,pos):
		minion = board.pop(pos)
		if '沉默' in minion[0]:
			return

		# 豹骑士
		if minion[0] == '豹骑士':
			if board == self.boardP1:
				if self.firstPlayer.mana > 0:
					self.firstPlayer.mana -= 1
			else:
				if self.secondPlayer.mana > 0:
					self.secondPlayer.mana -= 1
		# 收割机
		elif minion[0].startswith('收割机'):
			minion = random.choice(twoManaMinions)
			board.insert(pos, minion)

		# 淤泥
		elif minion[0].startswith('淤泥'):
			minion = ['小淤泥(嘲讽)',1,2]
			board.insert(pos, minion)

		# 小炸弹
		elif minion[0].startswith('小炸弹'):
			print(randint(1,4))
			pass


		

	def printBoard(self, player):
		print player.name + ': Below is the board:'
		print "************************************************************************************************"
		if player == self.firstPlayer:
			self.printBoardHelper(self.boardP2)
			print "************************************************************************************************"
			self.printBoardHelper(self.boardP1)
		else:
			self.printBoardHelper(self.boardP1)
			print "************************************************************************************************"
			self.printBoardHelper(self.boardP2)
		print "************************************************************************************************"
	def printBoardHelper(self,board):
		line1 = ''
		line2 = ''
		for i in range(len(board)):
			line1 += '[{0:^}]{1:^25}'.format(str(i+1),board[i][0])
			line2 += '{:^25}'.format(str(board[i][1])+' '+str(board[i][2]))
		print line1
		print line2



if __name__ == '__main__':
	p1 = player("zzd",deck1)
	p2 = player("smi",deck2)
	g = game(p1,p2) 
	g.start()
	#print p1.deck[0]