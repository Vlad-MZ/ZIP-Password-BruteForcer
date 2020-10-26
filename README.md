# ZIP-Password-BruteForcer

Project is to acquaintance with ZIP archive password brute force.


 ZIP Password BruteForcer
   Prototype:
       https://codeby.net/threads/brutim-arxivy-zip-rar-ispolzuja-python.65986/
   
   Example:
           ZIP-Password-BruteForcer.py -f OurZIP.zip -d our_dictionary.txt

   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   
  Found issue under WIN:
   
   Extract files from an encrpyted zip file with python3
       https://gist.github.com/colmcoughlan/db1384156b8efe6676c9a6cc47756933

   Take care, python3's zipfile only supports encrypted zip files that use
   CRC-32 based encryption This seems to be the default for the "zip" program
   on linux, but this doesn't work for AES encryption, or for many Windows based
   zip solutions
   See https://github.com/python/cpython/blob/3.6/Lib/zipfile.py for more details
   
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
