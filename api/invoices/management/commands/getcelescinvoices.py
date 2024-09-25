from django.core.management.base import BaseCommand
from invoices.functions.celesc import CelescInvoices

class Command(BaseCommand):
    help = "Get emails from CELESC"
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Buscando emails de fatura@celesc.com.br...")
        celesc_invoices = CelescInvoices()
        try:
            response = celesc_invoices.post_celesc_invoices()
            self.stdout.write(self.style.SUCCESS(response))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocorreu um erro: {e}"))
        
    