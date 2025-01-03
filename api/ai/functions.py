import json

from django.core.serializers.json import DjangoJSONEncoder

from condo_requests.models import CondoRequest
from users.models import User


class AiFunctions:

    def __init__(self, function, args) -> None:
        self.__args = args

        match function:
            case "get_requests_by_requester":
                self.__function = self.get_requests_by_requester

    def exec(self) -> str:
        return self.__function(self.__args)

    def get_requests_by_requester(self, args: dict) -> str:
        try:
            username = args["username"]
            user = User.objects.get(username=username)
            requests = CondoRequest.objects.filter(relation__resident=user).values(
                "ticket_number",
                "value",
                "relation__company",
                "relation__place__name",
                "relation__unit_number",
                "created_at",
            )
            requests_data = [
                {
                    "numero_bolero": request["ticket_number"],
                    "valor": request["value"],
                    "empresa": request["relation__company"],
                    "nome_do_local": request["relation__place__name"],
                    "unidade_consumidora": request["relation__unit_number"],
                    "data_recebimento": request["created_at"],
                }
                for request in requests
            ]
            list_requests = list(requests_data)
            requests_json = json.dumps(list_requests, cls=DjangoJSONEncoder)
            content = requests_json
            content += """ - Só passar os dados que o usuário pediu, nenhum outro."""
            return content
        except Exception as e:
            print(str(e))
            return "Erro ao procurar as faturas"
