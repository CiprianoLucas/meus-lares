from django.core.management.base import BaseCommand
from invoices.management.functions.celesc import CelescInvoices



class Command(BaseCommand):
    help = "Get emails from fatura@celesc.com.br"
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Buscando emails de fatura@celesc.com.br...")
        celesc_invoices = CelescInvoices()
        celesc_invoices.post_celesc_invoices()
        
    