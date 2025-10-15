import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# NOTA: Il file 'credentials.json' deve essere ottenuto dalla Google Cloud Console
# e contenere le credenziali per un'applicazione di tipo "Desktop" o "Web".
# Per un account di servizio, il flusso è leggermente diverso.
# Questo codice presuppone un flusso in cui l'utente autorizza l'app.

def get_gmail_service():
    """
    Crea e restituisce un'istanza del servizio Gmail.
    Le credenziali vengono cercate in un file token.json (creato al primo login)
    o tramite il file credentials.json.
    """
    creds = None
    # Il file token.json memorizza i token di accesso e refresh dell'utente.
    # Viene creato automaticamente quando il flusso di autorizzazione
    # viene completato per la prima volta.
    # if os.path.exists('token.json'):
    #     creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.send'])

    # Se non ci sono credenziali valide, l'utente deve effettuare il login.
    # Questo è un punto critico: in un'app web, questo flusso deve essere gestito
    # tramite le viste di Django, reindirizzando l'utente alla pagina di consenso di Google.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', ['https://www.googleapis.com/auth/gmail.send'])
    #         creds = flow.run_local_server(port=0)
    #     # Salva le credenziali per la prossima esecuzione
    #     with open('token.json', 'w') as token:
    #         token.write(creds.to_json())

    # Per ora, restituiamo None. La logica di autenticazione completa
    # richiede un'integrazione più profonda con le viste.
    # service = build('gmail', 'v1', credentials=creds)
    # return service
    return None


def send_email(service, to, subject, body):
    """
    Crea e invia un'email.
    """
    try:
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(f"Messaggio inviato. ID: {send_message['id']}")
    except HttpError as error:
        print(f"Si è verificato un errore: {error}")
        send_message = None
    return send_message