from utils.constants import MISSING_PARAMETERS_ERROR_MSG
from utils.exceptions import ValidationException


def validate_mandatory(data):
    """Takes an object of required fields and ensures none of the values
    are null.

    Args:
        data (obj): An object of mandatory fields and their provided values.

    Raises:
        ValidationException: If any of the supplied fields are null.

    """
    missing_params = []
    for key, value in data.items():
        if not value or value == '':
            missing_params.append(key)
    if missing_params:
        raise ValidationException(
            MISSING_PARAMETERS_ERROR_MSG.format(
                params=", ".join(missing_params)
            )
        )
