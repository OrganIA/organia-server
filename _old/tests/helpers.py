def assert_response(
        response, status_code=None, data=None, include=None, type_=None
):
    if hasattr(response, 'json'):
        got = response.json()
        status_code = status_code or 200
    else:
        got = response
    try:
        if status_code:
            assert response.status_code == status_code
        if type_:
            assert isinstance(got, type_)
        if data:
            assert got == data
        if include:
            assert all(x in got.items() for x in include.items())
    except AssertionError as e:
        print('Got:', got)
        raise e
    return got
