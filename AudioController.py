import sounddevice as sd
from Globals import SAMPLE_RATE
from Signal import Signal


class AudioController:
    @staticmethod
    def __record_sample__(input_signal, fs=SAMPLE_RATE):
        rec = sd.playrec(data=input_signal.y, samplerate=fs, channels=1)
        sd.wait()
        return rec

    @staticmethod
    def choose_default_device(recorder="LOGITECH PRO X", player="FOCUSRITE USB"):
        counter = 0
        r = -1
        p = -1
        devices = sd.query_devices()
        for device in devices:
            if device["name"].upper().find(recorder.upper()) > -1 and device["max_input_channels"] > 0 and r == -1:
                r = counter
            if device["name"].upper().find(player.upper()) > -1 and device["max_output_channels"] > 0 and p == -1:
                p = counter
            if r != -1 and p != -1:
                break
            counter += 1
        print("Used recorder: ", r)
        print(devices[r])
        print("Used player: ", p)
        print(devices[p])
        sd.default.device = (r, p)

    @staticmethod
    def record_signals(base_signals):
        recorded_signals = []
        for base_signal in base_signals:
            sample = AudioController.__record_sample__(base_signal)
            recorded_signal = Signal(y=sample, f=base_signal.f, d=base_signal.d)
            recorded_signals.append(recorded_signal)
        return recorded_signals

    @staticmethod
    def play_wave(input_wave, fs=SAMPLE_RATE):
        sd.play(data=input_wave, samplerate=fs)
        sd.wait()

    @staticmethod
    def get_audio_devices():
        return sd.query_devices()