headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'Accept' : 'text/css,*/*;q=0.1',
            'Accept-Encoding' : 'Accept-Encoding:gzip, deflate, sdch',
            'Accept-Language' : 'zh-CN,zh;q=0.8',
            'Connection' : 'keep-alive'
           }
proxy_list = [
            'http://123.245.64.64:8888',
            'http://218.202.111.10:80',
            'http://101.96.11.31:80',
            'http://120.198.231.2:8081',
            'http://111.47.171.149:8000',
            'http://183.209.233.128:8888',
            'http://101.96.11.47:80',
            'http://101.96.11.29:80',
            'http://101.96.11.43:80',
            'http://49.117.146.202:8090',
            'http://183.250.160.57:8888',
            'http://183.142.221.202:8888',
            'http://223.8.22.22:8888',
            'http://183.61.236.54:3128',
            'http://175.31.116.41:8888',
            'http://101.96.11.44:80',
            'http://110.80.62.110:8888',
            'http://101.96.11.30:80',
            'http://180.76.135.145:3128',
            'http://49.117.146.204:8088',
            'http://49.117.146.206:8088',
            'http://101.96.11.39:80',
            'http://101.96.11.41:80',
            'http://101.96.11.40:80',
            'http://101.96.11.32:80',
            'http://115.231.223.235:80',
            'http://60.191.167.93:3128',
            'http://202.100.167.180:80',
            'http://122.226.128.251:3128',
            'http://60.190.252.29:9090',
            'http://60.191.146.188:3128',
            'http://101.96.11.42:80',
            'http://202.100.167.149:80',
            'http://202.100.167.137:80',
            ]


def config_logger_from(logger_name):
    """logging setting for channel_extract.py
    return None
    """
    import logging
    import os
    from datetime import datetime
    LOG_FILENAME_PATH = "logs"
    if not isinstance(logger_name, str):
        raise NameError("Please use a string to name the log file")
    LOG_FILENAME = logger_name.upper() \
                   + " " \
                   + str(datetime.now()) \
                   + ".log"
    LOG_FULL_FILENAME = os.path.join(LOG_FILENAME_PATH, LOG_FILENAME).replace(" ", "_")
    logging.basicConfig(filename=LOG_FULL_FILENAME, level=logging.INFO)

