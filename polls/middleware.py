import datetime
import json
import time
from threading import local

from django.db import connection

thread_locals = local()


class RequestTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_locals.path = request.path
        thread_locals.sql_count = 0
        thread_locals.sql_total = 0
        timestamp = time.monotonic()

        response = self.get_response(request)
        
        query_count = len(connection.queries)

        data = {
            'path': request.path,
            'SQL total': query_count,
            'time': f'{datetime.datetime.now()}'[:22],
            'request_total': time.monotonic() - timestamp,
        }
        print(data)
        with open('request.log', 'a') as f:
            f.write(json.dumps(data) + '\n')

        thread_locals.sql_total = 0
        thread_locals.sql_count = 0
        thread_locals.path = ''

        return response
