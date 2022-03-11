"""
Contains all the functions needed for the link_down blueprint.
Things such as routes and forms should be in separate files.
"""


def build_response_data(data: dict) -> dict:
    """
    Takes the request data and extracts the relevant matches for the required data.

    When all expected parameters are recieved, they are returned in a sorted dictionary.

    >>> build_response_data({
    ... "event_url": "https://example.com",
    ... "timestamp": "2021-10-15 23:20:01",
    ... "causing_ci": "hostname.example.com"
    ... })
    {'causing_ci': 'hostname.example.com', 'event_url': 'https://example.com', 'timestamp': '2021-10-15 23:20:01'}


    When unexpected parameters are recieved, they are omitted from the returned dictionary.

    >>> build_response_data({"alphabet": "abcdefghijklmnopqrstuvwxyz",
    ... "event_url": "https://example.com", "timestamp": "2021-10-15 23:20:01"})
    {'event_url': 'https://example.com', 'timestamp': '2021-10-15 23:20:01'}

    :param data: Raw request data in dict or JSON format
    :return:  Relevant request data in alphabetical order
    """
    response = {}
    expected_parameters = [
        "causing_ci", "event_text", "event_url", "timestamp"
    ]

    for parameter in expected_parameters:
        if parameter in data:
            response.update({f"{parameter}": data[parameter]})
    return response
