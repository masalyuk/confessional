import time
import threading
import wave
import audioop

import pasimple

# CONSTANSTS
SAMPLE_RATE_HZ = 8000
CHANNEL = 1
SILENT_DURATION_SEC=3
OUT_SINK_NAME = 'baresip_sink.monitor' # to record what client say
INPUT_SINK_NAME = 'Music_Sink' # to send sound to client 
NOISE_THR = 500

    
class Sounder:
    def __init__(self, threshold=0.01, silence_duration=5, sample_rate=8000, channels=1):
        self.threshold = threshold
        self.silence_duration = silence_duration
        self.sample_rate = sample_rate
        self.channels = CHANNEL

        self.recording = True
        self.playing = True
        self.format = pasimple.PA_SAMPLE_S16LE
        self.bg_stop_trigger = None

    def stop_everything(self):
        self.stop_background_music()
        self.stop_recording()
        self.stop_playing()

    def stop_playing(self):
        self.playing = False
        self.stop_background_music 

    def stop_recording(self):
        self.recording = False
        self.playing = False

    def record(self, file_path, duration=SILENT_DURATION_SEC, noise_threshold=NOISE_THR, sink_name=OUT_SINK_NAME):
        #max_duration = 60 * 5 TODO

        with wave.open(file_path, 'wb') as wf:
            wf.setsampwidth(pasimple.format2width(self.format))
            wf.setnchannels(self.channels)
            wf.setframerate(self.sample_rate)

            sound_detected = False
    
            with pasimple.PaSimple(pasimple.PA_STREAM_RECORD, self.format, self.channels, self.sample_rate, device_name=sink_name) as pa:
                chunk_size = 1024
                self.recording = True
                silence_start_time = None
                while self.recording:
                    audio_data = pa.read(chunk_size)
                    wf.writeframes(audio_data)

                    if audioop.rms(audio_data, 2) < noise_threshold:
                        if sound_detected:
                            # Noise (or silence) detected
                            if silence_start_time is None:
                                silence_start_time = time.time()
                            elif time.time() - silence_start_time > duration:
                                # Silence duration exceeded, stop recording
                                self.recording = False
                    else:
                        sound_detected = True
                        silence_start_time = None
                    
                pa.close()

    def play_background_music(self, file):
        self.bg_stop_trigger = threading.Event()
        self.bg_sound = threading.Thread(target=self.play, args=(file, self.bg_stop_trigger))
        self.bg_sound.start()

    def stop_background_music(self):
        if self.bg_stop_trigger is not None:
            self.bg_stop_trigger.set()
            self.playing = False 
            self.bg_sound.join()

    def play(self, file, background_mode=None, sink_name=INPUT_SINK_NAME):
        self.playing = True

        with wave.open(file, 'rb') as wf:
            with pasimple.PaSimple(pasimple.PA_STREAM_PLAYBACK,
                                    pasimple.width2format(wf.getsampwidth()),
                                    wf.getnchannels(),
                                    wf.getframerate(),
                                    device_name=sink_name) as pa:
                
                chunk_size = 1024
                audio_chunk = wf.readframes(chunk_size)
                while len(audio_chunk) > 0:
                    pa.write(audio_chunk)
                    
                    # Check if we should stop playback
                    if background_mode is None:
                        if self.playing is False:
                            print("Stop playing")
                            break
                    else:
                        if background_mode.is_set() or self.playing is False:
                            print("Stopping background music")
                            break
                    
                    # Read the next chunk
                    audio_chunk = wf.readframes(chunk_size)
                pa.drain()
                pa.close()


