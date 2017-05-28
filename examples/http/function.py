from cloudfn.http import handle_http_event, Response


def handle_http(req):
    return Response(
        status_code=200,
        body={'key': 2},
        headers={'content-type': 'application/json'},
    )


handle_http_event(handle_http)
