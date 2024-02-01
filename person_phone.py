import json

from baresipy import BareSIP

from person import Person, SETTINGS

class PersonPhone(BareSIP):
    def __init__(self, entry, full_promt=None):
        with open(SETTINGS, 'r') as settings:
            self.gateway = json.load(settings).get("gateway")

        self.entry = entry    
        self.person = Person(self.entry, full_promt)
        super().__init__(entry['number'], entry['number'], self.gateway, config_path="./baresip_config")
    
    def handle_incoming_call(self, number):
        print("Accept incomming call")
        self.accept_call()

    def handle_call_established(self):
        try:
            self.person.async_accept_call()
        except Exception as e:
             print(f"An unexpected error occurred: {e}")
             self.person.stop_everything()
             self.hang()
    
    def handle_call_ended(self, reason):
        print(f"Call ended {reason}")
        self.person.stop_everything()
