# --- header files ---

from includes import server, constants, contacts
from email.utils import formatdate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from fpdf import FPDF
import os


# --- final check / final command to start mailing ---

def final_check():
    print("-- output --> mailing overview");
    print(f'------ working directory: --> {os.getcwd()}')
    print(f'------ event: --> {constants.event}');
    print(f'------ event info: --> {constants.event_info}');
    print(f'------ sender mail: --> {constants.sender_mail}');
    print(f'------ response mail: --> {constants.response_mail}');
    print(f'------ attachments: --> "{constants.attachment_name}_i.pdf"');
    print(f'------ courtesy: --> {constants.courtesy}\n')

    initialize = input("To start the mailing now, enter 'final'!\n -- input --> ")

    if initialize == "final":
        print("-- output --> The mailing is now being initialized! Almost done. :-)");

    else:
        print("-- output --> The program was quit unexpectedly.")
        server.mailserver.quit()
        exit()

# --- mailing ---

def send():

    f = open(f"{constants.root}/system/txt/systemLog.txt", "w");

    limit = len(contacts.name);

    print("-- output --> feedback loop:");

    for i in range(0, limit, 1):

        if constants.courtesy == 0:
            message = f'Hallo {contacts.name[i]}! \n\n Die Volleynight naht! Weil du dich bei der Anmeldung als Captain registriert hast, senden wir dir im Anhang die Rechnung deines Teams. Wir bitten dich, diese der Einfachheit zuliebe baldmöglichst zu begleichen, wobei dennoch eine Zahlungsfrist von 10 Tagen gilt. \n\n Zur Kontrolle deine Captain-Angaben: \n - Vorname, Name: {contacts.name[i]} {contacts.surname[i]} \n - E-Mail: {contacts.mailbox[i]} \n - Team: {contacts.team[i]} \n\n Im Anhang findest du: \n - "{constants.attachment_name}_{i + 1}.pdf" \n\n Solltest du einen Fehler feststellen, wendest du dich bitte per Mail an {constants.response_mail}. Beachte auch, dass diese E-Mail automatisiert mit einem Python-Skript versendet wurde. Reaktionen an {constants.sender_mail} können daher nicht beantwortet werden. \n\n In den nächsten Tagen werden automatisiert Tickets mit QR-Code und Besucher-ID erstellt und an jeden/jede Teilnehmer/-in individuell versendet. \n\n Ausführliche Informationen zum Event finden sich weiterhin auf unserer Website unter {constants.event_info}. Gerne geben wir dir bei individuellen Fragen auch per E-Mail Auskunft. \n\n Wir freuen uns auf eine tolle Volleynight und bedanken uns für die Unterstützung bei der Abwicklung der Zahlung. \n\n Herzliche Grüsse \n SO KZO \n\n _____________________________ \n Kantonsschule Zürcher Oberland \n\n SO KZO \n so@kzo.ch \n https://www.sorg.kzo.ch';

        else:
            message = f'Hallo {contacts.name[i]} {contacts.surname[i]}! \n\n Die Volleynight naht! Weil Sie sich bei der Anmeldung als Captain registriert haben, senden wir Ihnen im Anhang die Rechnung Ihres Teams. Wir bitten Sie, diese baldmöglichst zu begleichen. Selbstverständlich gilt dennoch eine Zahlungsfrist von 10 Tagen, weshalb der Zahlungsvorgang von der Teilnahme an der Volleynight entkoppelt ist. \n\n Zur Kontrolle Ihre Captain-Angaben: \n - Vorname, Name: {contacts.name[i]} {contacts.surname[i]} \n - E-Mail: {contacts.mailbox[i]} \n - Team: {contacts.team[i]} \n\n Im Anhang finden Sie: \n - "{constants.attachment_name}_{i + 1}.pdf" \n\n Sollten Sie einen Fehler feststellen, wenden Sie sich bitte per Mail an {constants.response_mail}. Beachten Sie auch, dass diese E-Mail automatisiert mit einem Python-Skript versendet wurde. Reaktionen an {constants.sender_mail} können daher nicht beantwortet werden. \n\n In den nächsten Tagen werden automatisiert Tickets mit QR-Code und Besucher-ID erstellt und an jeden/jede Teilnehmer/-in individuell versendet. \n\n Ausführliche Informationen zum Event finden sich weiterhin auf unserer Website unter {constants.event_info}. Gerne geben wir Ihnen bei individuellen Fragen auch per E-Mail Auskunft. \n\n Wir freuen uns auf eine tolle Volleynight und bedanken uns für die Unterstützung bei der Abwicklung der Zahlung. \n\n Herzliche Grüsse \n SO KZO \n\n _____________________________ \n Kantonsschule Zürcher Oberland \n\n SO KZO \n so@kzo.ch \n https://www.sorg.kzo.ch';

        msg = MIMEMultipart();
        msg['Subject'] = f'{constants.event} | Team {contacts.team[i]} | SO KZO';
        msg['From'] = constants.sender_mail;
        msg['Date'] = formatdate(localtime=True);
        msg['To'] = contacts.mailbox[i];
        msg['CC'] = constants.mail_systemProtocol;
        msg.attach(MIMEText(message))

        attachmentPath = rf'{constants.root}/attachments/{constants.attachment_name}_{i+1}.pdf'
        filename = f'{constants.attachment_name}_{i+1}.pdf'

        fileformat=filename.format(Path(attachmentPath).name)

        try:
            with open(attachmentPath, "rb") as attachment:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment', filename=fileformat)
                msg.attach(part)
        except Exception as e:
            f.write(f"error: (mail, captain, team): {contacts.mailbox[i]}, {contacts.name[i]} {contacts.surname[i]}, Team {contacts.team[i]}! \n");
            print(f'------ error {str(e)}: --> mail could not be sent to {contacts.mailbox[i]} and the following contacts as the attachment "{constants.attachment_name}_{i + 1}.pdf" could not be found. Please rerun the programm manually.');

            if str(e) == f"[Errno 2] No such file or directory: '{attachmentPath}'":
                print(f'------ error: --> mail could not be sent to {contacts.mailbox[i]} and the following contacts as the attachment "{constants.attachment_name}_{i + 1}.pdf" could not be found. Please rerun the programm manually.');
                f.write(f"error: (mail, captain, team): {contacts.mailbox[i]}, {contacts.name[i]} {contacts.surname[i]}, Team {contacts.team[i]}! \n");
                server.mailserver.quit()
                exit();

        message_final = msg.as_string();
        server.mailserver.sendmail(constants.sender_mail, contacts.mailbox[i], message_final);
        f.write(f"Success: (mail, captain, team): {contacts.mailbox[i]}, {contacts.name[i]} {contacts.surname[i]}, Team {contacts.team[i]}! \n");
        print(f'------ email sent to (mail, captain, team, status): --> {contacts.mailbox[i]}, {contacts.name[i]} {contacts.surname[i]}, Team {contacts.team[i]}, successful');

    f.close();
    print("-- output --> mailing successfully executed! \n");

