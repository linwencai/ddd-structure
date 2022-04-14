#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import pathlib
import toml
from diting.core.common.crypto import decrypt

_current_dir = pathlib.Path(os.path.dirname(__file__))

APP_CONFIG = toml.load(_current_dir / "settings.toml")

SETTINGS_DEV_FILE_PATH = _current_dir / os.environ.get("SETTINGS_DEV_FILE_NAME", "settings-dev.toml")
if os.path.exists(SETTINGS_DEV_FILE_PATH):
    APP_CONFIG.update(toml.load(SETTINGS_DEV_FILE_PATH))

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

def parth_path(value : str) -> str:
    path = _current_dir / value

    return str(path.resolve()).replace("\\", "/")

def parse_path_config(config : dict):
    
    enc_pattern = re.compile(r'PATH\((.*)\)')

    for key, value in config.items():
        if isinstance(value, str):
            match = enc_pattern.match(value)
            if match is None:
                continue
            relative_path = match.group(1)
            config[key] = parth_path(relative_path)

        if isinstance(value, dict):
            parse_path_config(value)

decrypt_config(APP_CONFIG)
parse_path_config(APP_CONFIG)

SANIC_CONFIG = APP_CONFIG.pop("sanic")
