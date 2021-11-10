#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 10:53:23 2021

@author: David Magalhaes Sousa
@email: davidmagalhaessousa@gmail.com

With minor tweeks from João Lourenço <joao.lourenco@fct.unl.pt>
"""

import sys
import shutil
import argparse

# What to replace (original, replacement)
utf8replacement = [
    ("−", "-"),
    ("–", "-"),
    (u"\u2212", "-"),
    ("−", "-"),
    ("{\_}", "_"),
    ("{\&}", "\&"),
    (" &", " \&"),
]

parser = argparse.ArgumentParser(description='Cleanup BibTeX files exported from Mendeley (or Zotero?!).')
parser.add_argument('--input', '-i', dest='inFile', type=argparse.FileType('r'),
                    default='-',
                    help='The input file. Defaults to STDIN (keyboard)')
parser.add_argument('--output', '-o', dest='outFile', type=argparse.FileType('w'),
                    default='-',
                    help='The output file. Defaults to STDOUT (screen)')
parser.add_argument('--fix-keys', '-k', dest='fixKeys', default=False, action='store_true',
                    help='fix keys: replace "(" and ")" with "_". Defaults to False')

args = parser.parse_args()


fl = args.inFile.readlines()

for i in range(len(fl)):
    for invalid, valid in utf8replacement:
        fl[i] = fl[i].replace(invalid, valid)

def erase(string, iterator):
    a = len(iterator)
    i=0
    while i <= a - 1:
        if string in iterator[i]:
            del(iterator[i])
            a = len(iterator)
        i += 1
    return iterator

fl = erase("month =", fl)
fl = erase("note =", fl)
fl = erase("annote =", fl)
fl = erase("keywords =", fl)
fl = erase("file =", fl)
fl = erase("annote =", fl)
fl = erase("url =", fl)
fl = erase("abstract =", fl)
fl = erase("issn =", fl)


# CLEANING (SPECIAL HANDLING EXTRA LINES)
if True:
    a = len(fl)
    i = 0
    while i <= a - 1:
        if (" = {" in fl[i]) or ("@" in fl[i]) or (fl[i] == "} ") or (fl[i] == "}") or (fl[i] == "}\n"):
            i += 1
            pass
        else:
            del(fl[i])
            a = len(fl)
#####################################


# DOI HANDLING
if True:
    for i in range(len(fl)):
        if "https://doi.org/" in fl[i] and "doi =" in fl[i]:
            
            fl[i] = fl[i].replace("https://doi.org/","")
#####################################


# CHECK FOR DUPLICATE KEYS
if True:
    keys = []
    duplicates = []
    badsymbols = []
    for i in range(len(fl)):
        if "@" in fl[i]:
            key = fl[i].split("{")[1].split(",")[0]
            if key not in keys:
                keys.append((key, i))
            else:
                duplicates.append((key, i))
            if "(" in key or ")" in key:
                if args.fixKeys:
                    fl[i]=fl[i].replace("(","_").replace(")", "_")
                else:
                    badsymbols.append((key, i))
    if len(duplicates) != 0:
        print("Warning! Duplicates found (key, line):")
        print(duplicates)
        print("")
    if len(badsymbols) != 0:
        print("Warning! '(' or ')' symbols found (key, line) — Use option '-k' to replace them with '_':")
        print(badsymbols)
        print("")
    else:
        del(duplicates)
#####################################

# try:
#     f = open(args.outFile, "w", encoding="utf8")
# except Exception as e:
#     print (e)
#     sys.exit()

for element in fl:
    args.outFile.write(element)

