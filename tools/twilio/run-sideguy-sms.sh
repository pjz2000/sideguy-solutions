#!/usr/bin/env bash

python3 -m venv .venv-sms
source .venv-sms/bin/activate
pip install --upgrade pip
pip install flask twilio python-dotenv
python3 sideguy_sms/app.py
