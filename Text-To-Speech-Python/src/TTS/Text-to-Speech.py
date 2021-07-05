import os
import pyaudio
import wave

from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from anaconda_navigator.utils.encoding import write

filePath = '../../temp/temp.wav'

def mktemp():
    path = '../../temp/temp.wav'
    folder = os.path.exists(path)
 
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径


def writeToWav(filename):
    speech_key, service_region = "6a6d33d49c9947558a3c424286c2550d", "westus"
    
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = AudioOutputConfig(filename = filename)
    ssml_string = open("ssml.xml", "r",encoding='UTF-8').read()
    
    
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config = audio_config)
    #print("Type some text that you want to speak...")
    #text = input()
    synthesizer.speak_ssml_async(ssml_string)
    
#if __name__=='__main__':
#    main()
    #audio_config = AudioOutputConfig(filename="path/to/write/file.wav")
    
def streamWav(filename):
    chunk = 1024
    file = wave.open(filename, 'rb')

    play = pyaudio.PyAudio()

    stream = play.open(format = play.get_format_from_width(file.getsampwidth()),
                    channels = file.getnchannels(),
                    rate = file.getframerate(),
                    output = True)
    
    # 写声音输出流进行播放
    while True:
        data = file.readframes(chunk)
        if data == "": break
        stream.write(data)
    
    #stream.wri
    stream.close()
    play.terminate()
    
    
mktemp()
writeToWav(filePath)
streamWav(filePath)
