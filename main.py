#encoding: utf-8
import telebot
import time
import requests
from bs4 import BeautifulSoup
import logging
from telebot.types import Message
import json
from telebot import types
from datetime import datetime
import re
from pycoingecko import CoinGeckoAPI
from web3 import Web3, HTTPProvider, IPCProvider

cg = CoinGeckoAPI()
bot_token = 'BOT_TOKEN'

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot = telebot.TeleBot(token=bot_token)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
print(w3.isConnected())

@bot.message_handler(commands=['start'])
def start_command(message):
    cid = message.chat.id
    bot.send_message(cid, "🔰 Hello 🔰 I am a PancakeSwap bot and I can tell you by your address how many tokens you have accumulated in which Pool and also " + \
                          "I will count all the necessary information, just write me your address." + "\n" + "\n" + \
                          "🔰 At the moment I can only provide information on 9 Pools: *CAKE, bOPEN, DODO, SWINGBY, BRY, ZEE, SWGB, SFP, LINA, LIT, HGET, BDO, EGLD, UST და DITTO.*" + "\n" + "\n" + \
                          "🔰 To view commands simply type `Commands`", parse_mode='Markdown')
                              
@bot.message_handler(func=lambda message: message.text == "Commands")
def help_command(message):
    cid = message.chat.id
    bot.send_message(cid, "🔰 If you want to know how much you have accumulated *CAKE, bOPEN, DODO, SWINGBY, BRY, ZEE, SWGB, SFP, LINA, LIT, HGET, BDO, EGLD, UST და DITTO* Pool-ში მაშინ უბრალოდ მისამართი მომწერე." + "\n" + "\n" + \
                          "🔰 cake, cake? Or /p cake - if you write to me then I will show you the price of $ CAKE." + "\n" + "\n" + \
                          "🔰 /pcs - If you subscribe then you will see PancakeSwap statistics.", parse_mode='Markdown')

try:
    get_gel = requests.get("https://transferwise.com/gb/currency-converter/usd-to-gel-rate")
    get_gelsourcecode = BeautifulSoup(get_gel.content, 'html.parser')
    get_gel_string = get_gelsourcecode.find('span', class_="text-success").get_text()
    get_gel_string_float = float(get_gel_string)
except Exception:
    get_gel_string_float = float(1)

def check_ping():
    checker = cg.ping()
    if checker['gecko_says'] == "(V3) To the Moon!":
        return True
    else:
        return False

