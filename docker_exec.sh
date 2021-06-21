#!/usr/bin/env bash

yum update
yum install -y gcc openssl-devel bzip2-devel libffi-devel python3
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

