#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: CryptON
# @Date: 2021-10-07
# @Last Modified by: CryptON

__author__ = "CryptON"
__copyright__ = "Copyright 2021, CryptON"
__license__ = "MIT"
__version__ = "0.0.1 Beta"
__maintainer__ = "CryptON"
__email__ = "CryptON112358@protonmail.com"


import sys
import os
import argparse
import json
import time
import sched
import logging
import threading

from termcolor import colored
import telebot

from exbts import CoinbaseAPI

logger = logging.getLogger('SimpleDCABot')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def print_logo():
    logo = """
    .d88b. w                8       888b. .d88b    db    888b.        w   
    YPwww. w 8d8b.d8b. 88b. 8 .d88b 8   8 8P      dPYb   8wwwP .d8b. w8ww 
        d8 8 8P Y8P Y8 8  8 8 8.dP' 8   8 8b     dPwwYb  8   b 8' .8  8   
    `Y88P' 8 8   8   8 88P' 8 `Y88P 888P' `Y88P dP    Yb 888P' `Y8P'  Y8P 
                       8                                                  
    """
    print(colored(logo, 'green'))


tm_welcome_msg = """
Hello, I am your SimpleDCABot.
As your faithful AI, I will inform you about every buy.
You can also send me some commands:

/help - print this help
/balance - print you balance of selected traiding pair

Let's get to work.
"""


class SimpleDCABot:
    def __init__(self, setting, test):
        self.setting = setting
        self.logger = logger
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.kill = False
        self.test = test

        self.ticker = f'{setting["crypto"]}-{setting["fiat"]}'
        self.fiat = setting["fiat"]
        self.crypto = setting["crypto"]
        self.amount = setting["amount"]

        if setting['exchange'].lower() == 'coinbase':
            self.ex = CoinbaseAPI(setting['exchange_api']['API_KEY'], setting['exchange_api']
                                  ['SECRET_KEY'], setting['exchange_api']['PASSPHRASE'])
        elif setting['exchange'].lower() == 'kraken':
            raise NotImplemented(f'{setting["exchange"]} is not supported.')
        else:
            raise NotImplemented(f'{setting["exchange"]} is not supported.')

        if 'telegram_api' in self.setting:
            self.tb = telebot.TeleBot(setting['telegram_api']['TOKEN'])
            self.tb.send_message(
                setting['telegram_api']['chat_id'], f'{tm_welcome_msg}')

            self._prepare_handlers()
        else:
            self.tb = None

    def _communicate(self, msg):
        logger.info(f'{msg}')
        if self.tb:
            self.tb.send_message(
                self.setting['telegram_api']['chat_id'], f'{msg}')

    def _validate(self, message):
        if self.tb:
            msg_dict = message.json  # json.loads(message.json)
            if not str(msg_dict['from']['id']) == self.setting['telegram_api']['chat_id']:
                self._communicate(
                    f'ALERT!!!\n Username {msg_dict["from"]["username"]} with id: {msg_dict["from"]["id"]} tried to contact me.')
                pass
            else:
                return True
        else:
            return True

    def _prepare_handlers(self,):
        if self.tb:
            @self.tb.message_handler(commands=['help'])
            def tbhelp(message):
                if self._validate(message):
                    self.tb.send_message(
                        settings['telegram_api']['chat_id'], f'{tm_welcome_msg}')

            @self.tb.message_handler(commands=['balance'])
            def tbbalance(message):
                if self._validate(message):
                    fiat_res, fiat_balance = self.ex.check_balance(self.fiat)
                    crypto_res, crypto_balance = self.ex.check_balance(
                        self.crypto)

                    if not fiat_res:
                        self.tb.send_message(
                            settings['telegram_api']['chat_id'], f'Error: {fiat_balance}')
                        return

                    if not crypto_res:
                        self.tb.send_message(
                            settings['telegram_api']['chat_id'], f'Error: {crypto_balance}')
                        return

                    msg = f'Balance:\n{self.fiat}: {fiat_balance}\n{self.crypto}: {crypto_balance}'
                    self.tb.send_message(
                        settings['telegram_api']['chat_id'], f'{msg}')

    def run(self,):
        logger.info(f'SimpleDCABot running...')
        self._communicate(
            f'The first purchase is scheduled in {self.setting["start"]} seconds with a purchase period of {self.setting["interval"]} seconds.')

        th = threading.Thread(target=self._run_dca_loop)
        th.start()

        if self.tb:
            self.tb.infinity_polling()

    def _buy(self):
        fiat_res, fiat_balance = self.ex.check_balance(self.fiat)
        if not fiat_res:
            self._communicate(
                f'Can\'t get fiat balance. Error: {fiat_balance}')
            return

        if self.amount > float(fiat_balance):
            self._communicate(
                f'The purchase failed due to a low balance. EUR: {fiat_balance}')
            return

        if not self.test:
            order_result = self.ex.buy_market(self.amount, self.ticker)
        else:
            order_result = 'TEST'

        self._communicate(
            f'Market order of {self.crypto} for {self.amount} {self.fiat} created. Result: {order_result}')

    def _run_dca_loop(self,):
        self.scheduler.enterabs(
            time.time()+int(settings['start']), 0, self._buy)
        self.scheduler.run()

        while True:
            self.scheduler.enterabs(
                time.time()+int(settings['interval']), 0, self._buy)
            self.scheduler.run()
            if self.kill:
                return

    def kill(self):
        self.kill = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', required=True, type=str,
                        default='conf/bot_conf.json', help="Json bot configuration.")
    parser.add_argument('--test', action='store_true',
                        help="Bot test mode. Bot will comunicate, but it will never byu anything.")
    args = parser.parse_args()

    with open(args.json, 'r') as f:
        settings = json.load(f)

    file_handler = logging.FileHandler(settings['logfile'])
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    print_logo()

    logger.info('Welcome!')
    print('')

    if args.test:
        logger.info(f'MODE:{colored("TESTING","blue")}')
    else:
        logger.info(f'MODE:{colored("LIVE","red")}')

    print('')
    logger.info(f'Running on host: {os.uname()[1]}')
    logger.info(f'Config:\n {json.dumps(settings, indent=4, sort_keys=True)}')

    logger.info(f'Starting bot...')
    bot = SimpleDCABot(settings, args.test)
    bot.run()
