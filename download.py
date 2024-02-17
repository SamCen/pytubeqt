from pytube import YouTube
import os


class YouTubeDownloader():


    def on_progress(self,stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        print(percentage_of_completion)

    def downloadAct(self,url,path):
        try:
            # 创建YouTube对象并获取视频流和标题
            youtube = YouTube(url)
            video_stream = youtube.streams.get_highest_resolution()
            title = youtube.title
            youtube.register_on_progress_callback(self.on_progress)
            # 获取当前工作目录并在其中保存视频
            downloadPath = os.path.abspath(path)
            video_stream.download(downloadPath)
            print(f"Fetching \"{video_stream.title}\"..")
            print(f"Fetching successful\n")
            print(f"Information: \n"
                f"File size: {round(video_stream.filesize * 0.000001, 2)} MegaBytes\n"
                f"Highest Resolution: {video_stream.resolution}\n"
                f"Author: {youtube.author}")
            print("Views: {:,}\n".format(youtube.views))

            # print(f"Downloading \"{video_stream.title}\"..")
            # print(f"视频 [{title}] 已成功下载到 {path} 目录下！")
            return 1
        except Exception as e:
            print(e)
            return 2



    #需要粘贴的代码   python  download.py