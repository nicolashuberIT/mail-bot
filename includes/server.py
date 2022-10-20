#header files

import smtplib, ssl
import includes.constants

def server_password():
    global password
    password = input("Enter mailserver password: \n -- input --> ");

#connect to srdmz.08.kzo.ch-server

def connect_server():
    global mailserver

    context = ssl.create_default_context();

    mailserver = smtplib.SMTP(includes.constants.server,includes.constants.port);
    mailserver.ehlo();
    mailserver.starttls(context=context)
    mailserver.ehlo();
    mailserver.login(includes.constants.login, password);

#print server status

def print_serverstatus():
    print("-- output --> outputting server status:");
    print(f'------ server --> {includes.constants.server}');
    print(f'------ port --> {includes.constants.port}');
    print(f'------ login --> {includes.constants.login}');
    print(f'------ message --> Successfully reached {includes.constants.server} server at port {includes.constants.port} for {includes.constants.login}. The emails can be sent now! \n');