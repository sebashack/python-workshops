import http.client


def create_http_connection(host, port):
    conn = http.client.HTTPConnection(host, port, timeout=10)

    return conn


def create_https_connection(host):
    conn = http.client.HTTPSConnection(host, 443, timeout=10)

    return conn
