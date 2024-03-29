"""
test renderer of python
"""

from collections import defaultdict

from jinja2 import Template

from zerotest.utils.generator_helper import get_name_from_request, dict_to_param_style_code

__author__ = 'Hari Jiang'


class Renderer(object):
    def __init__(self, options, match_options):
        self.options = options
        self.match_options = match_options

    def prepare(self, records):
        cases = []
        func_names = defaultdict(int)
        endpoint = self.options.get('endpoint', None)
        ignore_all_headers = self.match_options.get('ignore_all_headers', None)
        ignore_headers = self.match_options.get('ignore_headers', None)
        if not ignore_all_headers and ignore_headers:
            ignore_headers = set(map(lambda h: h.upper(), ignore_headers))

        for (req, res) in records:
            func_name = get_name_from_request(req)
            count = func_names[func_name]
            func_names[func_name] = count + 1
            if count > 0:
                func_name = '{}_{}'.format(func_name, count)

            if ignore_all_headers:
                content_type = res.get_header('content-type')
                if content_type:
                    res.headers = {'content-type': content_type}
                else:
                    res.headers = {}
            elif ignore_headers:
                res.headers = {k: v for k, v in res.headers.items() if
                               k.upper() not in ignore_headers}

            case_info = dict(request=req, response=res, func_name=func_name)
            cases.append(case_info)
        return cases

    def render(self, records):
        cases = self.prepare(records)
        t = Template(_TEMPLATE)
        result = t.render(options=self.options, match_params=dict_to_param_style_code(self.match_options), cases=cases)
        return result


_TEMPLATE = """
from zerotest.request import Request
from zerotest.response import Response
from zerotest.response_matcher import ResponseMatcher


matcher = ResponseMatcher({{ match_params }})
verify_ssl = {{ options.verify_ssl or False }}
{% if options.endpoint %}
endpoint = {{ options.endpoint.__repr__() }}
{% endif %}
{% for c in cases %}
def test_{{ c.func_name }}():
    request = {{ c.request.__repr__() }}
    {% if options.endpoint %}
    request.endpoint = endpoint
    {% endif %}
    real = Response.from_requests_response(request.send_request(verify=verify_ssl))
    expect = {{ c.response.__repr__() }}
    matcher.match_responses(expect, real)

{% endfor %}
"""
