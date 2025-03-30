from rest_framework.exceptions import ValidationError


def validator_materials_description(field):
    """
    Валидатор, проверяющий, что в описании нет ссылок на сторонние ресурсы
    """

    if "youtube.com" not in field:
        raise ValidationError("This field is not OK")