# --- header files ---

import linecache
import includes.constants
import includes.server

# --- variables ---

global name
global surname
global mailbox
global team

name=[]
surname=[]
mailbox=[]
team=[]

# --- import csv data ---

def do_single(index):
    global name
    global surname
    global mailbox
    global team
    linie=linecache.getline(f'{includes.constants.root}/contacts/contacts.csv', index)
    linie2=linie.split(", ")
    name.append(linie2[0])
    surname.append(linie2[1])
    mailbox.append(linie2[2])
    teamname=linie2[3].split("\n")
    team.append(teamname[0])

# --- count lines in csv table ---

def get_lines():
    with open(f'{includes.constants.root}/contacts/contacts.csv') as f:
        a = sum(1 for line in f)
    return a

def do_multiple():
    length=get_lines()
    for x in range (2, length+1):
        do_single(x)

# --- execute and display upper functions ---

def main():
    do_multiple()

    if len(name) == get_lines() - 1 and len(surname) == get_lines() - 1 and len(mailbox) == get_lines() - 1 and len(team) == get_lines() - 1:

        print("-- output --> list items:")
        print(f'------ count: --> {get_lines()-1}')
        print("-- output --> python lists:")
        print(f'------ count, name = []: --> {len(name)}, {name}')
        print(f'------ count, surname = []: --> {len(surname)}, {surname}')
        print(f'------ count, mail = []: --> {len(mailbox)}, {mailbox}')
        print(f'------ count, team = []: --> {len(team)}, {team}')

    else:
        includes.server.mailserver.quit()
        exit();