info_earnd = []
info_earnd.clear()
def contract_checker(guy):
    info_earnd.clear()
    info_from_contract = []
    info_from_contract.clear()
    cake_list = []
    cake_list.clear()
    cake_addr = '0x73feaa1eE314F8c655E354234017bE2193C9E24E'
    cake_abi = '[{"inputs":[{"internalType":"contract CakeToken","name":"_cake","type":"address"},{"internalType":"contract SyrupBar","name":"_syrup","type":"address"},{"internalType":"address","name":"_devaddr","type":"address"},{"internalType":"uint256","name":"_cakePerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"BONUS_MULTIPLIER","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"contract IBEP20","name":"_lpToken","type":"address"},{"internalType":"bool","name":"_withUpdate","type":"bool"}],"name":"add","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"cake","outputs":[{"internalType":"contract CakeToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cakePerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_devaddr","type":"address"}],"name":"dev","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"devaddr","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"enterStaking","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"leaveStaking","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"migrate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"migrator","outputs":[{"internalType":"contract IMigratorChef","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingCake","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"bool","name":"_withUpdate","type":"bool"}],"name":"set","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IMigratorChef","name":"_migrator","type":"address"}],"name":"setMigrator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract SyrupBar","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"multiplierNumber","type":"uint256"}],"name":"updateMultiplier","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    
    contract_list_address = ['0x624ef5C2C6080Af188AF96ee5B3160Bb28bb3E02',
                             '0xcCD0b93cC6ce3dC6dFaA9DB68f70e5C8455aC5bd',
                             '0x9cB24e9460351bC51d4066BC6AEd1F3809b02B78',
                             '0x2dcf4cDFf4Dd954683Fe0a6123077f8a025b66cF',
                             '0x6EFa207ACdE6e1caB77c1322CbdE9628929ba88F',
                             '0xD0b738eC507571176D40f28bd56a0120E375f73a',
                             '0xf7a31366732F08E8e6B88519dC3E827e04616Fc9',
                             '0x9F23658D5f4CEd69282395089B0f8E4dB85C6e79',
                             '0xB6fd2724cc9c90DD31DA35DbDf0300009dceF97d',
                             '0x108BFE84Ca8BCe0741998cb0F60d313823cEC143',
                             '0x212bb602418C399c29D52C55100fD6bBa12bea05',
                             '0x2B02d43967765b18E31a9621da640588f3550EFD',
                             '0x02861B607a5E87daf3FD6ec19DFB715F1b371379',
                             '0x1c736F4FB20C7742Ee83a4099fE92abA61dFca41',
                             '0x02aa767e855b8e80506fb47176202aA58A95315a',
                             '0xae3001ddb18A6A57BEC2C19D71680437CA87bA1D',
                             '0x5Ac8406498dC1921735d559CeC271bEd23B294A7',
                             '0xe56842ed550ff2794f010738554db45e60730371']

    contract_list_abi = ['[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]', 
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]',
                         '[{"inputs":[{"internalType":"contract IBEP20","name":"_syrup","type":"address"},{"internalType":"contract IBEP20","name":"_rewardToken","type":"address"},{"internalType":"uint256","name":"_rewardPerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"uint256","name":"_bonusEndBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"bonusEndBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"emergencyRewardWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"pendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stopReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract IBEP20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]']

    for addr, abi in zip(contract_list_address, contract_list_abi):
        sm = w3.eth.contract(addr, abi=abi)
        user_info = sm.functions.userInfo(guy).call()
        user_info_staked_cake = user_info[0]
        info_from_contract.append(user_info_staked_cake)
    cc = w3.eth.contract(cake_addr, abi=cake_abi)
    cake_staked = cc.functions.userInfo(0, guy).call()[0]
    cake_list.append(cake_staked)
    check_if_zeros = info_from_contract.count(info_from_contract[0]) == len(info_from_contract)
    print(info_from_contract)
    print(cake_list)
    if check_if_zeros == True and cake_list[0] == 0:
        return "At this address CAKE, DITTO, HGET, BDO, EGLD, UST, WSOTE, FRON, HELMET, BTCST, BSCX, LINA, SFP, ZEE And CAKE is not checked in BRY Pool!"
    else:
        ditto_pool = info_from_contract[0]
        hget_pool = info_from_contract[1]
        bdo_pool = info_from_contract[2]
        egld_pool = info_from_contract[3]
        ust_pool = info_from_contract[4]
        wsote_pool = info_from_contract[5]
        front_pool = info_from_contract[6]
        helmet_pool = info_from_contract[7]
        btcst_pool = info_from_contract[8]
        bscx_pool = info_from_contract[9]
        lina_pool = info_from_contract[10]
        sfp_pool = info_from_contract[11]
        zee_pool = info_from_contract[12]
        bry_pool = info_from_contract[13]
        swingby_pool = info_from_contract[14]
        dodo_pool = info_from_contract[15]
        bopen_pool = info_from_contract[16]
        bin = info_from_contract[17]
        cake_pool = cake_list[0]
        if cake_pool > 0:
            token_id = 'pancakeswap-token'
            coin_name = ' CAKE'
            pending_cake = cc.functions.pendingCake(0, guy).call() / 1000000000000000000
            staked_cake = float(w3.fromWei(cake_list[0], 'ether'))
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=0x73feaa1ee314f8c655e354234017be2193c9e24e&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            cakepool = int("{0:.0f}".format(cakepool))
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            info = cake_calculations(pending_cake, staked_cake, coin_list_price, cakepool)
            info_earnd.append(info)
            
        else:
            pass
        
        if ditto_pool > 0:
            token_id = 'ditto'
            coin_name = ' DITTO'
            addr = contract_list_address[0]
            abi = contract_list_abi[0]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[1]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)

        if hget_pool > 0:
            token_id = 'hedget'
            coin_name = ' HGET'
            addr = contract_list_address[1]
            abi = contract_list_abi[1]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[1]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)

        if bdo_pool > 0:
            token_id = 'bdollar'
            coin_name = ' BDO'
            addr = contract_list_address[2]
            abi = contract_list_abi[2]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[2]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)
        
        if egld_pool > 0:
            token_id = 'elrond-erd-2'
            coin_name = ' EGLD'
            addr = contract_list_address[3]
            abi = contract_list_abi[3]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[3]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)

        if ust_pool > 0:
            token_id = 'terrausd'
            coin_name = ' UST'
            addr = contract_list_address[4]
            abi = contract_list_abi[4]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[4]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)

        if wsote_pool > 0:
            token_id = 'soteria'
            coin_name = ' wSOTE'
            addr = contract_list_address[5]
            abi = contract_list_abi[5]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[5]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)

        if front_pool > 0:
            token_id = 'frontier'
            coin_name = ' FRONT'
            addr = contract_list_address[6]
            abi = contract_list_abi[6]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[6]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)
        
        if helmet_pool > 0:
            token_id = 'helmet-insure'
            coin_name = ' HELMET'
            addr = contract_list_address[7]
            abi = contract_list_abi[7]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[7]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)

        if btcst_pool > 0:
            token_id = 'btc-standard-hashrate-token'
            coin_name = ' BTCST'
            addr = contract_list_address[8]
            abi = contract_list_abi[8]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[8]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)

        if bscx_pool > 0:
            token_id = 'bscex'
            coin_name = ' BSCEX'
            addr = contract_list_address[9]
            abi = contract_list_abi[9]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[9]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)

        if lina_pool > 0:
            token_id = 'linear'
            coin_name = ' LINA'
            addr = contract_list_address[10]
            abi = contract_list_abi[10]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[10]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)

        if sfp_pool > 0:
            token_id = 'safepal'
            coin_name = ' SFP'
            addr = contract_list_address[11]
            abi = contract_list_abi[11]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[11]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)

        if zee_pool > 0:
            token_id = 'zeroswap'
            coin_name = ' ZEE'
            addr = contract_list_address[12]
            abi = contract_list_abi[12]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[12]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)

        if bry_pool > 0:
            token_id = 'berry-data'
            coin_name = ' BRY'
            addr = contract_list_address[13]
            abi = contract_list_abi[13]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[13]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)
        
        if swingby_pool > 0:
            token_id = 'swingby'
            coin_name = ' SWINGBY'
            addr = contract_list_address[14]
            abi = contract_list_abi[14]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[14]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)
          
        if dodo_pool > 0:
            token_id = 'dodo'
            coin_name = ' DODO'
            addr = contract_list_address[15]
            abi = contract_list_abi[15]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[15]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)
        
        if bopen_pool > 0:
            token_id = 'open-governance-token'
            coin_name = ' bOPEN'
            addr = contract_list_address[16]
            abi = contract_list_abi[16]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[16]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)

        if bin > 0:
            token_id = 'BIN'
            coin_name = 'Binemon'
            addr = contract_list_address[17]
            abi = contract_list_abi[17]
            sm = w3.eth.contract(addr, abi=abi)
            staked_cake = sm.functions.userInfo(guy).call()[0]
            pending_reward = sm.functions.pendingReward(guy).call() / 1000000000000000000
            reward_per_block = sm.functions.rewardPerBlock().call() / 1000000000000000000
            latest_block = w3.eth.blockNumber
            end_block = sm.functions.bonusEndBlock().call()
            coin_list = [token_id, 'binancecoin', 'bitcoin', 'ethereum', 'pancakeswap-token']
            coin_list_price = []
            for coinfasi in coin_list:
                coin_price = cg.get_price(ids=coinfasi, vs_currencies='usd')
                coin_fasi = coin_price[coinfasi]['usd']
                coin_list_price.append(coin_fasi)
            contract_address = contract_list_address[17]
            totalstakedcake = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82&address=" + contract_address + "&tag=latest"
            response = requests.get(totalstakedcake)
            qeiqebi = response.json()
            cakepool = (int(qeiqebi["result"]) / 1000000000000000000)
            info = calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block)
            info_earnd.append(info)

        print(info_earnd)
        print_all = ('\n'.join(map(str, info_earnd))) + "\n"
        return print_all

 
    

