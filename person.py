from time import sleep
import threading
import queue
import json

from openai import OpenAI
from pathlib import Path

from sounder import Sounder

SETTINGS = "settings.json"

SOUND_DIR = "sound"
COMMON_SOUND_DIR = "common"
CALL_SOUND_DIR = "call"

WAIT_WAV = "wait.wav"
HI_WAV = "hi.wav"
RECORDING_WAV = "recording.wav"
ANSWER_MP3 = "answer.mp3"
ANSWER_WAV = "answer.wav"

def check_call_running(func):
    """Decorator to check if call is running before executing a function."""

    def wrapper(self, *args, **kwargs):
        if self.call_running is False:
            print(f"Skipping {func.__name__} as call is not running.")
            return
        return func(self, *args, **kwargs)

    return wrapper

class Person():
# Init/Deinit
    def __init__(self, entry, full_promt=None):
        with open(SETTINGS, 'r') as settings:
            api_key_file = json.load(settings).get("api_key_file")
            with open(api_key_file, 'r') as file:
                self.api_key = file.read()
                self.client = OpenAI(api_key=self.api_key)

        self.entry = entry

        self.assystant_promt = self.make_assistant_promt()

        self.conversation = []

        self.sounder = Sounder()
        main_sound_dir = Path(SOUND_DIR)
        self.wait_music_file = str(main_sound_dir / COMMON_SOUND_DIR / entry['number'] / WAIT_WAV)
        self.answer_mp3_file = str(main_sound_dir / CALL_SOUND_DIR / ANSWER_MP3)
        self.answer_wav_file = str(main_sound_dir / CALL_SOUND_DIR / ANSWER_WAV)
        self.record_file     = str(main_sound_dir / CALL_SOUND_DIR / RECORDING_WAV)
        self.hi_file         = str(main_sound_dir / COMMON_SOUND_DIR / entry['number'] /HI_WAV)
        self.answer = None
    
        # To make possible interchange SIP messages
        self.call_running = False
        self.commands = queue.Queue()
        self.results = queue.Queue()
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop_everything(self):
        self.sounder.stop_everything()
        self.call_running = False
        self.clear_conversation()

    def make_assistant_promt(self):
        return f'''In a dialogue where you're portraying {self.entry['prompt_who_you_are']}, respond in character to the replica in the same language as replica. Your response should be profound yet concise, capturing the essence of your perspective in no more than 40 words'''

    def clear_conversation(self):
        self.conversation.clear()

#  Thread specific command
    def run(self):
        while True:
            command, args, kwargs = self.commands.get()
            if command is None:
                break  # Exit loop if None is received
            result = getattr(self, command)(*args, **kwargs)

    def perform_task(self, command, *args, **kwargs):
        self.commands.put((command, args, kwargs))

    def async_accept_call(self):
        self.perform_task("accept_call")

# AUDIO part
    def say_hi(self):
        self.sounder.play(self.hi_file)

    @check_call_running
    def record_request(self):
        self.sounder.record(self.record_file)

    @check_call_running
    def play_waiting_music(self):
        self.sounder.play_background_music(self.wait_music_file)

    def stop_wating_music(self):
        print(self.sounder)
        self.sounder.stop_background_music()

    @check_call_running
    def say_responce(self):
        self.sounder.play(self.answer_wav_file)

# OpenAI part
    @check_call_running
    def transcript_call(self, call_record_file):

        call = open(call_record_file, "rb")
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1", 
            file=call,
            response_format="text"
        )

        print("Transcription of call:")
        print(transcript)

        self.transcription = transcript
        return transcript

    @check_call_running
    def sound_answer(self, answer):
        speech_file_path = Path(__file__).parent / self.answer_mp3_file
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=self.entry['voice'],
            input=answer
        )
        response.stream_to_file(speech_file_path)

        from baresipy import BareSIP
        BareSIP.convert_audio(self.answer_mp3_file, self.answer_wav_file)

    @check_call_running
    def ask_advice(self, text):
        self.conversation.append({"role": "user", "content": text})

        completion  = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.conversation
        )

        self.answer = completion.choices[0].message.content

        print("Advice: ")
        print(self.answer)
        self.conversation.append({"role": "assistant", "content": self.answer})  
          
        return self.answer
    
    def accept_call(self):
        self.stop_everything()
        self.call_running = True

        self.say_hi()        
        self.conversation.append({"role": "system", "content": self.assystant_promt})

        while self.call_running:
            self.record_request()
            self.play_waiting_music()
            self.confess()
            self.stop_wating_music()
            self.say_responce()
        
        self.stop_everything()

    @check_call_running
    def confess(self):
        self.transcript_call(self.record_file)
        self.ask_advice(self.transcription)
        self.sound_answer(self.answer)
