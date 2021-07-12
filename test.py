from pygame._sdl2 import get_num_audio_devices, get_audio_device_name #Get playback device names
from pygame import mixer #Playing sound
import pygame

from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
speech_key, service_region = "6a6d33d49c9947558a3c424286c2550d", "westus"

from playsound import playsound


def cn_speak():
    speech_config = SpeechConfig(subscription=speech_key, region=service_region,)
    speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"
    audio_config = AudioOutputConfig(filename="file.wav")
    text = "我是你爹我是你爹我是你爹我是你爹"
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text)


def main():
    cn_speak()
    mixer.init()
    print([get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))]) # Returns playback devices
    # ['Headphones (Oculus Virtual Audio Device)', 'MONITOR (2- NVIDIA High Definition Audio)', 'Speakers (High Definition Audio Device)', 'Speakers (NVIDIA RTX Voice)', 'CABLE Input (VB-Audio Virtual Cable)']
    mixer.quit()# Quit the mixer as it's initialized on your main playback device

    mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)') #Initialize it with the correct device
    # mixer.init(devicename="耳机 (Realtek(R) Audio)")
    mixer.music.load("file.wav")  # Load the mp3
    mixer.music.play(0)
    while pygame.mixer.music.get_busy():
        playsound("file.wav")
        pygame.time.Clock().tick(10)


if __name__ == "__main__":
    main()
