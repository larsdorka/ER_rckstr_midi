import requests


class SwitchRequestor:
    """"""

    def __init__(self, debug_log=dict()):
        """"""
        self.debug_log = debug_log
        self.debug_log['requestor_data'] = ""
        self.debug_log['requestor_response'] = ""
        self.debug_log['requestor_error'] = ""
        self.url = ""
        self.password = ""
        self.session = requests.session()
        self.switch_states = [False] * 4
        self.switch_states_new = [False] * 4

    def open(self, url, password):
        """"""
        self.url = url
        self.password = password

    def login(self):
        """"""
        response = self.session.post(self.url + "/login.html", data={'pw': self.password})

    def logout(self):
        """"""
        response = self.session.get(self.url + "/login.html")

    def switch_off(self, outlet, prepare=False):
        """"""
        if 1 <= outlet <= 4:
            self.switch_states_new[outlet - 1] = False
            if not prepare:
                self.send_switches()

    def switch_on(self, outlet, prepare=False):
        """"""
        if 1 <= outlet <= 4:
            self.switch_states_new[outlet - 1] = True
            if not prepare:
                self.send_switches()

    def switch_toggle(self, outlet, prepare=False):
        """"""
        if 1 <= outlet <= 4:
            self.switch_states_new[outlet - 1] = not self.switch_states_new[outlet]
            if not prepare:
                self.send_switches()

    def send_switches(self):
        """"""
        data = dict()
        for index in range(4):
            if self.switch_states_new[index] != self.switch_states[index]:
                if self.switch_states_new[index]:
                    data['cte' + str(index + 1)] = "1"
                else:
                    data['cte' + str(index + 1)] = "0"
                self.switch_states[index] = self.switch_states_new[index]
            else:
                data['cte' + str(index + 1)] = ""
        self.debug_log['requestor_data'] = str(data)

        try:
            response = self.session.post(self.url, data=data)
            self.debug_log['requestor_response'] = str(response)
            self.debug_log['requestor_error'] = ""
        except Exception as ex:
            self.debug_log['requestor_error'] = str(ex)
