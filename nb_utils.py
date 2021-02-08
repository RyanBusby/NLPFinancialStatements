
from ratelimit import limits, sleep_and_retry

class AlphaVantageAPI(object):
    @staticmethod
    @sleep_and_retry
    @limits(calls=5, period=60)
    def _call_api(url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('API response: {}'.format(response.status_code))
        return response

    def get(self, url):
        return self._call_api(url).json()

def print_ten_k_data(ten_k_data, fields, field_length_limit=50):
    indentation = '  '
    print('[')
    for ten_k in ten_k_data:
        print_statement = '{}{{'.format(indentation)
        for field in fields:
            value = str(ten_k[field])

            # Show return lines in output
            if isinstance(value, str):
                value_str = '\'{}\''.format(value.replace('\n', '\\n'))
            else:
                value_str = str(value)

            # Cut off the string if it gets too long
            if len(value_str) > field_length_limit:
                value_str = value_str[:field_length_limit] + '...'

            print_statement += '\n{}{}: {}'.format(indentation * 2, field, value_str)

        print_statement += '},'
        print(print_statement)
    print(']')
