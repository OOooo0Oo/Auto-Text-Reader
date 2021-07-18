import configparser
import os

import subprocess

from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from anaconda_navigator.utils.encoding import write
from playsound import playsound


def mktemp():
    path = '../../temp/temp.wav'
    folder = os.path.exists(path)

    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径


def writeToWav(filename, apiKey, apiArea):
    speech_key, service_region = apiKey, apiArea

    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat["Riff8Khz8BitMonoALaw"])
    audio_config = AudioOutputConfig(filename = filename)
    ssml_string = open("../TTS/ssml.xml", "r",encoding='UTF-8').read()
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config = None)
    result = synthesizer.speak_ssml_async(ssml_string).get()

    stream = AudioDataStream(result)
    stream.save_to_wav_file(filename)


def wav_to_amr(wave_path, arm_path, ffpeg_path):
    error = subprocess.call([ffpeg_path+"/ffmpeg.exe", '-i', wave_path, '-y', arm_path], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    if error:
        return
    #print ('amr success')

def getApi(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config["common"]["tts api key"], config["common"]["tts api area"]


def main():
    mktemp()
    wav_Path = '../../temp/temp.wav'
    arm_path = '../../temp/temp.amr'
    ffpeg_path = '../../../ffmpeg/bin'
    config_path = "../../config/config.ini"
    apiKey, apiArea = getApi(config_path)
    writeToWav(wav_Path, apiKey, apiArea)
    wav_to_amr(wav_Path, arm_path, ffpeg_path)

if __name__=='__main__':
   main()

'''
Abandoned Code
def playToMic():
    #mixer.init()
    #print([get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))])
    #mixer.quit()
    #streamWav(filePath)
    #mixer.pre_init(devicename='CABLE Input (VB-Audio Virtual Cable)')
    #playsound('../../temp/temp.wav')
    #os.system("../../temp/temp.wav")
    mixer.init(devicename = 'CABLE Input (VB-Audio Virtual Cable)') #Initialize it with the correct device
    mixer.music.load("../../temp/temp.wav") #Load the mp3
    mixer.music.play(0)

    while mixer.music.get_busy():
        pygame.time.Clock().tick(10)
        playsound('../../temp/temp.wav')
    mixer.quit()
    #sound.play(0)
    #mixer.init()
    
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
'''