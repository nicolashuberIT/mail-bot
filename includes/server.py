# --- header files ---

import smtplib
import ssl

# --- input server bascis ---

def server_setup():

    global server
    global port
    global login
    global sender

    server = input("Enter the server adress: \n -- input --> ")
    print(f"-- output --> server adress: {server}");
    port = input("Enter the server port: \n -- input --> ")
    print(f"-- output --> server port: {port}");
    login = input("Enter the server login key: \n -- input --> ")
    print(f"-- output --> server login key: {login} \n");

# --- server authentication ---

def server_password():

    global password
    password = input("Enter mailserver password: \n -- input --> ");

# --- server connection ---

def connect_server():

    global mailserver

    context = ssl.create_default_context();

    mailserver = smtplib.SMTP(server,port);
    mailserver.ehlo();
    mailserver.starttls(context=context)
    mailserver.ehlo();
    mailserver.login(login, password);

# --- server status ---

def print_serverstatus():
    print("-- output --> outputting server status:");
    print(f'------ server --> {server}');
    print(f'------ port --> {port}');
    print(f'------ login --> {login}');
    print(f'------ message --> Successfully reached {server} server at port {port} for {login}. The emails can be sent now! \n');