from bs4 import BeautifulSoup
import os, sys, requests
from selenium import webdriver
import pickle
import json

"""
sys.setrecursionlimit(10000)

def get_spell(spell):
    driver = webdriver.Firefox()
    url = 'https://roll20.net/compendium/dnd5e/Spells:%s#content' % (spell)
    driver.get(url)
    spell_soup = BeautifulSoup(driver.page_source, 'html5lib')
    driver.quit()
    body = spell_soup.find('div', attrs={'class', 'body'})
    return body
"""

    
def get_list_spells():
    url = 'https://roll20.net/compendium/dnd5e/Index%3ASpells'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html5lib')
    soup_list = soup.find_all('ul')
    spell_list = []
    for letter in soup_list:
        spells = letter.find_all('a')
        for spell in spells:
            spell_list.append(spell.contents[0])
    spell_list = spell_list[8:]
    return spell_list

"""
def save_dict_spells():
    spell_list = get_list_spells()
    for spell in spell_list:
        if not os.path.isfile('spell_html_%s.p' % spell):
            data = {spell : get_spell(spell)}
            with open('spell_html_%s.p' % spell, 'wb') as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

def read_spell_html():
    spell_list = get_list_spells()
    list_dict_spells = []
    for spell in spell_list:
        with open('spell_html_%s.p' % spell, 'rb') as f:
            data = pickle.load(f)
        text = data[spell]
        spell_dict = {}
        spell_dict['Name'] = str(text.find('h1').contents[0])
        spans = text.find_all('span')
        li = text.find_all('li')
        spell_dict['Spell Level'] = str(spans[0].contents[0])
        spell_dict['Spell Type'] = str(spans[1].contents[0])
        spell_dict['Casting Time'] = str(li[0].contents[1])
        spell_dict['Range'] = str(li[1].contents[1])
        spell_dict['Components'] = str(li[2].contents[1])
        if len(li[3]) == 3:
            spell_dict['Duration'] = 'Concentration, ' + str(li[3].contents[2])
        else:
            spell_dict['Duration'] = str(li[3].contents[1])
        spell_dict['Classes'] = str(li[4].contents[1])
        spell_dict['Description'] = str(li[5].contents[0])
        try:
            spell_dict['At Higher Levels'] = str(li[6].contents[1])
        except:
            pass
        list_dict_spells.append(spell_dict)
        print('Made dictionary for spell %s' % spell)
    return list_dict_spells

def save_list_dict_spells(list_dict):
    with open('spells', 'w') as fout:
        json.dump(list_dict, fout)
"""
def return_spell(spell):
    with open('spells', 'r') as fout:
        data = json.load(fout)
    spell_dict = {}
    for item in data:
        if item['Name'].lower() == spell.lower():
            spell_dict = item
            break
    return spell_dict
    




