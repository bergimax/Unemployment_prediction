#!/usr/bin/env python
# coding: utf-8

import requests

url = 'http://localhost:9696/predict'

#row number: 16608
#val expected: 8.094

unemploy = {
  "country_code": "ITA",
  "year": 2022,
  "personal_remittances": 0.523746,
  "gdp": 28.32937,
  "gdp_grow": 3.674683
}

requests.post(url, json=unemploy)

requests.post(url, json=unemploy).json()

response = requests.post(url, json=unemploy).json()

#rx = response['unemploy']
print('The unemployment level is: ', response['unemploy'] )