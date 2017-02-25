import url_manager
import html_downloader
import html_parser
import html_outputer

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        count = 0
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                #self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                print 'craw %d : %s' % (count, new_url)
                #count = count + 1

                #if count == 30:
                 #break;
            except Exception as e:
                print e

        #return self.outputer.get_datas()
        rev_data = self.outputer.get_datas()
        return rev_data[0]
        #print rev_data[0]
        # for key, value in rev_data[0].iteritems():
        #     print rev_data[0][key]


# if __name__ == "__main__":
#     root_url = "http://www.qiushibaike.com/8hr/page/1"
#     obj_spider = SpiderMain()
#     obj_spider.craw(root_url)