import urllib.parse

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'text/plain; charset=utf-8')]
    start_response(status, headers)

    query_string = environ.get('QUERY_STRING', '')
    get_params = urllib.parse.parse_qs(query_string)

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    
    request_body = environ.get('wsgi.input').read(request_body_size)
    post_params = urllib.parse.parse_qs(request_body.decode('utf-8'))

    response = (
        f"=== GET PARAMETERS ===\n{get_params}\n\n"
        f"=== POST PARAMETERS ===\n{post_params}\n"
    )
    return [response.encode('utf-8')]