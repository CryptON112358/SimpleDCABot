# -*- coding: utf-8 -*-
# @Author: CryptON
# @Date: 2021-10-07
# @Last Modified by: CryptON

from typing import Union
from .abc_exchange import ABCExchangeAPI

import cbpro


class CoinbaseAPI(ABCExchangeAPI):
    def __init__(self, api_key, secret_key, passphrase) -> None:
        self.coinbase_client = cbpro.AuthenticatedClient(
            api_key, secret_key, passphrase)

    def buy_market(self, amout, ticker) -> str:
        result = self.coinbase_client.place_market_order(
            product_id=ticker, side='buy', funds=amout)
        return result

    def check_balance(self, ticker) -> Union[bool, float]:
        results = self.coinbase_client.get_accounts()
        if 'message' in results:
            return False, results
        for item in self.coinbase_client.get_accounts():
            if item['currency'] == ticker:
                return True, item['balance']
