# encoding=utf-8
import json
import base64
import requests

"""
输入你的微博账号和密码，可去淘宝买，一元七个。
建议买几十个，微博限制的严，太频繁了会出现302转移。
或者你也可以把时间间隔调大点。
"""
myWeiBo = [

    # {'no':'17181344363',  'psw':'ys654321'},
    # {'no':'13046080018',  'psw':'ys654321'},
    # {'no':'15664629386',  'psw':'ys654321'},
    # {'no':'15619036354',  'psw':'ys654321'},
    # {'no':'18349302814',  'psw':'ys654321'},
    # {'no':'13609739042',  'psw':'ys654321'},
    # {'no':'18380443985',  'psw':'ys654321'},
    # {'no':'18374735790',  'psw':'ys654321'},
    # {'no':'18663861428',  'psw':'ys654321'},
    # {'no':'18663893147',  'psw':'ys654321'},
    # {'no':'18663873410',  'psw':'ys654321'},
    # {'no':'17010259288',  'psw':'ys654321'},
    # {'no':'18663839465',  'psw':'ys654321'},
    # {'no':'17181347699',  'psw':'ys654321'},
    # {'no':'18349370574',  'psw':'ys987654'},
    # {'no':'18349394909',  'psw':'ys987654'},
    # {'no':'17076741243',  'psw':'ys987654'},
    # {'no':'17076743673',  'psw':'ys987654'},
    # {'no':'18349382099',  'psw':'ys987654'},
    # {'no':'15200534375',  'psw':'ys987654'},
    # {'no':'15096071324',  'psw':'ys987654'},
    # {'no':'18349303217',  'psw':'ys987654'},
    # {'no':'17181340377',  'psw':'ys987654'},
    # {'no':'17181342705',  'psw':'ys987654'},

    # {'no':'17010255880',  'psw':'ys987654'},
    # {'no':'17010259031',  'psw':'ys987654'},
    # {'no':'17096653489',  'psw':'ys987654'},
    # {'no':'17096653238',  'psw':'ys987654'},
    # {'no':'17010255865',  'psw':'ys987654'},
    # {'no':'17181347075',  'psw':'ys987654'},
    # {'no':'17181344387',  'psw':'ys987654'},
    # {'no':'14740573041',  'psw':'ys987654'},
    # {'no':'17181340257',  'psw':'ys987654'},
    # {'no':'17181343342',  'psw':'ys987654'},
    # {'no':'18349301802',  'psw':'ys987654'},
    # {'no':'17096642399',  'psw':'ys987654'},
    # {'no':'17181347301',  'psw':'ys987654'},
    # {'no':'13728092785',  'psw':'ys987654'},
    # {'no':'17181343895',  'psw':'ys987654'},
    # {'no':'17181343891',  'psw':'ys987654'},
    # {'no':'15197483478',  'psw':'ys987654'},
    # {'no':'17076741303',  'psw':'ys156354'},
    # {'no':'17180360545',  'psw':'ys156354'},
    # {'no':'17095948793',  'psw':'ys156354'},
    # {'no':'17181340585',  'psw':'ys156354'},
    # {'no':'17095949136',  'psw':'ys156354'},
    # {'no':'17096641822',  'psw':'ys156354'},
    # {'no':'17134753936',  'psw':'ys156354'},
    # {'no':'17096643159',  'psw':'ys156354'},
    # {'no':'17065416995',  'psw':'ys156354'},
    # {'no':'17010256036',  'psw':'ys156354'},
    # {'no':'17010259887',  'psw':'ys156354'},
    # {'no':'17181344073',  'psw':'ys156354'},
    # {'no':'13414136414',  'psw':'ys156354'},

    # {'no':'13518722402',  'psw':'you456789'},
    # {'no':'15140835581',  'psw':'you456789'},
    # {'no':'13941452914',  'psw':'you456789'},
    # {'no':'13282143376',  'psw':'you456789'},
    # {'no':'13941976071',  'psw':'you456789'},
    # {'no':'17186023381',  'psw':'you456789'},
    # {'no':'17724498217',  'psw':'you456789'},
    # {'no':'15916779246',  'psw':'you456789'},
    # {'no':'15140941943',  'psw':'you456789'},

    {'no':'woaiyangzhihui520@163.com',  'psw':'yc20161019'},
    {'no':'wodedaling.123@163.com',  'psw':'yc20161019'},
    {'no':'woaipj000@163.com',  'psw':'yc20161019'},
    {'no':'wodezhuanghao123@163.com',  'psw':'yc20161019'},
    {'no':'wohuiyi001@163.com',  'psw':'yc20161019'},
    {'no':'wohaofang55@163.com',  'psw':'yc20161019'},
    {'no':'wohune@163.com',  'psw':'yc20161019'},
    {'no':'wojiuaini-1316@163.com',  'psw':'yc20161019'},
    {'no':'woshi1181026@163.com',  'psw':'yc20161019'},
    {'no':'woshi5489757@163.com',  'psw':'yc20161019'},
    {'no':'woshiqianchen123@163.com',  'psw':'yc20161019'},
    {'no':'woyaoxingfu_yy@163.com',  'psw':'yc20161019'},
    {'no':'woshuai1314512@163.com',  'psw':'yc20161019'},
    {'no':'wujiapei.1996@163.com',  'psw':'yc20161019'},
    {'no':'wujunjian.14@163.com',  'psw':'yc20161019'},
    {'no':'wuhanfanqie@163.com',  'psw':'yc20161019'},
    {'no':'wuwuwu678910@163.com',  'psw':'yc20161019'},
    {'no':'wuyuqi5201314@163.com',  'psw':'yc20161019'},
    {'no':'wuliu69@163.com',  'psw':'yc20161019'},
    {'no':'wuxiaoyongkkk@163.com',  'psw':'yc20161019'},
    {'no':'ww1307367@163.com',  'psw':'yc20161019'},
    {'no':'wuxinfeng.pk@163.com',  'psw':'yc20161019'},
    {'no':'wuzhenlovefang@163.com',  'psw':'yc20161019'},
    {'no':'ww58969631@163.com',  'psw':'yc20161019'},
    {'no':'www.163.com2580@163.com',  'psw':'yc20161019'},
    {'no':'www.55you.con@163.com',  'psw':'yc20161019'},
    {'no':'ww517575698@163.com',  'psw':'yc20161019'},
    {'no':'ww--020620@163.com',  'psw':'yc20161019'},
    {'no':'www.zheng..com.cn@163.com',  'psw':'yc20161019'},
    {'no':'ww4217586@163.com',  'psw':'yc20161019'},
    {'no':'www.minidwg@163.com',  'psw':'yc20161019'},
    {'no':'www42102319850511@163.com',  'psw':'yc20161019'},
    {'no':'wwwaixiexin6722@163.com',  'psw':'yc20161019'},
    {'no':'www861115@163.com',  'psw':'yc20161019'},
    {'no':'wwwliwenhaook@163.com',  'psw':'yc20161019'},
    {'no':'wwww5492@163.com',  'psw':'yc20161019'},
    {'no':'wxyandcx@163.com',  'psw':'yc20161019'},
    {'no':'wybest1234@163.com',  'psw':'yc20161019'},
    {'no':'wx54201314807@163.com',  'psw':'yc20161019'},
    {'no':'wxo_880414@163.com',  'psw':'yc20161019'},
    {'no':'x.t5861@163.com',  'psw':'yc20161019'},
    {'no':'x2883174@163.com',  'psw':'yc20161019'},
    {'no':'xi517662752@163.com',  'psw':'yc20161019'},
    {'no':'xiongyiai300@163.com',  'psw':'yc20161019'},
    {'no':'xliang1992@163.com',  'psw':'yc20161019'},
    {'no':'xuancf@163.com',  'psw':'yc20161019'},
    {'no':'xuancf20061@163.com',  'psw':'yc20161019'},
    {'no':'xihuanni.mimi@163.com',  'psw':'yc20161019'},
    {'no':'xjzs5200000@163.com',  'psw':'yc20161019'},
    {'no':'xue3085@163.com',  'psw':'yc20161019'},
    {'no':'xuechenbing.cheng@163.com',  'psw':'yc20161019'},
    {'no':'xulinsheng.4246173@163.com',  'psw':'yc20161019'},
    {'no':'xunxiaojun5492698@163.com',  'psw':'yc20161019'},
    {'no':'xuke3510821@163.com',  'psw':'yc20161019'},
    {'no':'xuqiao1990922@163.com',  'psw':'yc20161019'},
    {'no':'xuwei5017203@163.com',  'psw':'yc20161019'},
    {'no':'xue15163508864@163.com',  'psw':'yc20161019'},
    {'no':'xusinuo2000@163.com',  'psw':'yc20161019'},
    {'no':'y31324084@163.com',  'psw':'yc20161019'},
    {'no':'yalp111@163.com',  'psw':'yc20161019'},
    {'no':'xuluhao-wo@163.com',  'psw':'yc20161019'},
    {'no':'yang592605574@163.com',  'psw':'yc20161019'},
    {'no':'yangyusheng2010@163.com',  'psw':'yc20161019'},
    {'no':'yaojinhuei123456@163.com',  'psw':'yc20161019'},
    {'no':'ychina138@163.com',  'psw':'yc20161019'},
    {'no':'yaochang584201314@163.com',  'psw':'yc20161019'},
    {'no':'yhl780821@163.com',  'psw':'yc20161019'},
    
    {'no':'yflijinxiang@163.com',  'psw':'yc20161019'},
    {'no':'yinaibiego@163.com',  'psw':'yc20161019'},
    {'no':'yirenbin@163.com',  'psw':'yc20161019'},
    {'no':'yiopfed@163.com',  'psw':'yc20161019'},
    {'no':'ying_2_yang@163.com',  'psw':'yc20161019'},
    {'no':'yian.ji63326789@163.com',  'psw':'yc20161019'},
    {'no':'yinqi6517795@163.com',  'psw':'yc20161019'},
    {'no':'yjlyl1597530@163.com',  'psw':'yc20161019'},
    {'no':'yiyiyiyi2006@163.com',  'psw':'yc20161019'},
    {'no':'yly930702@163.com',  'psw':'yc20161019'},
    {'no':'yk5661013@163.com',  'psw':'yc20161019'},
    {'no':'yishenghaowangji@163.com',  'psw':'yc20161019'},
    {'no':'yi-xiao-520@163.com',  'psw':'yc20161019'},
    {'no':'yong13569111945@163.com',  'psw':'yc20161019'},
    {'no':'youguishou125@163.com',  'psw':'yc20161019'},
    {'no':'ykk5000@163.com',  'psw':'yc20161019'},
    {'no':'yjtmyiu941@163.com',  'psw':'yc20161019'},
    {'no':'yu_cheng_ai@163.com',  'psw':'yc20161019'},
    {'no':'yqalong@163.com',  'psw':'yc20161019'},
    {'no':'yu13121312@163.com',  'psw':'yc20161019'},
    {'no':'ytfjia@163.com',  'psw':'yc20161019'},

]


def getCookies(weibo):
    """ 获取Cookies """
    cookies = []
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        username = base64.b64encode(account.encode('utf-8')).decode('utf-8')
        postData = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": username,
            "service": "sso",
            "sp": password,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT",
        }
        session = requests.Session()
        r = session.post(loginURL, data=postData)
        jsonStr = r.content.decode('gbk')
        info = json.loads(jsonStr)
        if info["retcode"] == "0":
            print "Get Cookie Success!( Account:%s )" % account
            cookie = session.cookies.get_dict()
            cookies.append(cookie)
        else:
            print "Failed!( Reason:%s )" % info['reason']
    return cookies


cookies = getCookies(myWeiBo)
print "Get Cookies Finish!( Num:%d)" % len(cookies)
