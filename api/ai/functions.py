import json

from django.core.serializers.json import DjangoJSONEncoder

from invoices.models import Invoice
from users.models import User


class AiFunctions:

    def __init__(self, function, args) -> None:
        self.__args = args

        match function:
            case "get_invoices_by_requester":
                self.__function = self.get_invoices_by_requester

    def exec(self) -> str:
        return self.__function(self.__args)

    def get_invoices_by_requester(self, args: dict) -> str:
        try:
            username = args["username"]
            user = User.objects.get(username=username)
            invoices = Invoice.objects.filter(relation__resident=user).values(
                "ticket_number",
                "value",
                "relation__company",
                "relation__place__name",
                "relation__unit_number",
                "created_at",
            )
            invoices_data = [
                {
                    "numero_bolero": invoice["ticket_number"],
                    "valor": invoice["value"],
                    "empresa": invoice["relation__company"],
                    "nome_do_local": invoice["relation__place__name"],
                    "unidade_consumidora": invoice["relation__unit_number"],
                    "data_recebimento": invoice["created_at"],
                }
                for invoice in invoices
            ]
            list_invoices = list(invoices_data)
            invoices_json = json.dumps(list_invoices, cls=DjangoJSONEncoder)
            content = invoices_json
            content += """ - Só passar os dados que o usuário pediu, nenhum outro."""
            return content
        except Exception as e:
            print(str(e))
            return "Erro ao procurar as faturas"
