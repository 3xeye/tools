# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup as BS
import urllib2 as url
import urllib
import json
import os
import logging.config

def setup_logging(default_path='logging.json', default_level=logging.DEBUG, env_key='LOG_CFG'):
    """Setup logging configuration """
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


args = [{'kw':'股指', 'name':'gz'}, {'kw':'600556', 'name':'hq'}, {'kw':'600666', 'name':'xnyy'}, {'kw':'002186', 'name':'qjd'}]

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

setup_logging()
nx = Nx(args)
nx.process()

# # print bs.original_encoding
# # print (bs.title).encode('gb18030')
# # print (bs.title.name).encode('gb18030')
