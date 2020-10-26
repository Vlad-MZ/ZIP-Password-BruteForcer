#
#
#   Source: "Брутим архивы ZIP/RAR используя python."
#       https://codeby.net/threads/brutim-arxivy-zip-rar-ispolzuja-python.65986/
#   It was written on python 2.x
#       time python3  brutilka.py -f evil.zip -d dictionary
#       time python3  brutilka.py -f evil.rar -d dictionary
#
import zipfile
import rarfile
import argparse


def cutMagicNumbers(archive):
    with open(archive, 'rb') as file:
        currentType = file.read(2).decode()
    return launcher(currentType)


def launcher(extension):
    return {'Ra': prepareBruteRar,
            'PK': prepareBruteZip,
            }.get(extension, 'Not Found')


def prepareBruteZip(archive, dictionary):
    '''
    Ограничения file <ZipName> == 2.0
    type(pwd) == byte
    '''

    zArchive = zipfile.ZipFile(archive)
    with open(dictionary, 'r') as wordlist:
        for word in wordlist.readlines():
            password = word.strip('\n').encode('ascii')
            brute(zArchive, password)


def brute(archive, password):
    try:
        archive.extractall(pwd=password)
        print('[+] Password is {}'.format(password))
    except:
        pass


def prepareBruteRar(archive, dictionary):
    '''
    type(pwd) == str
    requirements installed unrar
    '''
    rArchive = rarfile.RarFile(archive)
    with open(dictionary, 'r') as wordlist:
        for word in wordlist.readlines():
            password = word.strip('\n')
            brute(rArchive, password)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        '--file <archive>' + '--dict <dictionary>')

    parser.add_argument('-f', '--file',  dest='archive', required=True,
                        type=str, help='Archive file')
    parser.add_argument('-d', '--dict',  dest='dictionary', required=True,
                        type=str, help="Dictionary file")
    args = parser.parse_args()

    cutMagicNumbers(args.archive)(args.archive, args.dictionary)