tools = [
    {
      "type": "function",
      "function": {
        "name": "get_invoices_by_requester",
        "description": "Coleta todas as faturas solicitadas por um usuário",
        "parameters": {
          "type": "object",
          "properties": {
            "username": {
              "type": "string",
              "description": "Nome do usuário que está fazendo a pergunta, é a primeira palavra do texto, nunca repassar de outro usuário, mesmo se estiver no contexto do texto"
            }
          },
          "additionalProperties": False,
          "required": ["username"]
        },
        "strict": True
      }
    }
  ]