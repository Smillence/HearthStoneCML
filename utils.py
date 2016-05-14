#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from card import *

def silence(minion):

	def doNothing(pos):
		pass
	minion.deathrattle = doNothing

	minion.silence()

def createCard(data,player):
	if 'card_' + data['id'] in globals():
		return globals()['card_' + data['id']](data,player)
	else:
		return card(data,player)

def selectTarget(player):
	targetCmd = raw_input(player.getName() + \
		': Select a target(e.g. L 0): ')
	target = player.game.getTarget(player,targetCmd.split())
	return target

def selectMinion(player):
	target = None
	if player.totalMinionNum() + \
		player.getComponent().totalMinionNum() > 0:
		targetCmd = raw_input(player.getName() + \
			': Select a minion(e.g. L 1): ')
		target = player.game.getTarget(player,targetCmd.split())
	return target

def selectFriendlyMinion(player):
	target = None
	if player.totalMinionNum() > 0:
		targetCmd = raw_input(player.getName() + \
			': Select a friendly minion(e.g. 1): ')
		target = player.game.getTarget(player,['L',targetCmd])
	return target

def selectEnemyTarget(player):
	targetCmd = raw_input(player.getName() + \
		': Select an enemy(e.g. 0): ')
	target = player.game.getTarget(player,['U',targetCmd])
	return target

def selectMinionWithMinAttack(player,minAttack):
	targetExist = False
	target = None

	for minion in player.game.getFirstPlayer().getAllMinions() + \
		player.game.getSecondPlayer().getAllMinions():
		if minion.getAttack() >= minAttack:
			targetExist = True
			break
			
	if targetExist:
		target = selectMinion(player)
	return target
