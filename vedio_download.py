import yt_dlp


# 网页端安装Cookie-Editor获取B站的cookies
def load_cookies_from_file(file_path):
    """从 Netscape 格式的 Cookies 文件加载"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines and lines[0].startswith("# Netscape HTTP Cookie File"):
                print("成功加载 Netscape 格式的 Cookies 文件！")
                return file_path
            else:
                print("Cookies 文件格式错误，确认是 Netscape 格式。")
                return None
    except FileNotFoundError:
        print("Cookies 文件未找到，请确认路径是否正确。")
        return None


def list_formats(url, cookies_file=None):
    """列出可用的格式选项"""
    ydl_opts = {
        'listformats': True,
        'quiet': False,
    }
    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"列出格式失败: {e}")


def download_video_and_audio(url, video_format_code, audio_format_code, cookies_file=None):
    """同时下载视频和音频并自动合并"""
    ydl_opts = {
        'format': f'{video_format_code}+{audio_format_code}',  # 使用视频和音频格式合并
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'  # 最终合并输出为 mp4 格式
            }
        ]
    }
    if cookies_file:
        ydl_opts['cookiefile'] = cookies_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"下载失败: {e}")


def main():
    video_url = input("请输入Bilibili视频地址：").strip()
    print("\n请选择Cookies选项：")
    print("1. 从Cookies文件加载")
    print("2. 不使用Cookies")
    choice = input("请输入选项（1/2，默认2）：").strip() or "2"
    cookies_file = None
    if choice == "1":
        file_path = input("请输入Cookies文件路径：").strip()
        cookies_file = load_cookies_from_file(file_path)
        if not cookies_file:
            print("加载 Cookies 文件失败，程序退出。")
            return
    elif choice == "2":
        print("未使用任何 Cookies。")
    else:
        print("无效的选项，程序退出。")
    print("\n正在列出可用格式，请稍候...")
    list_formats(video_url, cookies_file)

    video_format_code = input("请输入你想要下载的视频格式代码：").strip()
    audio_format_code = input("请输入你想要下载的音频格式代码：").strip()

    print("\n开始下载并合并，请稍候...")
    download_video_and_audio(video_url, video_format_code, audio_format_code, cookies_file)
    print("下载完成！")


if __name__ == "__main__":
    main()
