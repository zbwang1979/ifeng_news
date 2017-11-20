# encoding: utf-8
import datetime
import pytz
import re
import threading
import random
import requests
import time
from web_ins import web_ins
import emoji
from apscheduler.schedulers.blocking import BlockingScheduler

def timestamp2day(timestramp):
    tz = pytz.timezone(pytz.country_timezones('cn')[0])
    format_local_time = datetime.datetime.fromtimestamp(timestramp, tz).strftime('%Y/%m/%d %H:%M:%S\t')
    return format_local_time

def get_news_list(news_para):
    log_string = 'Trying to get %s'%news_para
    print(log_string)
    my_s=requests.Session()
    my_s.headers.update({
        'Accept-Encoding': '',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Host': 'api.iclient.ifeng.com',
        'User-Agent': 'Dalvik/2.1.0(Linux;U;Android 5.1;iphone249 plus 1 Build/LMY47I)',
        'Accept-Language':'zh-CN,zh;q=0.8'
    })
    my_data={}
    my_data['id']=news_para
    my_data['action'] = ''
    my_data['pullNum']='1'
    my_data['lastDoc'] = ',,,'
    my_data['gv'] = '5.7'
    my_data['av'] = '5.7'
    my_data['screen'] = '720x1280'
    my_data['nw'] = 'wifi'
    my_data['province'] = '上海'
    my_data['city'] = '上海'
    my_data['proid'] = 'ifengnews'
    try:
        r=my_s.get('http://api.iclient.ifeng.com/ClientNews',params=my_data,timeout=10)
    except Exception as e:
        print(e)
    else:
        return r

def log_in(receive_cookie):
    log_string = 'Trying to login...ifeng news'
    print(log_string)
    my_s=requests.Session()
    my_s.headers.update({
        'Accept-Encoding': '',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Host': 'id.ifeng.com',
        'User-Agent': 'Dalvik/2.1.0(Linux;U;Android 5.1;iphone249 plus 1 Build/LMY47I)',
        'Accept-Language':'zh-CN,zh;q=0.8'
    })
    '''
    体育TY43 军事JS83
    '''
    comment_url='http://icomment.ifeng.com/wappost.php'
    my_cookies={item['name']:item['value'] for item in receive_cookie }
    my_s.cookies.update(my_cookies)

    # ''''KJ123,FOCUSKJ123 'SYLB10,SYDT10' TY43,FOCUSTY43,TYTOPIC''''
    news_data=[
        {'news_data': 'KJ123',
         'key_word': ' ',
         'reply_txt': ['xxxxxxxxxxxx',
                       'mmmmmmmmmmmmmmm']
         },
        {'news_data':'TY43',
                'key_word':['key1',],
                'reply_txt':['xxxxxxxxxxxx',
                             'xxxxxxxxxxxx',
                             'xxxxxxxxxxxx',
                             'xxxxxxxxxxxx',
                             'xxxxxxxxxxxx',
               ]},]
    my_s.headers.update({
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Host': 'comment.ifeng.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept-Language':'zh-CN,zh;q=0.8',
    })
    comment_ext2 = {'comment_level': '0',
                    'comment_verify':'',
                    'device_type': 'iphone249 plus 1',
                    'from': 'sh',
                    'isSync': '0',
                    'isTrends': '0',
                    'lat': '39.970585',
                    'location': '丹东鸭绿江',
                    'lon': '123.975259',
                    'nickname': '江边摸鱼人..',
                    'userimg': 'http://my.ifengimg.com/2017/08/02/8326ef78edbd78cf1501652140_1.jpg'
                    }
    try:
        emoji_res = requests.get('https://api.github.com/emojis').json()
    except:
        print('获取emoji失败')
        return
    for news_item in news_data:
        r=get_news_list(news_item['news_data'])
        res=r.json()
        try:
            find_item=res[0]['item']
        except:
            print('未获取到%s列表'%(news_item['news_data']))
            return
        for item in find_item:
            try:
                current_url=item['commentsUrl']
            except:
                print('此条无可用信息')
                continue
            if bool(re.match(r'sub_\d*?',current_url)) and \
                    bool(([word for word in news_item['key_word'] if word in item['title']]) or news_item['key_word']==''):
                global used_url_list
                global last_refresh_time
                if int(time.time()-last_refresh_time)>24*60*60:
                    used_url_list.clear()
                    last_refresh_time=int(time.time())
                    print('清空url_list')
                if not item['commentsUrl'] in used_url_list:
                    used_url_list.append(item['commentsUrl'])
                    lead_emoji_list = ['👎', '💩']
                    while (True):
                        if len(lead_emoji_list) > 0:
                            my_data = {}
                            my_data['docName'] = item['title']
                            my_data['quoteId']=''
                            my_data['docUrl'] = item['commentsUrl']
                            my_data['client'] = '1'
                            my_data['rt'] = 'sj'
                            my_data['skey'] = '05BF27'
                            tail_emoji=lead_emoji_list.pop(random.randrange(0,len(lead_emoji_list)))+''.join([re.sub(r":.*?:",'',
                                             emoji.emojize(':%s:'%random.choice(list(emoji_res))))for i in range(5)])
                            reply_message_index=random.randrange(0,len(news_item['reply_txt']))
                            my_data['content'] = news_item['reply_txt'][reply_message_index]+tail_emoji
                            comment_ext2['docId'] = item['commentsUrl']
                            comment_ext2['docUrl'] ='http://api.iclient.ifeng.com/api_vampire_article_detail?' \
                                                    'aid=%s&channelid=%s'%(item['commentsUrl'],news_item['news_data'])
                            comment_ext2['nickname'] = random.choice(['将来买了秘书', '将来买了主席', '将来买了看门大爷', '将来买了保洁阿姨', '将来买了吃瓜群众'])
                            my_data['ext2'] = str(comment_ext2)
                            try:
                                r = my_s.get(comment_url, params=my_data,timeout=10)
                                if bool(r):
                                    print('news_%d发布于:%s标题:%s\n状态:%s回复:%s' % (len(used_url_list),
                                    item['updateTime'], item['title'], r.text,(str(reply_message_index)+tail_emoji)))
                                else:
                                    print('news_%d发布于:%s标题:%s\n状态:%s提示:%s回复:%s' % (len(used_url_list),item['updateTime'], item['title'], r.text,' ',(str(reply_message_index)+tail_emoji)))
                                    break
                            except Exception as e:
                                print(e)
                                return
                            time.sleep(5)
                        else:
                            break
                else:
                    res_txt='已发过评论'
                    print(
                        'news_%d发布于:%s标题:%s\n状态:%s' % (len(used_url_list),
                                                          item['updateTime'], item['title'], res_txt))
                time.sleep(5)
        print('news_完成查找时间：%s'%timestamp2day(time.time()))

used_url_list=[]
last_refresh_time=int(time.time())
USER_NAME='xxx'
PASS_WORD='xxx'
my_web=web_ins(USER_NAME,PASS_WORD)
cookie=my_web.log_in()
log_in(cookie)
sched = BlockingScheduler(timezone='Asia/Shanghai')
def new_scheduled():
    @sched.scheduled_job('interval', id='ifeng_news',  minutes=15)
    def scheduled_ins_down():
        time.sleep(1)
        log_in(cookie)
    sched.start()
t = threading.Thread(target =new_scheduled)
t.start()
