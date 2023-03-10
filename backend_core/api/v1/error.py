from collections import namedtuple
from http import HTTPStatus
from enum import IntEnum


class ServerStatus(IntEnum):
    """
    Additional server status code and reason phrases
    Notes:
        CLIENT_CLOSED_REQUEST - 499
        UNKNOWN_ERROR - 520
        INVALID_SSL_CERTIFICATE - 526
    """

    def __new__(cls, value, phrase, description=''):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.phrase = phrase
        obj.description = description
        return obj

    CLIENT_CLOSED_REQUEST = (499,
                             'Client Closed Request',
                             'Full description: Client Closed Request')
    VERSION_NOT_SUPPORTED = (505,
                             'Version Not Supported',
                             'Cannot fulfill request')
    UNKNOWN_ERROR = (520,
                     'Unknown Error',
                     'Full description: Unknown Error')
    INVALID_SSL_CERTIFICATE = (526,
                               'Invalid SSL Certificate',
                               'Full description: Invalid SSL Certificate')


def check_error_pattern(status: str) -> namedtuple:
    """
    Checks the error name against the existing error types supported by
    the server. The error name is passed as a "status" parameter.
    Args:
        status (str): error name
    Returns:
        (namedtuple): named tuple with three value, where
                        ``value`` - status code of error
                        ``phrase`` - status name of error
                        ``description`` - short description of the error
    """

    CatchError = namedtuple('CatchError', ['code',
                                           'status',
                                           'detail'])
    try:
        getattr(HTTPStatus, status).value
    except AttributeError:
        http_status_not_found = True
    except TypeError:
        raise TypeError("".join(("Wrong status type passed",
                                 f" it should be {type(str())}",
                                 f" but it was passed {type(status)}")))
    else:
        obj = getattr(HTTPStatus, status)
        http_status_not_found = False

    if http_status_not_found:
        try:
            getattr(ServerStatus, status)
        except AttributeError:
            raise AttributeError("Received a non-existent error status")
        else:
            obj = getattr(ServerStatus, status)

    return CatchError(obj.value,
                      obj.phrase,
                      obj.description)
