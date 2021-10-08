# -*- coding: utf-8 -*-
# @Author: CryptON
# @Date: 2021-10-07
# @Last Modified by: CryptON

from abc import ABC, abstractclassmethod
from typing import Union


class ABCExchangeAPI(ABC):

    @abstractclassmethod
    def __init__(self, **kwargs):
        super().__init__()

    @abstractclassmethod
    def buy_market(self, amount, ticker):
        pass

    @abstractclassmethod
    def check_balance(self, amount, ticker):
        pass