def cake_calculations(pending_cake, staked_cake, coin_list_price, cakepool):
    pending_usd = coin_list_price[0] * pending_cake
    pending_gel = get_gel_string_float * pending_usd
    pending_bnb = pending_usd / coin_list_price[1]
    pending_btc = pending_usd / coin_list_price[2]
    pending_eth = pending_usd / coin_list_price[3]
    staked_usd = coin_list_price[0] * staked_cake 
    staked_gel = staked_usd * get_gel_string_float
    staked_bnb = staked_usd / coin_list_price[1]
    staked_btc = staked_usd / coin_list_price[2]
    staked_eth = staked_usd / coin_list_price[3]
    stakingunitpercent = '{:.15f}'.format(1 / cakepool * 100)
    totaldailyrewards = 288000
    stakingunitearns = float(stakingunitpercent) / 100 * totaldailyrewards
    ##########################################################################
    yourdailyreward = stakingunitearns * staked_cake
    dailyreward_price = yourdailyreward * float(coin_list_price[0])
    weekly_cake_reward = yourdailyreward * 7
    weekly_cake_reward_price = weekly_cake_reward * float(coin_list_price[0])
    apy = yourdailyreward / staked_cake * 100 * 365
    monthofcompounding = staked_cake * (1 + apy/100/30)**(30*0.0865)
    twomonthofcompunding = staked_cake * (1 + apy/100/30)**(60*0.0865)
    threemonthofcompunding = staked_cake * (1 + apy/100/30)**(90*0.0865)
    twodayreward = yourdailyreward * 2
    threedayreward = yourdailyreward * 3
    twodayreward_price = twodayreward * float(coin_list_price[0])
    threedayreward_price = threedayreward  * float(coin_list_price[0])
    ##########################################################################
    monthofcompoundingprice = float(coin_list_price[0]) * float(monthofcompounding) 
    twomonthofcompundingprice = float(coin_list_price[0]) * float(twomonthofcompunding)
    threemonthofcompundingprice = float(coin_list_price[0]) * float(threemonthofcompunding)
    info = "🔰 *CAKE Staking* (" + '{0:,.2f}'.format(float(apy)) + "%) 🔰" + "\n" + \
        "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
        "🟢 Accumulated: " + '{0:,.8f}'.format(float(pending_cake)) + " CAKE" + "\n" + \
        "▶️ 1 Per day: " + '{0:,.2f}'.format(float(yourdailyreward)) + " CAKE ($" + '{0:,.2f}'.format(float(dailyreward_price)) + ")" + "\n" + \
        "▶️ 2 Per day: " + '{0:,.2f}'.format(float(twodayreward)) + " CAKE ($" + '{0:,.2f}'.format(float(twodayreward_price)) + ")" + "\n" + \
        "▶️ 3 Per day: " + '{0:,.2f}'.format(float(threedayreward)) + " CAKE ($" + '{0:,.2f}'.format(float(threedayreward_price)) + ")" + "\n" + \
        "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
        "▶️ In 1 a week: " + '{0:,.2f}'.format(float(weekly_cake_reward)) + " CAKE ($" + '{0:,.2f}'.format(float(weekly_cake_reward_price)) + ")" + "\n" + \
        "▶️ In 1 months: " + '{0:,.2f}'.format(float(monthofcompounding)) + " CAKE ($" + '{0:,.2f}'.format(float(monthofcompoundingprice)) + ")" + "\n" + \
        "▶️ In 2 months: " + '{0:,.2f}'.format(float(twomonthofcompunding)) + " CAKE ($" + '{0:,.2f}'.format(float(twomonthofcompundingprice)) + ")" + "\n" + \
        "▶️ In 3 months: " + '{0:,.2f}'.format(float(threemonthofcompunding)) + " CAKE ($" + '{0:,.2f}'.format(float(threemonthofcompundingprice)) + ")" + "\n" + \
        "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
        "▶️ Cost: ~$" + '{0:,.2f}'.format(float(pending_usd)) + " | ~₾" + '{0:,.2f}'.format(float(pending_gel)) + "\n" + \
        "🔸 BNB: " + '{0:,.8f}'.format(float(pending_bnb)) + "\n" + \
        "🔸 BTC: " + '{0:,.8f}'.format(float(pending_btc)) + "\n" + \
        "🔸 ETH: " + '{0:,.8f}'.format(float(pending_eth)) + "\n" + \
        "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
        "🥞 STICKED CAKE: " + '{0:,.8f}'.format(float(staked_cake)) + "\n" + \
        "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
        "▶️ Cost: ~$" + '{0:,.2f}'.format(float(staked_usd)) + " | ~₾" + '{0:,.2f}'.format(float(staked_gel)) + "\n" + \
        "🔸 BNB: " + '{0:,.8f}'.format(float(staked_bnb)) + "\n" + \
        "🔸 BTC: " + '{0:,.8f}'.format(float(staked_btc)) + "\n" + \
        "🔸 ETH: " + '{0:,.8f}'.format(float(staked_eth)) + "\n" + \
        "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
        "🔹 1 CAKE = $" + '{0:,.4f}'.format(float(coin_list_price[0])) + "\n" + "\n"
    return info



