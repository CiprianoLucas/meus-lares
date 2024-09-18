from django.core import serializers
from users.models import User
from requests.models import Request
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
            requests = user.request_requester.all()
            requests_json = serializers.serialize('json', requests, fields=('title', 'status', 'created_at'))
            requests_data = json.loads(requests_json)
            
            content = json.dumps({"requests": requests_data})
            content += 'A: ANDAMENTO, C: CONCLUIDO, P: PENDENTE'
            return content
        except:
            return 'Erro ao procurar os chamados'
        