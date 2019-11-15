import requests
import threading

class downloader:
    def __init__(self,url,path_and_name,threadnum):
        self.url = url
        self.num = threadnum
        self.name = path_and_name
        r = requests.head(self.url)
        # 获取文件大小
        self.total = int(r.headers['Content-Length'])


    # 获取每个线程下载的区间
    def get_range(self):
        ranges = []
        offset = int(self.total/self.num)
        for i in range(self.num):
            if i == self.num-1:
                ranges.append((i*offset,''))
            else:
                ranges.append((i*offset,(i+1)*offset))
        return ranges  # [(0,100),(100,200),(200,"")]

    # 通过传入开始和结束位置来下载文件
    def download(self,start,end):
        headers = {'Range':'Bytes=%s-%s'%(start,end),'Accept-Encoding':'*'}
        res = requests.get(self.url,headers=headers)

        # 将文件指针移动到传入区间开始的位置
        self.fd.seek(start)
        self.fd.write(res.content)

    def run(self):
        self.fd = open(self.name,"wb")

        thread_list = []
        n = 0

        for ran in self.get_range():
            # 获取每个线程下载的数据块
            start,end = ran
            n += 1
            thread = threading.Thread(target=self.download,args=(start,end))
            thread.start()
            thread_list.append(thread)

        for i in thread_list:
            # 设置等待，避免上一个数据块还没写入，下一数据块对文件seek，会报错
            i.join()

        self.fd.close()

# if __name__ == "__main__":
#     url='http://jdvodrvfb210d.vod.126.net/mooc-video/nos/mp4/2017/08/01/1006648121_95bdf6576f1d41959cff6238395479f3_sd.mp4?ak=7909bff134372bffca53cdc2c17adc27a4c38c6336120510aea1ae1790819de8f367f13abf0e7b26e6615bf4adf3beb852857fe90aa09176fa2a2411e16a18493059f726dc7bb86b92adbc3d5b34b132adb519c85b055b7dbafb09012fdf9f28623591d5e74d0640a136e4a4f0e4eb71'
#     downloader(url,r'data\test.mp4',10).run()