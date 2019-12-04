#!/usr/bin/env python
import argparse
import requests
import base64
import json


def validity_iban(iban):
    url = f'https://sandbox.swift.com/swiftref-api/ibans/{iban}/validity'
    headers = {'x-api-key': 'vm47jyQ6vxfWzUAV7GdGfwYMYGgJLyBs'}
    response = requests.get(url, headers=headers)
    print(response.text)


def get_access_token(verbose=False):
    url = 'https://sandbox.swift.com/oauth2/v1/token'
    consumer = '8bHOOqTtnAAYroSNTJgexY6KOYSx3m5E'
    secret = 'slr1yOEfgvYLzgAI'
    credentials = f'{consumer}:{secret}'
    base64_credentials = base64.b64encode(
        credentials.encode('utf8')).decode('utf8')
    Authorization = f'Basic {base64_credentials}'
    headers = {'x-api-key': '8bHOOqTtnAAYroSNTJgexY6KOYSx3m5E',
               'Authorization': Authorization,
               'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'password',
            'username': 'sandbox-id',
            'password': 'sandbox-key'}
    response = requests.post(url, headers=headers, data=data)
    if verbose:
        print(response.text)
    parsed = json.loads(response.text)
    return parsed['access_token']


def value_and_currency():
    url = 'https://sandbox.swift.com/biapi/banking-analytics/1.0.0/value-and-currency?market=PMTS_payments&reporting_period=2019-01'
    response = requests.get(url,
                            headers={'Authorization':
                                     f'Bearer {get_access_token()}'})
    parsed = json.loads(response.text)
    print(json.dumps(parsed, indent=2, sort_keys=True))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--validity_iban")
    parser.add_argument("--value_and_currency", action="store_true")
    parser.add_argument("--get_access_token", action="store_true")
    args = parser.parse_args()
    if args.validity_iban:
        validity_iban(args.validity_iban)
    elif args.get_access_token:
        get_access_token(verbose=True)
    elif args.value_and_currency:
        value_and_currency()
    else:
        parser.print_help()

