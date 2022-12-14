# --- header files ---

import includes.initialisation
import includes.server
import includes.mailing
import includes.contacts

# --- initialisation ---

print("\n<------- START: INITIALISATION PROCESS------> \n");

includes.initialisation.admin_password();
includes.initialisation.execute_program();

print("<------- END: INITIALISATION PROCESS ------>");

# --- connection to mail server ---

print("<------- START: CONNECTION TO MAIL SERVER ------> \n");

includes.server.server_setup()
includes.server.server_password();
includes.server.connect_server();
includes.server.print_serverstatus();

print("<------- END: CONNECTION TO MAIL SERVER ------>");

# --- importing contacts ---

print("<------- START: IMPORTING CONTACTS ------> \n");

includes.contacts.main();

print("\n<------- END: IMPORTING CONTACTS ------>");

# --- mailing process ---

print("<------- START: MAILING PROCESS ------> \n");

includes.mailing.final_check();
includes.mailing.send();

print("<------- END: MAILING PROCESS ------>");

# --- system protocol ---

print("<------- START: SYSTEM PROTOCOL ------>\n");

includes.mailing.sendProtocol();

print("\n<------- END: SYSTEM PROTOCOL ------>");

# --- termination ---

print("<------- START: SERVER TERMINATION ------>\n");

includes.mailing.quitServer(includes.server.mailserver);

print("<------- END: SERVER TERMINATION ------> \n");

print("Congrats! The mailing has been completed. :-D");