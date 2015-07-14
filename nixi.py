# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup as BS
import urllib2 as url
import urllib
import json
import os
import logging.config

def setup_logging(default_path='logging.json', default_level=logging.DEBUG, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
        
keys = ('name', 'opening', 'closing', 'now', 'high', 'low', 'buy', 'sell', 'volume', 'amount', '买一量', '买一价', '买二量', '买二价', '买三量', '买三价', '买四量', '买四价', '买五量', '买五价', '卖一量', '卖一价', '卖二量', '卖二价', '卖三量', '卖三价', '卖四量', '卖四价', '卖五量', '卖五价', 'date', 'time', 'other')
key_idx_name = 0
key_idx_opening = 1
key_idx_closing = 2
key_idx_now = 3
key_idx_high = 4
key_idx_low = 5
key_idx_buy = 6
key_idx_sell = 7
key_idx_volume = 8
key_idx_amount = 9


args = [{'kw':'股指', 'name':'gz'}, {'kw':'600556', 'name':'hq'}, {'kw':'600666', 'name':'xnyy'}, {'kw':'002186', 'name':'qjd'}]
arg1 = [{'kw':'000001', 'name':'gz'}, {'kw':'600556', 'name':'hq'}, {'kw':'600666', 'name':'xnyy'}, {'kw':'002186', 'name':'qjd', 'prefix':'sz'}]

# http://hq.sinajs.cn/list=sh600666
# http://hq.sinajs.cn/list=sh000001
class Nx(object):
    
    def __init__(self, args):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('Nx init with %s', args)
        self.args = args
        
    def baidu_search(self, keyword):
        p = {'wd': keyword}
        res = url.urlopen("http://www.baidu.com/s?" + urllib.urlencode(p))
        html = res.read()
        return html
    
    def printResult(self, arg, html):
        bs = BS(html, from_encoding="utf8")
        c = bs.select('.op-stockdynamic-moretab-cur-num')
        num = c[0].string if c else 0
        
        c = bs.select('.op-stockdynamic-moretab-cur-info')
        per = c[0].string if c else 0
        
        reStr = '%s %s %s' % (arg.get('name', 'noName'), num, per)
        self.logger.debug(reStr)
        print reStr
    
    def printResultFind(self, arg, html):
        bs = BS(html, from_encoding="utf8")
        
        c = bs.find_all('span', attrs={'class':'op-stockdynamic-moretab-cur-num'})
        num = c[0].string if c else 0
        
        c = bs.find_all('span', attrs={'class':'op-stockdynamic-moretab-cur-info'})
        per = c[0].string if c else 0
        
        reStr = '%s %s %s' % (arg.get('name', 'noName'), num, per)
        self.logger.debug(reStr)
        print reStr
    
    def process(self):
        if not self.args:
            print 'no args to process'
            return
        for arg in self.args:
            keyword = arg.get('kw', '')
            html = self.baidu_search(keyword)
            self.printResultFind(arg, html)
            
            
class NxSina(object):
    
    def __init__(self, args):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info('NxSina init with %s', args)
        self.args = args
        
    def getContent(self, arg):
        keyword = arg.get('kw', '')
        prefix = arg.get('prefix', 'sh')
        res = url.urlopen("http://hq.sinajs.cn/list=%s%s" % (str(prefix), str(keyword)))
        html = res.read()
        return html

    def printResultFind(self, arg, html):
        #self.logger.debug(html.decode("gbk"))
        retStr = html.decode("gbk")
        if not retStr:
            self.logger.info("no result to process")
            return
        array = retStr.split("\"")
        if not array or len(array) <= 2:
            self.logger.info("result format error")
            return
        content = array[1]
        if not content:
            self.logger.info("result format error")
            return
        values = content.split(",")
        
        retStr = '%s, open:%s, close:%s, now:%s, high:%s, low:%s, buy:%s, sell:%s, volume:%s, amount:%s' % \
            (values[key_idx_name], values[key_idx_opening], values[key_idx_closing], values[key_idx_now], values[key_idx_high], \
             values[key_idx_low], values[key_idx_buy], values[key_idx_sell], values[key_idx_volume], values[key_idx_amount])
        
        print retStr
    
    def process(self):
        if not self.args:
            print 'no args to process'
            return
        for arg in self.args:
            html = self.getContent(arg)
            self.printResultFind(arg, html)

setup_logging()
nx = NxSina(arg1)
nx.process()

# # print bs.original_encoding
# # print (bs.title).encode('gb18030')
# # print (bs.title.name).encode('gb18030')
