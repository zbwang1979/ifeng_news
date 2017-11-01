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
    # comment_url='http://comment.ifeng.com/post.php'
    my_cookies={item['name']:item['value'] for item in receive_cookie }
    my_s.cookies.update(my_cookies)
    # r = my_s.get('http://id.ifeng.com', timeout=10)
    # res_txt = r.text
    # print(res_txt)
    # return
    # ''''KJ123,FOCUSKJ123''''
    news_data=[
        {'news_data': 'KJ123,FOCUSKJ123',
         'key_word': ' ',
         'reply_txt': ['清除市场败类酷骑单车，清退用户押金，严惩不法分子，还公平正义给用户。',
                       '酷骑单车，市场败类']
         },
        {'news_data':'TY43,FOCUSTY43,TYTOPIC',
                'key_word':['中超','中甲','男足','国足','足球','足协','足坛','足联','足总','恒大','上港','权健','鲁能','国安',
              '富力','亚泰','开新','亿利','申花','辽足','亚冠','郝海东'],
                'reply_txt':['停止男足💩职业联赛，男足💩退出国际足联，解散男足国家队💩',
               '中国男足在世界杯出现的唯一办法：和南极洲🐧分在一组，主场定在海南，客场保平，主场争胜,最重要的要请海豹当裁判👮',
               '中国不适合职业足球，马上解散足协男足，多建几个免费灯光场让普通人玩玩就行了',
               '停办足球，支援边疆；停办足球，多建绿地；停办足球，学生减负；停办足球，社会将更和谐，大家会更开心',
               '足协请把你们定位在服务人员上，而不是管理者。创造条件让普通的热爱足球运动的人们能轻松的踢场球，让孩子们能轻松的踢场球，这是你们最该干的',
               '我现在年薪五六万，真不够用的，听说男足队员都是年薪千万，我现在申请跳槽，加入国足，理由如下： 一、我也能不赢球；二、 我也不能带球突破对方球员；三、对方球员带球也能很轻松的把我晃过；四、面对对方球门，我也射不进球；五、我也接不住队友传给我的球；六、我也不能把球准确地传给队友；七、在场上，我也会吃口香糖；八、在场上我也敢骂裁判；九、输了球，面对媒体我也会潸然泪下，过后又像没事人一样；十、我也爱美女网红女模特，泡吧泡到大天亮；十一、我也有纹身,绝对比贝克汉姆多；十二、我也对豪车如数家珍,有钱就买。十三、输球了我也会发微博，指责骂我们的球迷',
               '我现在年薪五六万，真不够用的，听说男足队员都是年薪千万，我现在申请跳槽，加入国足，理由如下： 一、我也能不赢球；二、 我也不能带球突破对方球员；三、对方球员带球也能很轻松的把我晃过；四、面对对方球门，我也射不进球；五、我也接不住队友传给我的球；六、我也不能把球准确地传给队友；七、在场上，我也会吃口香糖；八、在场上我也敢骂裁判；九、输了球，面对媒体我也会潸然泪下，过后又像没事人一样；十、我也爱美女网红女模特，泡吧泡到大天亮；十一、我也有纹身,绝对比贝克汉姆多；十二、我也对豪车如数家珍,有钱就买。十三、输球了我也会发微博，指责骂我们的球迷',
               ]},]
    my_s.headers.update({
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Host': 'comment.ifeng.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Accept-Language':'zh-CN,zh;q=0.8',
    })
    comment_ext2 = {'comment_level': '0',
                    'device_type': 'iphone249 plus 1',
                    'from': 'sh',
                    'isSync': '1',
                    'isTrends': '0',
                    'lat': '39.970585',
                    'location': '丹东鸭绿江',
                    'lon': '123.975259',
                    'nickname': 'xxxxx',
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
                    lead_emoji_list = ['👎', '💩', '👮']
                    while (True):
                        if len(lead_emoji_list) > 0:
                            my_data = {}
                            my_data['docName'] = item['title']
                            my_data['docUrl'] = item['commentsUrl']
                            tail_emoji=lead_emoji_list.pop(random.randrange(0,len(lead_emoji_list)))+''.join([re.sub(r":.*?:",'',
                                             emoji.emojize(':%s:'%random.choice(list(emoji_res))))for i in range(5)])
                            reply_message_index=random.randrange(0,len(news_item['reply_txt']))
                            my_data['content'] = news_item['reply_txt'][reply_message_index]+tail_emoji
                            comment_ext2['docId'] = item['commentsUrl']
                            my_data['ext2'] = str(comment_ext2)
                            try:
                                r = my_s.get(comment_url, params=my_data,timeout=10)
                                if bool(r):
                                    res_txt=r.json()
                                    print('news_%d发布于:%s标题:%s\n状态:%s提示:%s回复:%s' % (len(used_url_list),
                                    item['updateTime'], item['title'], res_txt['code'],res_txt['message'] if 'message' in res_txt.keys()else ' ',(str(reply_message_index)+tail_emoji)))
                                else:
                                    print('news_%d发布于:%s标题:%s\n状态:%s提示:%s回复:%s' % (len(used_url_list),item['updateTime'], item['title'], '失败',' ',(str(reply_message_index)+tail_emoji)))
                                    break
                            except Exception as e:
                                print(e)
                                return
                            time.sleep(10)
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