# --- generating system protocol ---
def generateProtocol():
    pdf = FPDF();
    pdf.add_page();
    pdf.set_font("Arial", size=9);
    f = open(rf'{constants.root}/system/txt/systemLog.txt', "r");
    for x in f:
        pdf.cell(200, 10, txt=x, ln=1, align='C');
    pdf.output(rf'{constants.root}/system/pdf/{constants.attachment_systemProtocol}.pdf');

# --- sending system protocol ---

def sendProtocol():

    message = f"Hallo! \n\n Es handelt sich hierbei um ein automatisch erstelltes Systemprotokoll, das zur Kontrolle des vorangehenden Mailings dient. \n\n Angaben zum Mailing: \n- Datum: {formatdate(localtime=True)} \n - Event: {constants.event} \n\n Im Anhang findet sich daher: \n -{constants.attachment_systemProtocol} \n\n _____________________________ \n Kantonsschule Zürcher Oberland \n\n SO KZO \n so@kzo.ch \n https://www.sorg.kzo.ch";

    msg = MIMEMultipart();
    msg['Subject'] = f'Systemprotokoll | Mailing: {constants.event} | SO KZO';
    msg['From'] = constants.sender_mail;
    msg['Date'] = formatdate(localtime=True);
    msg['To'] = constants.mail_systemProtocol;
    msg.attach(MIMEText(message))

    attachmentPath = rf'{constants.root}/system/pdf/{constants.attachment_systemProtocol}.pdf'
    filename = f'{constants.attachment_systemProtocol}.pdf'

    fileformat = filename.format(Path(attachmentPath).name)

    try:
        with open(attachmentPath, "rb") as attachment:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=fileformat)
            msg.attach(part)
    except Exception as e:
        print(f'------ error {str(e)}: --> mail could not be sent to {constants.mail_systemProtocol} as the attachment "{constants.attachment_systemProtocol}.pdf" could not be found. Please rerun the programm manually.');

        if str(e) == f"[Errno 2] No such file or directory: '{attachmentPath}'":
            print(f'------ error {str(e)}: --> mail could not be sent to {constants.mail_systemProtocol} as the attachment "{constants.attachment_systemProtocol}.pdf" could not be found. Please rerun the programm manually.');
            server.mailserver.quit()
            exit();

    message_final = msg.as_string();
    server.mailserver.sendmail(constants.sender_mail, constants.mail_systemProtocol, message_final);
    print(f'-- output --> protocol sent to (mail, status): {constants.mail_systemProtocol}, successful');

def quitServer(mailserver):
    mailserver.quit()
    print("-- output --> The server connection was automatically terminated.\n");
