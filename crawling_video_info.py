import requests, json, time

mid = '390461123'

cid_url = 'https://api.bilibili.com/x/player/pagelist?aid={0}&jsonp=jsonp'
video_info_url = 'https://api.bilibili.com/x/web-interface/view?aid={0}&cid={1}'
video_list_url = 'https://api.bilibili.com/x/space/arc/search?mid={0}&ps=100&tid=0&pn={1}&keyword=&order=pubdate&jsonp=jsonp'

CLASS_VIDEO = {76:'生活',12:'科技'}

tlite = ['author', 'create_time', 'title', 'description', 'video_length', 'video_type', 'video_review', 'is_pay', 'view', 'coin', 'share', 'like', 'favorite']

def get_request(url):
    while True:
        try:
            data = requests.get(url)
            break
        except Exception as e:
            print(e)
            time.sleep(3)
    return data

def get_cid(aid):

    url = cid_url.format(aid)
    data = get_request(url)
    data = json.loads(data.text)
    cid = data['data'][0]['cid']
    return cid



def write_data(data):
    try:
        write_str = ','.join(data) + '\n'
        with open('./data.csv', 'a+', encoding='utf-8') as f:
            f.write(write_str)
    except Exception as e:
        raise e

def processce_info(vlist):
    try:
        for v in vlist:
            info = []
            aid = v['aid']
            cid = get_cid(aid)
            time.sleep(3)
            url = video_info_url.format(aid, cid)
            video_info = get_request(url)
            video_info = json.loads(video_info.text)
            k = video_info['data']['stat']
            timeArray = time.localtime(v['created'])
            create_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray )
            info.append(v['author'])
            info.append(create_time)
            info.append(v['title'].replace('\n', ''))
            info.append(v['description'].replace('\n', ''))
            info.append(v['length'])
            info.append(v['typeid'])
            info.append(v['video_review'])
            info.append(v['is_pay'])
            info.append(k['view'])
            info.append(k['coin'])
            info.append(k['share'])
            info.append(k['like'])
            info.append(k['favorite'])
            info = [str(i) for i in info]
            write_data(info)
    except Exception as e:
        raise e

def get_video_list():
    try:
        url = video_list_url.format(mid, 1)
        print(url)
        video_list_info = requests.get(url)
        video_list_info = json.loads(video_list_info.text)
        data = video_list_info.get('data')
        count = data['page']['count']
        number = int(count / 100) + 1
        for i in range(number+1):
            url = video_list_url.format(mid, i+1)
            video_list_info = get_request(url)
            video_list_info = json.loads(video_list_info.text)
            vlist = video_list_info['data']['list']['vlist']
            print('write data : ', i)
            if not vlist:
                continue
            processce_info(vlist)
        print('end............')
    except Exception as e:
        raise e

if __name__ == "__main__":
    write_data(tlite)
    get_video_list()
