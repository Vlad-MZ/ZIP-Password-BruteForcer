# !/usr/bin/python
# -*- coding utf-8 -*-

#
# ZIP Password BruteForcer
#   Prototype:
#       https://codeby.net/threads/brutim-arxivy-zip-rar-ispolzuja-python.65986/
#   Example:
#           ZIP-Password-BruteForcer.py -f OurZIP.zip -d our_dictionary.txt
#
#   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#   Extract files from an encrpyted zip file with python3
#       https://gist.github.com/colmcoughlan/db1384156b8efe6676c9a6cc47756933
#
#   Take care, python3's zipfile only supports encrypted zip files that use
#   CRC-32 based encryption This seems to be the default for the "zip" program
#   on linux, but this doesn't work for AES encryption, or for many Windows based
#   zip solutions
#   See https://github.com/python/cpython/blob/3.6/Lib/zipfile.py for more details
#   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import os
import argparse
import zipfile
from time import time


start_time = None

def crack_on_word_list(zip_, word_list_file):
    i = 0
    with open(word_list_file, "r") as f:
        passes = f.readlines()
        for x in passes:
            i += 1
            password = x.split("\n")[0]
            try:
                #zip_.extractall(pwd=password)
                zip_.extractall(pwd=bytes(password, 'utf-8'))
                global start_time
                duration = time() - start_time
                print("\n [*] crack_on_word_list: Password Found :)\n" + " [*] Password: {}\n".format(password))
                print(" [***] Took {0} seconds to crack the Password. That is, {1:8.3f} attempts per second.".format(duration, i / duration))
                return password
            except Exception as ex:
                pass
    return None

def crack_on_popular(zip_):
    with open('Data/100-password-list-top-10000.txt', encoding = 'utf-8') as f:
        passes = f.read().split('\n')
        i = 0
        for x in passes:
            i += 1
            password = x.split("\n")[0]
            #password = password.encode('utf-8')
            try:
                zip_.extractall(pwd=bytes(password,'utf-8'))
                global start_time
                duration = time() - start_time
                print("\n [*] crack_on_word_list: Password Found :)\n" + " [*] Password: {}\n".format(password))
                print(" [***] Took {0} seconds to crack the Password. That is, {1:8.3f} attempts per second.".format(duration, i / duration))
                return password
            except Exception as ex:
                pass
    return None

def crack_with_brute_force(zip_):

    #alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    alphabet = '0123'   #'abcd'
    base = len(alphabet)

    iterations = 0
    i = 0
    length = 0
    while True:
        # i: 10 -> base
        iterations += 1
        password = ''
        temp = i
        while temp != 0:
            rest = temp % base
            temp = temp // base
            password = alphabet[rest] + password

        # while len(password) < length:
        #     password = '0' + password
        password = alphabet[0] * (length - len(password)) + password

        print(length, i, password)
        try:
            #zip_.extractall(pwd=password)
            zip_.extractall(pwd=bytes(password, 'utf-8'))
            global start_time
            duration = time() - start_time
            print("\n [*] crack_on_word_list: Password Found :)\n" + " [*] Password: {}\n".format(password))
            print(" [***] Took {0} seconds to crack the Password. That is, {1:8.3f} attempts per second.".format(duration,
                                                                                                iterations / duration))
            return password
        except Exception as ex:
            print(ex)
            pass

        if password == alphabet[-1] * length:
            length += 1
            if length > base:
                break
            i = 0
        else:
            i += 1

    return None

def run(zip_file, dictionary_file):
    if not os.path.exists(zip_file) or not os.path.isfile(zip_file):
        print(" [!] Please check the file's Path. It doesn't seem to be existed.")
        return
    if dictionary_file is not None:
        if not os.path.exists(dictionary_file) or not os.path.isfile(dictionary_file):
            print(" [!] Please check the file's Path for WordsList. It doesn't seem to be existed.")
            return
    else:
        print(" [?] You didn't point Passwords List File (dictionary")

    if zipfile.is_zipfile(zip_file) != True:
        print(" [!] Please check ZIP file's Path. It doesn't seem to be a ZIP file.")
        return

    start_time = time()
    password = None
    with zipfile.ZipFile(zip_file) as zip_:
        while True:
            if dictionary_file is not None:
                password = crack_on_word_list(zip_, dictionary_file)
                if password is not None:
                    break
            password = crack_on_popular(zip_)
            if password is not None:
                break
            password = crack_with_brute_force(zip_)
            break

    if password is not None:
        end_time = time()
        print("\n [*] Password Found :)\n" + " [*] Password: {}\n".format(password))
        print(" [***] Took {0:8.2f} seconds to crack the Password.".format(end_time - start_time))
    else:
        print(" [X] Sorry, Password Not Found :(")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        '--file <archive>' + '--dict <dictionary>')

    parser.add_argument('-f', '--file',  dest='archieve', required=True,
                        type=str, help='Archieve file')
    parser.add_argument('-d', '--dict',  dest='dictionary', required=True,
                        type=str, help="Dictionary file")
    args = parser.parse_args()

    # zipfile_path = args.archieve
    # word_list_file = args.dictionary
    run(args.archieve, args.dictionary)
