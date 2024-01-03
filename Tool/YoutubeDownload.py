from pytube import YouTube
from pytube import exceptions
from pydub import AudioSegment
import time
import random
import os

class YoutubeDownload:
    """輸入來網址下載youtube的影片，下載資料夾的初始位置在youtubefile/audio"""
    def __init__(self, url: str, save_path=None):
        self.__yt = YouTube(url)
        if save_path == None:
            self.__save_path = "./youtubefile/audio"
        else:
            self.__save_path = save_path

        transtring = str.maketrans({" " : "_", "." : "", "/" : ""})
        self.__filename = self.__yt.title.translate(transtring)
        print(self.__filename)

    def audiodownloader(self):
        """only audio"""
        try:
            if os.path.exists("%s/%s.mp3" % (self.__save_path, self.__filename)) or \
                os.path.exists("%s/%s.wav" % (self.__save_path, self.__filename)):
                print("下載過了。")
                return
            audio = self.__yt.streams.filter(only_audio=True).first()
            audio.download(self.__save_path, self.__filename)
            print("%s 下載完成"%(self.__filename))
        except exceptions.VideoUnavailable as ev:
            print("套件失效 原因:", ev)

    def videodownloader(self):
        """Bad picture quality"""
        try:
            if os.path.exists("%s/%s.mp4" % (self.__save_path, self.__filename)):
                print("下載過了。")
                return
            video = self.__yt.streams.get_by_resolution("720p")
            video.download(self.__save_path, self.__filename + ".mp4")
            print("%s 下載完成"%(self.__filename))
        except exceptions.VideoUnavailable as ev:
            print("套件失效 原因:", ev)
        
    def audiotomp3(self):
        if os.path.exists("%s/%s.mp3" % (self.__save_path, self.__filename)):
            return
        audio_file = AudioSegment.from_file("%s/%s" % (self.__save_path, self.__filename))
        mp3_file_path = "%s/%s.mp3" % (self.__save_path, self.__filename)
        audio_file.export(mp3_file_path, format="mp3")
        print("%s 完成轉換" % (self.__filename))
        os.remove(os.path.join(self.__save_path, self.__filename))

    def audiotowav(self):
        if os.path.exists("%s/%s.wav" % (self.__save_path, self.__filename)):
            return
        audio_file = AudioSegment.from_file("%s/%s" % (self.__save_path, self.__filename))
        wav_file_path = "%s/%s.wav" % (self.__save_path, self.__filename)
        audio_file.export(wav_file_path, format="wav")
        print("%s 完成轉換" % (self.__filename))
        os.remove(os.path.join(self.__save_path, self.__filename))

def main():
    urls = []
    random_time = [3.5, 7.1, 2.3, 4.2, 3.9, 6.4]
    #mp4類型還沒找到高畫質的下載方法，不提示
    while True:
        mode = str(input("請輸入要儲存的檔案類型(支援mp3, wav): ").lower())
        if mode not in ["mp3", "wav", "mp4"]:
            print("請輸入支援的檔案類型")
            continue
        break

    print("請輸入youtube網址再輸入start開始，如果要結束請輸入quit")
    while True:
        html = str(input(">>>"))
        if html.lower() == "quit" or html.lower() == "q":
            urls.append(html)
            break
        if html.lower() == "start":
            break
        if not html.startswith("https://www.youtube.com/"):
            print("這不是油土伯!")
            continue
        urls.append(html)
    
    if mode.lower() == "wav":
        try:
            for i, url in enumerate(urls, 1):
                try:
                    print("第%d個 開始下載"%(i))
                    
                    if any(keyword.lower() in map(str.lower, urls) for keyword in ["quit", "q"]):
                        break

                    yt = YoutubeDownload(url)
                    yt.audiodownloader()
                    yt.audiotowav()
                    time.sleep(random.choice(random_time))
                    print("第%d個 完成"%(i))

                except Exception as e:
                    print("發生例外:", e)
            
        finally:
            print("程序已結束!")

    elif mode.lower() == "mp3":
        try:
            for i, url in enumerate(urls, 1):
                try:
                    print("第%d個 開始下載"%(i))
                    
                    if any(keyword.lower() in map(str.lower, urls) for keyword in ["quit", "q"]):
                        break

                    yt = YoutubeDownload(url, "./youtubefile/mp3")
                    yt.downloader()
                    yt.audiotomp3()
                    time.sleep(random.choice(random_time))
                    print("第%d個 完成"%(i))

                except Exception as e:
                    print("發生例外:", e)
            
        finally:
            print("程序已結束!")

    elif mode.lower() == "mp4":
        try:
            for i, url in enumerate(urls, 1):
                try:
                    print("第%d個 開始下載"%(i))
                    
                    if any(keyword.lower() in map(str.lower, urls) for keyword in ["quit", "q"]):
                        break

                    yt = YoutubeDownload(url)
                    yt.videodownloader()
                    #yt.videotomp4()
                    time.sleep(random.choice(random_time))
                    print("第%d個 完成"%(i))

                except Exception as e:
                    print("發生例外:", e)
            
        finally:
            print("程序已結束!")

#考慮加入youtube list來下載
    

if __name__ == "__main__":
    main()
