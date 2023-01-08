import requests
import re

class downloader():
    _download_header = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "accept-encoding": "gzip, deflate, br",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Connection": "keep-alive",
        "Cookie": "tstc=p",
    }
    
    def __init__(self,cookies:str) -> None:
        self._cookies = cookies
    
    def download_video(self,baseurl:str,quality:str,filename:str):
        header_get_download_link = {
            "referer":baseurl,
            "X-Requested-With": "XMLHttpRequest",
            "content-type": "application/x-www-form-urlencoded",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "accept-encoding": "gzip, deflate, br",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Cookie": self._cookies
        }
        
        id_hash = self._get_hash_id_with_url(baseurl)
        
        preIdPar = id_hash[0].split("_")[0]
        postData = {
            "act": "show",
            "al": "1",
            "al_ad": "0",
            "autoplay": "1",
            "force_no_repeat": "1",
            "list": id_hash[1],
            "module": "profile_own_videos",
            "playlist_id": preIdPar + "_1",
            "show_next": "1",   
            "video": id_hash[0]
        }
        
        response = requests.post(url="https://vk.com/al_video.php?act=show",data=postData,headers=header_get_download_link)
        j = response.json()
        video = j["payload"][1][4]["player"]["params"][0]
        if quality == "240":
            self._download_video(video["url240"],filename)
        if quality == "360":
            self._download_video(video["url360"],filename)
        if quality == "480":
            self._download_video(video["url480"],filename)
        if quality == "720":
            self._download_video(video["url720"],filename)
        if quality == "1080":
            self._download_video(video["url1080"],filename)

    @staticmethod
    def _download_video(url:str, filename:str)->None:
        try:
            response = requests.get(url=url,stream=True, headers=downloader._download_header)
            with open(filename, 'wb') as file:
                i = 0
                for chunk in response.iter_content(chunk_size=1024*1024):
                    if chunk:
                        i+=1
                        print("downloading "+ str(i) +" chunk")
                        file.write(chunk)
        except Exception as e:
            print(e)

    @staticmethod
    def _get_hash_id_with_url(url:str) -> tuple[str,str]:
        id = re.findall(r'video([0-9-]+_[0-9-]+)',url)[0]
        
        res = re.findall(r'%2F([0-9a-zA-Z-]+)',url)
        if len(res) < 1 :
            return (id, "")
        
        hash = res[0]
        
        return(id, hash)
