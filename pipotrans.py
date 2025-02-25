"""Translating po files."""

import getopt
import os
from pathlib import Path
import re
import sys

import deepl
import polib

DEEPL_API_TOKEN = os.environ["DEEPL_API_TOKEN"]

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, "d:l:")


def translate(text, lang):
    """Translate."""
    # Define a dictionary to hold the mappings of tokens to placeholders
    placeholders = {}

    # Use a regular expression to find all the tokens
    tokens = re.findall(r'%\((.*?)\)s', text)

    # Replace each token with a unique placeholder
    for i, token in enumerate(tokens):
        placeholder = f'__PLACEHOLDER_{i}__'
        placeholders[placeholder] = f'%({token})s'
        text = text.replace(f'%({token})s', placeholder)

    # Perform the translation
    translator = deepl.Translator(DEEPL_API_TOKEN)
    translated_text = str(translator.translate_text(text, target_lang=lang))

    # Replace the placeholders back with the original tokens
    for placeholder, token in placeholders.items():
        translated_text = translated_text.replace(placeholder, token)

    return translated_text


def get_dirname():
    """Get dirname."""
    dirname = False
    for opt, arg in opts:
        if opt in ['-d']:
            dirname = arg
    if not dirname:
        print("Please enter the directory for "
              "the PO files:")
        dirname = input()
    return dirname


def get_target_language():
    """Get target language."""
    lang = False
    for opt, arg in opts:
        if opt in ['-l']:
            lang = arg
    if not lang:
        print("Please enter two letter ISO "
              "language code, e.g. DE:")
        lang = input()
    return lang


def process_files(dirname, lang):
    """Process files."""

    files = Path(dirname).rglob("*.po")
    for filename in files:
        po = polib.pofile(filename)
        # Untranslated entries
        for entry in po.untranslated_entries():
            print(entry.msgid)
            print("translating...")
            entry.msgstr = translate(entry.msgid, lang)
            entry.fuzzy = True
            print(entry.msgstr)
            print('\n')
            po.save(filename)
        # # Fuzzy entries
        # for entry in po.fuzzy_entries():
        #     print(entry.msgid)
        #     print("update translation...")
        #     entry.msgstr = translate(entry.msgid, lang)
        #     print(entry.msgstr)
        #     print('\n')
        #     po.save(filename)


if __name__ == '__main__':
    process_files(get_dirname(), get_target_language())

# Enf od file
