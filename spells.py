#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import json
from Minion import Minion
from minions import *
import random
import utils

with open('data/cards.json') as f:
	allCards = json.load(f)

# Living Roots
def AT_037(card,player,game):
	damage = 2 + game.getSpellDamage(player)
	cmd = int(raw_input(player.getName() + ': Choose One: [1]Deal '+ str(damage) +
		' damage; or [2]Summon two 1/1 Saplings: '))
	if cmd == 1:
		target = utils.selectTarget(player)
		target.modifyHealth(-damage)
	elif cmd == 2:
		for cardData in allCards:
			if cardData['id'] == 'AT_037t':
				card_1 = utils.createCard(cardData,player)
				card_2 = utils.createCard(cardData,player)
				sapling_1 = Minion(card_1,player,game)
				sapling_2 = Minion(card_2,player,game)
				player.insertToBoard(sapling_1,player.totalMinionNum()+1)
				player.insertToBoard(sapling_2,player.totalMinionNum()+1)

# Savage Roar
def CS2_011(card,player,game):
	scheduledTime = game.currentTime() + 1

	# add attack for the player
	player.modifyAttack(2)
	def task(game):
		player.modifyAttack(-2)

	game.addTask(task,scheduledTime)

	# add attack for the minions
	def minionTask(minion):
		minion.modifyAttack(-2)

	for minion in player.getAllMinions():
		minion.modifyAttack(2)
		minion.addTask(minionTask,scheduledTime)

# Swipe
def CS2_012(card,player,game):
	damage_1 = 4 + game.getSpellDamage(player)
	damage_2 = 1 + game.getSpellDamage(player)

	enemy = utils.selectEnemyTarget(player)
	enemy.modifyHealth(-(damage_1-damage_2))

	numberOfEnemies = player.getComponent().totalMinionNum() + 1
	targets = []
	for i in range(numberOfEnemies):
		command = ['U',str(i)]
		targets.append(game.getTarget(player,command))
	for target in targets:
		target.modifyHealth(-damage_2)

# Wild Growth
def CS2_013(card,player,game):
	if player.getMaxMana() == 10:
		player.draw()
	else:
		player.modifyMaxMana(1)

# Wrath
def EX1_154(card,player,game):
	damage_1 = 3 + game.getSpellDamage(player)
	damage_2 = 1 + game.getSpellDamage(player)
	cmd = int(raw_input(player.getName() + ': Choose One: [1]Deal ' + str(damage_1) +
		' damage to a minion; or [2]' + str(damage_2) +' damage and draw a card: '))
	if cmd == 1:
		target = utils.selectMinion(player)
		target.modifyHealth(-damage_1)
	elif cmd == 2:
		target = utils.selectMinion(player)
		target.modifyHealth(-damage_2)
		player.draw()

# Innervate
def EX1_169(card,player,game):
	player.modifyMana(2)

# Power Overwhelming
def EX1_316(card,player,game):

	minion = utils.selectFriendlyMinion(player)

	minion.modifyAttack(4)
	minion.modifyMaxHealth(4)
	minion.modifyHealth(4)

	def task(minion):
		minion.die()

	minion.addTask(task,game.currentTime()+1)

# Force of Nature
def EX1_571(card,player,game):
	pos = player.totalMinionNum() + 1
	for cardData in allCards:
		if cardData['id'] == 'EX1_tk9':
			card_1 = utils.createCard(cardData,player)
			card_2 = utils.createCard(cardData,player)
			card_3 = utils.createCard(cardData,player)
			treant_1 = EX1_tk9(card_1,player,game)
			treant_2 = EX1_tk9(card_2,player,game)
			treant_3 = EX1_tk9(card_3,player,game)
			player.insertToBoard(treant_1,pos)
			player.insertToBoard(treant_2,pos)
			player.insertToBoard(treant_3,pos)
			return
	
# The Coin
def GAME_005(card,player,game):
	player.modifyMana(1)

# Imp-losion
def GVG_045(card,player,game):
	damage = random.randint(2,4) + game.getSpellDamage(player)

	target = utils.selectMinion(player)
	target.modifyHealth(-damage)
	
	for cardData in allCards:
		if cardData['id'] == 'GVG_045t':
			for i in range(damage):
				card = utils.createCard(cardData,player)
				imp = Minion(card,player,game)
				player.insertToBoard(imp,player.totalMinionNum() + 1)
			return
	