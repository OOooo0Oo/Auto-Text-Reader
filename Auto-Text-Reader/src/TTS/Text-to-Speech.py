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


def writeToWav(filename):
    speech_key, service_region = "6a6d33d49c9947558a3c424286c2550d", "westus"

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


def main():
    mktemp()
    wav_Path = '../../temp/temp.wav'
    arm_path = '../../temp/temp.amr'
    ffpeg_path = '../../../ffmpeg/bin'
    writeToWav(wav_Path)
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