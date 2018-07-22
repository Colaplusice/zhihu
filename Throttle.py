from urllib.parse import urlparse
import datetime
import time

class Throttle:
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        # x 对同一个域名限制访问时间
        print(url)
        domain = urlparse(url).netloc
        print('域名是:%s' % domain)
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
                print('睡了%s' % sleep_secs)
            else:
                print('秒数%s' % sleep_secs)
        self.domains[domain] = datetime.datetime.now()
