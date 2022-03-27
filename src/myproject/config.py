#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import pathlib
import toml
from  myproject.common.crypto import decrypt

_current_dir = pathlib.Path(os.path.dirname(__file__))

APP_CONFIG = toml.load(_current_dir / "settings.toml")

SANIC_CONFIG = APP_CONFIG.pop("sanic")

_secret_key = APP_CONFIG['secret_key']

def decrypt_config(config : dict):
    enc_pattern = re.compile(r'ENC\((.*)\)')

    for key, value in config.items():
        if isinstance(value, str):
            match = enc_pattern.match(value)
            if match is None:
                continue
            encrypt_text = match.group(1)
            config[key] = decrypt(encrypt_text, _secret_key)

        if isinstance(value, dict):
            decrypt_config(value)

decrypt_config(APP_CONFIG)