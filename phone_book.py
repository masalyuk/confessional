import json

class PhoneBook:
    VALID_VOICES = ["echo", "onyx", "alloy", "fable", "nova"]

    def __init__(self, json_file=None):
        self.entries = []
        if json_file:
            self.load_from_json(json_file)

    def add_entry(self, number, name, prompt_who_you_are,voice):
        """
        Add a new entry to the phone book. Now includes 'voice'.
        """
        if voice not in PhoneBook.VALID_VOICES:
            raise ValueError(f"Invalid voice: {voice}. Valid options are: {', '.join(PhoneBook.VALID_VOICES)}")
        
        entry = {
            "number": number,
            "name": name,
            "prompt_who_you_are": prompt_who_you_are,
            "voice": voice 
        }
        self.entries.append(entry)

    def get_entry_by_number(self, number):
        for entry in self.entries:
            if entry['number'] == number:
                return entry
        return None

    def write_to_json(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.entries, file, indent=4)

    def load_from_json(self, file_name):
        with open(file_name, 'r') as file:
            self.entries = json.load(file)
