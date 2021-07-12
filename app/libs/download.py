import requests

class HTTP:
    @staticmethod
    def get(url, return_json=True):
        headers = {'apikey': 'OWHagO3Wmkt0FLaZJTtgHxCzGDxHt0Uu'}
        response = requests.request("GET", url, headers=headers)
        print('response', response.status_code)
        if response.status_code == 201:
            # print("response", response.json())
            return response.json() if return_json else response.text   
        return {} if return_json else ''
        # if response.status_code == '200':
        #     if return_json:
        #         return response.json()
        #     else:
        #         return response.text()
        # else:
        #     if return_json:
        #         return {}
        #     else:
        #         return ''