def calculations(coin_name, pending_reward, staked_cake, reward_per_block, coin_list_price, cakepool, sm, end_block, latest_block):
    pending_usd = coin_list_price[0] * pending_reward
    pending_gel = get_gel_string_float * pending_usd
    pending_bnb = pending_usd / coin_list_price[1]
    pending_btc = pending_usd / coin_list_price[2]
    pending_eth = pending_usd / coin_list_price[3]
    staked_cake = staked_cake / 1000000000000000000
    staked_usd = coin_list_price[4] * staked_cake
    staked_gel = staked_usd * get_gel_string_float
    staked_bnb = staked_usd / coin_list_price[1]
    staked_btc = staked_usd / coin_list_price[2]
    staked_eth = staked_usd / coin_list_price[3]
    l_total_rewards_per_block = reward_per_block
    k_total_cake_staked = cakepool
    j_staked_token_price = coin_list_price[4]
    a_your_stake = staked_cake
    b_your_stake_usd = float(a_your_stake) * j_staked_token_price
    f_staking_unit_percent = 1 / k_total_cake_staked * 100
    g_total_daily_rewards = 28800 * l_total_rewards_per_block
    h_staking_unit_earns = f_staking_unit_percent / 100 * g_total_daily_rewards
    c_your_24h_reward = float(h_staking_unit_earns)  * float(a_your_stake)
    d_your_2hh_reward_usd = float(c_your_24h_reward) * float(coin_list_price[0])
    e_apy = d_your_2hh_reward_usd / b_your_stake_usd * 100 * 365
    j_staked_token_price = coin_list_price[4]
    k_total_cake_staked = cakepool
    one_month = float(c_your_24h_reward) * 30
    one_month_price = float(one_month) * float(coin_list_price[0])
    days_left = (end_block - latest_block) / 28800
    yourdailyreward = h_staking_unit_earns * staked_cake
    yourdailyreward_price = yourdailyreward * coin_list_price[0]
    two_day_reward = yourdailyreward * 2
    three_day_reward = yourdailyreward * 3
    two_day_reward_price = two_day_reward * coin_list_price[0]
    three_day_reward_price = three_day_reward * coin_list_price[0]
    weekly_reward = yourdailyreward * 7
    weekly_reward_price = weekly_reward * coin_list_price[0]
    one_hour_reward = yourdailyreward / 24
    one_hour_reward_price = one_hour_reward * coin_list_price[0]
    two_hour_reward = one_hour_reward * 2
    two_hour_reward_price = two_hour_reward * coin_list_price[0]
    three_hour_reward = one_hour_reward * 3
    three_hour_reward_price = three_hour_reward * coin_list_price[0]
    if days_left == 0:
        days_left == " Is over!"
    else:
        pass
    darchenili_dge = days_left * yourdailyreward
    darchenili_dge_price = darchenili_dge * coin_list_price[0]
    info = "🔰 *" + coin_name.strip() + " Staking* (" + '{0:,.2f}'.format(float(e_apy)) + "%) 🔰" + "\n" + \
            "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
            "🟢 Accumulated: " + '{0:,.8f}'.format(float(pending_reward)) + coin_name + "\n" + \
            "Per 1️⃣ Day: " + '{0:,.2f}'.format(float(yourdailyreward)) + coin_name + " ($" + '{0:,.2f}'.format(float(yourdailyreward_price)) + ")" + "\n" + \
            "Per 2️⃣ Day: " + '{0:,.2f}'.format(float(two_day_reward)) + coin_name + " ($" + '{0:,.2f}'.format(float(two_day_reward_price)) + ")" + "\n" + \
            "Per 3️⃣ Day: " + '{0:,.2f}'.format(float(three_day_reward)) + coin_name + " ($" + '{0:,.2f}'.format(float(three_day_reward_price)) + ")" + "\n" + \
             "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
            "1️⃣ per week: " + '{0:,.2f}'.format(float(weekly_reward)) + coin_name + " ($" + '{0:,.2f}'.format(float(weekly_reward_price)) + ")" + "\n" + \
            "1️⃣ per month: " + '{0:,.2f}'.format(float(one_month)) + coin_name + " ($" + '{0:,.2f}'.format(float(one_month_price)) + ")" + "\n" + \
             "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
            "🕐 in 1 hour: " + '{0:,.2f}'.format(float(one_hour_reward)) + coin_name + " ($" + '{0:,.2f}'.format(float(one_hour_reward_price)) + ")" + "\n" + \
            "🕑 In 2 hours: " + '{0:,.2f}'.format(float(two_hour_reward)) + coin_name + " ($" + '{0:,.2f}'.format(float(two_hour_reward_price)) + ")" + "\n" + \
            "🕒 In 3 hours: " + '{0:,.2f}'.format(float(three_hour_reward)) + coin_name + " ($" + '{0:,.2f}'.format(float(three_hour_reward_price)) + ")" + "\n" + \
            "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
            "💵 Cost: ~$" + '{0:,.2f}'.format(float(pending_usd)) + " | ~₾" + '{0:,.2f}'.format(float(pending_gel)) + "\n" + \
            "🔸 BNB: " + '{0:,.8f}'.format(float(pending_bnb)) + "\n" + \
            "🔸 BTC: " + '{0:,.8f}'.format(float(pending_btc)) + "\n" + \
            "🔸 ETH: " + '{0:,.8f}'.format(float(pending_eth)) + "\n" + \
            "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
            "🥞 Stacked CAKE: " + '{0:,.5f}'.format(float(staked_cake)) + "\n" + \
            "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
            "💵 Cost: ~$" + '{0:,.2f}'.format(float(staked_usd)) + " | ~₾" + '{0:,.2f}'.format(float(staked_gel)) + "\n" + \
            "🔸 BNB: " + '{0:,.8f}'.format(float(staked_bnb)) + "\n" + \
            "🔸 BTC: " + '{0:,.8f}'.format(float(staked_btc)) + "\n" + \
            "🔸 ETH: " + '{0:,.8f}'.format(float(staked_eth)) + "\n" + \
            "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
            "🔹 1 " + coin_name.strip() + " = $" + '{0:,.4f}'.format(float(coin_list_price[0])) + "\n" + \
            "🔹 1 CAKE = $" + '{0:,.4f}'.format(float(coin_list_price[4])) + "\n" + \
            "`- - - - - - - - - - - - - - - - - -`" + "\n" + \
            "🕐 will end: " + '{0:,.3f}'.format(float(days_left)) + "\n" + \
            "🕐 You will accumulate before graduation: " + '{0:,.2f}'.format(float(darchenili_dge)) + " ($" + '{0:,.2f}'.format(float(darchenili_dge_price)) + ")" + "\n"
    return info

