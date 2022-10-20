import includes.constants

def admin_password():
    admin_password = input("Please enter the admin password to run the mailing program! \n -- input --> ")

    if admin_password ==  includes.constants.admin_key:
        print("-- output --> The correct key was entered! Let's go. \n")

    else:
        print("-- output --> Wrong user key! The program was quit unexpectedly... \n");
        exit();

def execute_program():
    programm_start = input("Enter 'start' the run the mailing program! \n -- input --> " );

    if programm_start == includes.constants.program_key:
        print("-- output --> The start key was entered! The program can be executed now! \n");

    else:
        print("-- output --> Wrong start key. The mailing was quit unexpectedly... \n");
        quit();

