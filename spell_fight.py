import os, sys
from bs_DND_spells import *
from random import randint
import csv


def dice_combos():
	D_list = ['d4', 'd6', 'd8', 'd10', 'd12', 'd20', 'd100']
	number_list = []
	for i in range(1, 21):
		number_list.append(str(i))
	dice_combo_list = []
	for die in D_list:
		for num in number_list:
			dice_combo_list.append(num + die)
	return dice_combo_list

def attack(spell_name):
	r = csv.reader(open('DND_spell_attacks.csv'))
	lines = list(r)
	attack_roll = roll_die('1d20')
	damage = 0
	if attack_roll > 11:
		for spell in lines:
			if spell[0] == spell_name:
				damage = roll_die(spell[1])

	return damage, attack_roll

def save_attacks():
	spells = get_list_spells()
	dice_list = dice_combos()
	header = ['Spell', 'Damage', 'Description']
	template_spell = {
	'Spell': '',
	'Damage': '',
	'Description': ''
	}
	with open('DND_spell_attacks.csv', mode='w') as csv_spell:
		writer = csv.DictWriter(csv_spell, fieldnames=header)
		writer.writeheader()
		for spell in spells:
			spell_desc = return_spell(spell)['Description']
			desc_list = spell_desc.split('.')
			for sentence in desc_list:
				for die in dice_list:
					if die in sentence and template_spell['Spell'] != spell:
						template_spell['Spell'] = spell
						template_spell['Damage'] = die
						template_spell['Description'] = sentence
						writer.writerow(template_spell)

def roll_die(die):
	die_nums = die.split('d')
	total = 0
	for i in range(int(die_nums[0])):
		total += randint(1, int(die_nums[1]))
	return total

def saving_throw():
	result = roll_die('1d20')
	if result >= 10:
		return result, True
	else:
		return result, False

def init_players(players):
	template_dict = {
	'Name' : None,
	'HP' : 100,
	'Max HP' : 100,
	'Death Throw Fails' : 0,
	'Death Throw Successes' : 0,
	'Dead' : 0,
	'Armor' : 12,
	'Unconcious' : 0,
	'Last' : 0
	}
	header = template_dict.keys()
	with open('DND_player_data.csv', mode="w") as csv_DND:
		writer = csv.DictWriter(csv_DND, fieldnames=header)
		writer.writeheader()
		for player in players:
			template_dict['Name'] = player
			writer.writerow(template_dict)

"""
def search_str_spell(string):
	str_list = string.split()
	spell_list = get_list_spells()
	index_start = 0
	for i, word in enumerate(str_list):
		for spell in spell_list:
			if word.lower() in spell.lower():
				index_start = i
				return index_start
	return index_start
"""