@bot.message_handler(func=lambda message: message.text == "cake" or message.text == "🥞" or message.text == "Cake" or message.text == "CAKE" or message.text == "/p cake")
def command_text_hi(message):
    if check_ping:
        cid = message.chat.id
        cake_info = cg.get_coin_by_id(id='pancakeswap-token')
        price = cake_info['market_data']['current_price']['usd']
        price_change_percentage_24h = cake_info['market_data']['price_change_percentage_24h']
        ath = cake_info['market_data']['ath']['usd']
        atl = cake_info['market_data']['atl']['usd']
        market_cap = cake_info['market_data']['market_cap']['usd']
        high_24h = cake_info['market_data']['high_24h']['usd']
        low_24h = cake_info['market_data']['low_24h']['usd']
        total_volume = cake_info['market_data']['total_volume']['usd']

        info = "🔸 Price: $" + '{0:,.4f}'.format(float(price)) + " ("+ '{0:,.2f}'.format(float(price_change_percentage_24h)) + "%)" + "\n" + \
            "`- - - - - - - - - - - - -`" + "\n" + \
            "🔸 Capitalization: $"  + '{0:,.0f}'.format(float(market_cap)) + "\n" + \
            "🔸 Shopping (24 hours): $"  + '{0:,.0f}'.format(float(total_volume)) + "\n" + \
            "`- - - - - - - - - - - - -`" + "\n" + \
            "🔸 High (24 hours): $"   + '{0:,.4f}'.format(float(high_24h)) + "\n" + \
            "🔸 Low (24 hours): $"   + '{0:,.4f}'.format(float(low_24h)) + "\n" + \
            "`- - - - - - - - - - - - -`" + "\n" + \
            "🔸 ATH and ATL: $" + '{0:,.2f}'.format(float(ath)) + " | $" + '{0:,.2f}'.format(float(atl))
        bot.send_message(cid, info, parse_mode='Markdown')
    else:
        bot.send_message(cid, "❌ Connection to CoinGecko API is temporarily impossible ❌")

