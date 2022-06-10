from math import ceil
from flask import request

class BaseController():
    def build_links(self, total, offset, limit):
        url = str(request.url)
        last = total - limit - 1
        if last < 0:
            last = 0
        links = {
            'prev': None,
            'curr': url,
            'next': None,
            'start': url.replace('offset='+str(offset), 'offset=0'),
            'last': url.replace('offset='+str(offset), 'offset=' + str(last)),
        }
        if (offset + limit) < total:
            links['next'] = url.replace(
                'offset='+str(offset),
                'offset='+str(offset+limit)
            )
        if offset > 0:
            new_offset = offset - limit
            if new_offset < 0:
                new_offset = 0
            links['previous'] = url.replace(
                'offset='+str(offset),
                'offset='+str(new_offset)
            )
        return links