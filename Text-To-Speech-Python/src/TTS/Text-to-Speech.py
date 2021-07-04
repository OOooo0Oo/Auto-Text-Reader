import pyaudio
import wave
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
speech_key, service_region = "6a6d33d49c9947558a3c424286c2550d", "westus"

speech_config = SpeechConfig(subscription=speech_key, region=service_region)
audio_config = AudioOutputConfig(use_default_speaker=True)
ssml_string = open("ssml.xml", "r",encoding='UTF-8').read()


synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config = audio_config)
#print("Type some text that you want to speak...")
#text = input()
synthesizer.speak_ssml_async(ssml_string)

#audio_config = AudioOutputConfig(filename="path/to/write/file.wav")
