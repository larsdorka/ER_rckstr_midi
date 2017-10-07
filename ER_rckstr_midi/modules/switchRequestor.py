import requests


class SwitchRequestor:
    """"""

    def __init__(self, debug_log=dict()):
        """"""
        self.debug_log = debug_log
        self.debug_log['requestor_data'] = ""
        self.debug_log['requestor_request'] = ""
        self.debug_log['requestor_response'] = ""
        self.debug_log['requestor_error'] = ""
        self.url = ""
        self.password = ""
        self.session = requests.session()
        self.switch_states = [False] * 4
        self.switch_states_new = [False] * 4
        self.prepared = False

    def open(self, url, password):
        """"""
        self.url = url
        self.password = password

    def login(self):
        """"""
        try:
            response = self.session.post(self.url + "/login.html", data={'pw': self.password})
            self.debug_log['requestor_request'] = "login"
            self.debug_log['requestor_response'] = str(response)
            self.debug_log['requestor_error'] = ""
        except Exception as ex:
            self.debug_log['requestor_error'] = str(ex)

    def logout(self):
        """"""
        try:
            response = self.session.get(self.url + "/login.html")
            self.debug_log['requestor_request'] = "logout"
            self.debug_log['requestor_response'] = str(response)
            self.debug_log['requestor_error'] = ""
        except Exception as ex:
            self.debug_log['requestor_error'] = str(ex)

    def switch_off(self, outlet, prepare=False):
        """"""
        if 1 <= outlet <= 4:
            self.switch_states_new[outlet - 1] = False
            if not prepare:
                self.send_switches()
            else:
                self.prepared = True

    def switch_on(self, outlet, prepare=False):
        """"""
        if 1 <= outlet <= 4:
            self.switch_states_new[outlet - 1] = True
            if not prepare:
                self.send_switches()
            else:
                self.prepared = True

    def switch_toggle(self, outlet, prepare=False):
        """"""
        if 1 <= outlet <= 4:
            self.switch_states_new[outlet - 1] = not self.switch_states_new[outlet]
            if not prepare:
                self.send_switches()
            else:
                self.prepared = True

    def send_switches(self):
        """"""
        data = dict()
        changes_detected = False
        for index in range(4):
            if self.switch_states_new[index] != self.switch_states[index]:
                changes_detected = True
                if self.switch_states_new[index]:
                    data['cte' + str(index + 1)] = "1"
                else:
                    data['cte' + str(index + 1)] = "0"
                self.switch_states[index] = self.switch_states_new[index]
            else:
                data['cte' + str(index + 1)] = ""
        if changes_detected:
            self.prepared = False
            self.debug_log['requestor_data'] = str(data)
            try:
                response = self.session.post(self.url, data=data)
                self.debug_log['requestor_request'] = "send switches"
                self.debug_log['requestor_response'] = str(response)
                self.debug_log['requestor_error'] = ""
            except Exception as ex:
                self.debug_log['requestor_error'] = str(ex)
        else:
            # self.debug_log['requestor_data'] = 'no changes detected'
            pass
