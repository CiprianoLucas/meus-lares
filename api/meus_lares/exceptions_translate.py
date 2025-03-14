import re

from django.utils.translation import gettext as _


def translate(response):

    if response is not None:
        if response.status_code == 404:
            response = translate_404(response)

    return response


def translate_404(response):
    detail = response.data.get("detail", "")

    match = re.search(r"No (\w+) matches the given query\.", detail)

    if match:
        object_name = match.group(1)
        word = _(object_name).lower()
        response.data["detail"] = _("No matching %(word)s were found") % {"word": word}

    return response
