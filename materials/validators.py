import logging
import re

from rest_framework.exceptions import ValidationError


def validator_materials_description(field):
    """
    Валидатор, проверяющий, что в описании нет ссылок на сторонние ресурсы
    """
    url_pattern = re.compile(r"https?://[\w.-]+(?:\.[a-zA-Z]{2,})+")
    urls = url_pattern.findall(field)
    for url in urls:
        if "youtube.com" not in url:
            raise ValidationError("This field contains non-YouTube links")
