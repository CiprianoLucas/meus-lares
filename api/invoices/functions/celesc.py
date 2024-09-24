from bs4 import BeautifulSoup
import imaplib
import email
import environ
import os
from email.header import decode_header
from django.db import transaction
from invoices.models import Invoice, RelationInvoice

# Inicializar environ
env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

class CelescInvoices:
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    
    def __init__(self):
        pass
    
    def post_celesc_invoices(self):
        email_bodies = self._get_celesc_emails()
        invoices_to_create = []

        for body in email_bodies:
            unit = self._extract_unity_celesc(body)
            value = self._extract_value_celesc(body)
            ticket_number = self._extract_ticket_celesc(body)

            relations = RelationInvoice.objects.filter(unit_number=unit).distinct()
            
            if not (unit and value and ticket_number and relations):
                continue

            for relation in relations:
                invoice = Invoice(
                    relation=relation,
                    value=value,
                    ticket_number=ticket_number
                )
                invoices_to_create.append(invoice)

        if invoices_to_create:
            with transaction.atomic():
                Invoice.objects.bulk_create(invoices_to_create)
    
    def _get_celesc_emails(self):
        imap = imaplib.IMAP4_SSL(self.EMAIL_HOST)
        imap.login(self.EMAIL_HOST_USER, self.EMAIL_HOST_PASSWORD)
        imap.select("inbox")
        _, messages = imap.search(None, 'FROM', '"lucashcipriano14@gmail.com"')
        email_bodies = []
        messages = messages[0].split(b' ')
        
        for mail_id in messages:
            _, msg_data = imap.fetch(mail_id, "(RFC822)")

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])

                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")

                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/html":
                                body = part.get_payload(decode=True).decode("utf-8")
                                email_bodies.append(body)
                    else:
                        body = msg.get_payload(decode=True).decode("utf-8")
                        email_bodies.append(body)
         
        imap.close()
        imap.logout()
        
        return email_bodies
        
    def _extract_unity_celesc(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")

        strong_tags = soup.find_all("strong", text=lambda t: "Unidade Consumidora" in t if t else "")

        if strong_tags:
            unidade_consumidora_tag = strong_tags[0].find_next_sibling("strong")
            if unidade_consumidora_tag:
                return unidade_consumidora_tag.text.strip()

        return None
    
    def _extract_value_celesc(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        tag = soup.find('strong', text="Valor da fatura:")

        if tag:
            value_str = tag.find_next('td').get_text(strip=True)
            value_str = value_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
            try:
                return float(value_str)
            except ValueError:
                return None

        return None
    
    def _extract_ticket_celesc(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        div = soup.find("div", style="width:600px;text-align:justify;font-family:Verdana,Arial!important;font-size:16px")
        if div:
            h4_tags = div.find_all("h4")

            if len(h4_tags) >= 2:
                ticket_code = h4_tags[1].text.strip()
                return ticket_code

        return None