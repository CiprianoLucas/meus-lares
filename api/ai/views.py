import json

from openai import OpenAI
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .functions import AiFunctions
from .props import tools
from .serializers import OpenaiChatSerializer


# Create your views here.
@api_view(["POST"])
def openai_chat(request):

    serializer = OpenaiChatSerializer(data=request.data)

    if serializer.is_valid():

        input_message = serializer.validated_data["message"]
        username = request.user.username

        messages = [{"role": "user", "content": f"{input_message}"}]

        openai = OpenAI()

        openai_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300,
            tools=tools,
        )

        response = openai_response.choices[0].message
        tool_call = openai_response.choices[0].message.tool_calls

        if tool_call:
            function = tool_call[0].function.name
            args = json.loads(tool_call[0].function.arguments)
            args["username"] = username

            ai_function = AiFunctions(function, args)
            data = ai_function.exec()
            messages.append(response)
            messages.append(
                {
                    "role": "tool",
                    "content": data,
                    "tool_call_id": response.tool_calls[0].id,
                }
            )
            openai_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=300,
                tools=tools,
            )
            response = openai_response.choices[0].message

        return Response({"response": response.content}, status=status.HTTP_200_OK)

    # Retorna erro se os dados forem inválidos
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