@bot.message_handler(func=lambda message: message.text == "bin" or message.text == "$BIN" or message.text == "Bin" or message.text == "BIN" or message.text == "/p bin")
def command_text_hi(message):
    if check_ping:
        cid = message.chat.id
        cake_info = cg.get_coin_by_id(id='bin
        price = cake_info['market_data']['current_price']['usd']
        price_change_percentage_24h = cake_info['market_data']['price_change_percentage_24h']
        ath = cake_info['market_data']['ath']['usd']
        atl = cake_info['market_data']['atl']['usd']
        market_cap = cake_info['market_data']['market_cap']['usd']
        high_24h = cake_info['market_data']['high_24h']['usd']
        low_24h = cake_info['market_data']['low_24h']['usd']
        total_volume = cake_info['market_data']['total_volume']['usd']

        info = "🔸 Price: $" + '{0:,.4f}'.format(float(price)) + " ("+ '{0:,.2f}'.format(float(price_change_percentage_24h)) + "%)" + "\n" + \
            "`- - - - - - - - - - - - -`" + "\n" + \
            "🔸 Capitalization: $"  + '{0:,.0f}'.format(float(market_cap)) + "\n" + \
            "🔸 Shopping (24 hours): $"  + '{0:,.0f}'.format(float(total_volume)) + "\n" + \
            "`- - - - - - - - - - - - -`" + "\n" + \
            "🔸 High (24 hours): $"   + '{0:,.4f}'.format(float(high_24h)) + "\n" + \
            "🔸 Low (24 hours): $"   + '{0:,.4f}'.format(float(low_24h)) + "\n" + \
            "`- - - - - - - - - - - - -`" + "\n" + \
            "🔸 ATH and ATL: $" + '{0:,.2f}'.format(float(ath)) + " | $" + '{0:,.2f}'.format(float(atl))
        bot.send_message(cid, info, parse_mode='Markdown')
    else:
        bot.send_message(cid, "❌ Connection to CoinGecko API is temporarily impossible ❌")


@bot.message_handler(func=lambda message: message.text == "hedget" or message.text == "🥞" or message.text == "Hedget" or message.text == "CAKE" or message.text == "/p hedget")
def command_text_hi(message):
    if check_ping:
        cid = message.chat.id
        cake_info = cg.get_coin_by_id(id='hedget')
        price = cake_info['market_data']['current_price']['usd']
        price_change_percentage_24h = cake_info['market_data']['price_change_percentage_24h']
        ath = cake_info['market_data']['ath']['usd']
        atl = cake_info['market_data']['atl']['usd']
        market_cap = cake_info['market_data']['market_cap']['usd']
        high_24h = cake_info['market_data']['high_24h']['usd']
        low_24h = cake_info['market_data']['low_24h']['usd']
        total_volume = cake_info['market_data']['total_volume']['usd']

        info = "🔸 Price: $" + '{0:,.4f}'.format(float(price)) + " ("+ '{0:,.2f}'.format(float(price_change_percentage_24h)) + "%)" + "\n" + \
            "`- - - - - - - - - - - - -`" + "\n" + \
            "🔸 Capitalization: $"  + '{0:,.0f}'.format(float(market_cap)) + "\n" + \
            "🔸 Shopping (24 hours): $"  + '{0:,.0f}'.format(float(total_volume)) + "\n" + \
            "`- - - - - - - - - - - - -`" + "\n" + \
            "🔸 High (24 hours): $"   + '{0:,.4f}'.format(float(high_24h)) + "\n" + \
            "🔸 Low (24 hours): $"   + '{0:,.4f}'.format(float(low_24h)) + "\n" + \
            "`- - - - - - - - - - - - -`" + "\n" + \
            "🔸 ATH and ATL: $" + '{0:,.2f}'.format(float(ath)) + " | $" + '{0:,.2f}'.format(float(atl))
        bot.send_message(cid, info, parse_mode='Markdown')
    else:
        bot.send_message(cid, "❌ Connection to CoinGecko API is temporarily impossible ❌")


@bot.message_handler(commands=['pcs'])
def send_pcs_info(message: Message):
    try:
        cid = message.chat.id
        mid = message.message_id
        cake = '0x73feaa1eE314F8c655E354234017bE2193C9E24E'
        ditto = '0x624ef5C2C6080Af188AF96ee5B3160Bb28bb3E02'
        bdo = '0x9cB24e9460351bC51d4066BC6AEd1F3809b02B78'
        egld = '0x2dcf4cDFf4Dd954683Fe0a6123077f8a025b66cF'
        ust = '0x6EFa207ACdE6e1caB77c1322CbdE9628929ba88F'
        wsote = '0xD0b738eC507571176D40f28bd56a0120E375f73a'
        front = '0xf7a31366732F08E8e6B88519dC3E827e04616Fc9'
        helmet = '0x9F23658D5f4CEd69282395089B0f8E4dB85C6e79'
        btcst = '0xB6fd2724cc9c90DD31DA35DbDf0300009dceF97d'
        bscx = '0x108BFE84Ca8BCe0741998cb0F60d313823cEC143'
        ten = '0x108BFE84Ca8BCe0741998cb0F60d313823cEC143'
        albt = '0x3cc08B7C6A31739CfEd9d8d38b484FDb245C79c8'
        zee = '0x02861B607a5E87daf3FD6ec19DFB715F1b371379'
        bry = '0x1c736F4FB20C7742Ee83a4099fE92abA61dFca41'
        swingby = '0x02aa767e855b8e80506fb47176202aA58A95315a'
        dodo = '0xae3001ddb18A6A57BEC2C19D71680437CA87bA1D'
        bopen = '0x5Ac8406498dC1921735d559CeC271bEd23B294A7'
        bin = '0x547cbe0f0c25085e7015aa6939b28402eb0ccdac'
        cake_bnb_farm = '0xA527a61703D82139F8a06Bc30097cC9CAA2df5A6'
        cake_stax = '0x7cd05f8b960Ba071FdF69C750c0E5a57C8366500'
        cake_nar = '0x745C4fD226E169d6da959283275A8E0EcDd7F312'
        cake_nya = '0x2730bf486d658838464A4ef077880998D944252d'
        cake_brobe = '0x970858016C963b780E06f7DCfdEf8e809919BcE8'
        burn_address = '0x000000000000000000000000000000000000dEaD'
        burn_address_1 = '0x35f16A46D3cf19010d28578A8b02DfA3CB4095a1'
        burn_address_2 = '0xd4CFEC77CDc21573982EC85cf33Cfde6Cc677e74'
        contracts = [cake, ditto, bdo, egld, ust, wsote, front, helmet, btcst, bscx, ten, albt, zee, bry, swingby, dodo, bopen]
        contract_names = ["CAKE", "DITTO", "BDO", "EGLD", "UST", "WSOTE", "FRONT", "HELMET", "BTCST", "BSCEX", "TEN", "ALBT", "ZEE", "BRY", "SWINGBY", "DODO", "BOPEN", "BIN"]
        contract_address = ['0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82']
        contract_abi = ['[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegator","type":"address"},{"indexed":true,"internalType":"address","name":"fromDelegate","type":"address"},{"indexed":true,"internalType":"address","name":"toDelegate","type":"address"}],"name":"DelegateChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"delegate","type":"address"},{"indexed":false,"internalType":"uint256","name":"previousBalance","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newBalance","type":"uint256"}],"name":"DelegateVotesChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DELEGATION_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DOMAIN_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint32","name":"","type":"uint32"}],"name":"checkpoints","outputs":[{"internalType":"uint32","name":"fromBlock","type":"uint32"},{"internalType":"uint256","name":"votes","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatee","type":"address"}],"name":"delegate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatee","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"delegateBySig","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegator","type":"address"}],"name":"delegates","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getCurrentVotes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"blockNumber","type":"uint256"}],"name":"getPriorVotes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"numCheckpoints","outputs":[{"internalType":"uint32","name":"","type":"uint32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]']
        contract_balances = []
        balansi = []
        balansi.clear()
        contract_balances.clear()
        for addr, abi in zip(contract_address, contract_abi):
            sm = w3.eth.contract(addr, abi=abi)
            for con, con_names in zip(contracts, contract_names):
                balances = sm.functions.balanceOf(con).call()
                test = w3.fromWei(balances, 'ether')
                info = "🔸 " + str(con_names) + ": " + str('{0:,.2f}'.format(float(test)))
                balansi.append(test)
                contract_balances.append(info)
        burned = sm.functions.balanceOf(burn_address).call() / 1000000000000000000
        totalsupply = sm.functions.totalSupply().call() / 1000000000000000000
        totalsupply = (totalsupply - burned)
        burn_1 = sm.functions.balanceOf(burn_address_1).call() / 1000000000000000000
        burn_2 = sm.functions.balanceOf(burn_address_2).call() / 1000000000000000000
        mondeyBurn = burn_1 + burn_2
        cakebnb = sm.functions.balanceOf(cake_bnb_farm).call() / 1000000000000000000
        staxcake = sm.functions.balanceOf(cake_stax).call() / 1000000000000000000
        narcake = sm.functions.balanceOf(cake_nar).call() / 1000000000000000000
        nyacake = sm.functions.balanceOf(cake_nya).call() / 1000000000000000000
        brobecake = sm.functions.balanceOf(cake_brobe).call() / 1000000000000000000
        sull = sum(balansi)
        farm_sum = float(cakebnb) + float(staxcake) + float(narcake) + float(nyacake) + float(brobecake)
        total = float(sull) + float(farm_sum)
        staked_percent = float(total) / float(totalsupply) * 100
        coin_price = cg.get_price(ids='pancakeswap-token', vs_currencies='usd')
        coin_fasi = coin_price['pancakeswap-token']['usd']
        total_price = total * coin_fasi
        btc_price = cg.get_price(ids='bitcoin', vs_currencies='usd')
        btc_fasi = btc_price['bitcoin']['usd']
        pcs = cg.get_exchanges_by_id(id='pancakeswap')
        trade_volume_24h_btc = pcs['trade_volume_24h_btc']
        trade_volume = btc_fasi * trade_volume_24h_btc
        mondey_burn_price = mondeyBurn * coin_fasi
        try:
            cakestat = 'https://api.pancakeswap.finance/api/v1/stat'
            response = requests.get(cakestat)
            stats = response.json()
            total_value_locked_all = stats['total_value_locked_all']
            total_value_locked_all = '{0:,.2f}'.format(float(total_value_locked_all))
        except Exception:
            total_value_locked_all = " API ERROR!"
    
        info = "🥞 1 CAKE = $" + '{0:,.3f}'.format(float(coin_fasi)) + "\n" + \
                "🔸 Total points: " + '{0:,.2f}'.format(float(totalsupply)) + "\n" + \
                "🔸 Burned: " + '{0:,.2f}'.format(float(burned)) + "\n" + \
                "🔸 Will burn: " + '{0:,.2f}'.format(float(mondeyBurn)) + " ($" + '{0:,.2f}'.format(float(mondey_burn_price)) + ")" + "\n" + \
                "🔸 Stacked: " + '{0:,.2f}'.format(float(total)) + " ($" + '{0:,.2f}'.format(float(total_price)) + ")" + "\n" + \
                "🔸 " + '{0:,.2f}'.format(float(staked_percent)) + "% The full number is confirmed." + "\n" + \
                "🔸 Trade (24h): $" + '{0:,.2f}'.format(float(trade_volume)) + "\n" + \
                "🔸 TVL: $" + total_value_locked_all

        bot.send_message(cid, info, parse_mode='Markdown')
        bot.delete_message(cid, mid)
        balansi.clear()
        contract_balances.clear()
    except Exception as r:
        bot.send_message(cid, r)
        try:
            bot.delete_message(cid, mid)
        except Exception:
            pass

@bot.message_handler(func=lambda message: True)
def get_info_pool(message):
    cid = message.chat.id
    info_earnd.clear()
    try:
        guy = Web3.toChecksumAddress(message.text)
        try:
            info_earnd.clear()
            bot.send_message(cid, contract_checker(guy), parse_mode='Markdown')
        except Exception:
            pass
    except Exception:
        info_earnd.clear()        
        bot.send_message(cid, "❌ You have entered the address incorrectly 🙄")
    
while True:
    try:
        bot.polling()
        break
    except Exception:
        time.sleep(30)
