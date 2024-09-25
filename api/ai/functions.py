from django.core import serializers
from users.models import User
from requests.models import Request
from invoices.models import Invoice
import json

class AiFunctions:
    
    def __init__(self, function, args) -> None:
        self.__args = args
        
        match function:
            case 'get_requests_by_requester':
                self.__function = self.get_requests_by_requester
                
    def exec(self) -> str:
        return self.__function(self.__args)

    def get_requests_by_requester(self, args: dict) -> str:
        try:
            username = args['username']
            user = User.objects.get(username=username)
            invoices = Invoice.objects.filter(relation__resident=user)
            invoices_json = serializers.serialize('json', invoices, fields=('title', 'status', 'created_at'))
            invoices_data = json.loads(invoices_json)
            
            content = json.dumps({"invoices": invoices_data})
            content += 'A: ANDAMENTO, C: CONCLUIDO, P: PENDENTE'
            return content
        except:
            return 'Erro ao procurar os chamados'
        