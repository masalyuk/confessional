import sounder
import subprocess
from phone_book import PhoneBook
from person_phone import PersonPhone

# Create a new phone book instance
phone_book = PhoneBook()


def init_phone_book():
    phone_book.add_entry("07", "Catholic priest ", "Catholic priest", "echo")
    phone_book.add_entry("0108", "Bhikkhunī ", "Buddhist monk", "nova")
    phone_book.add_entry("0666", "Satan ", "Satan", "onyx")
    phone_book.add_entry("03", "Wiccan witch ", "Witch who practices tarot reading and astrology.", "alloy")
    phone_book.add_entry("062", "Sigmund Freud", "Sigmund Freud", "fable")

def init_persons():
    for entry in phone_book.entries:
        phone1 = PersonPhone(phone_book.get_entry_by_number(entry['number']))

def init_sound():
    subprocess.run(['./scripts/setup_audio.sh'])

def main():
    init_sound()
    init_phone_book()
    init_persons()
    

if __name__ == "__main__":
    main()