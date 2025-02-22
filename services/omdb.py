import os
import time


class Counter:
    def __init__(self):
        self.filename = os.environ.get('LOG_FILE', 'log-omdb.txt')

    def request(self, flow):
        flow.request.query["apikey"] = "TOKEN_HERE"
        with open(self.filename, "a") as f:
            f.write("========REQUEST========\n")
            f.write(flow.request.method + "\n")
            f.write(flow.request.pretty_url + "\n")
            f.write(flow.request.text + "\n")

    def response(self, flow):
        with open(self.filename, "a") as f:
            f.write("========RESPONSE========\n")
            f.write(str(time.time()) + "\n")
            f.write(str(flow.response.status_code) + "\n")
            f.write(flow.response.text + "\n")


addons = [Counter()]
