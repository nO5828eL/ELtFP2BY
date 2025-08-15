# 代码生成时间: 2025-08-16 07:25:53
import requests
from bs4 import BeautifulSoup
from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
from celery.utils.log import get_task_logger
from requests.exceptions import RequestException
from urllib.parse import urljoin, urlparse

# 设置Celery配置
celery_app = Celery('web_scraper',
                    broker='pyamqp://guest@localhost//')

# 获取Celery的logger
logger = get_task_logger(__name__)

# Celery任务装饰器
@celery_app.task(name='scraping.scrape_page', soft_time_limit=60)  # 设置任务超时时间为60秒
def scrape_page(url, domain):
    '''
    抓取网页内容的任务
    :param url: 要抓取的网页URL
    :param domain: 网页内容属于的域
    :return: 网页内容
    '''
    try:
        # 发送HTTP GET请求
        response = requests.get(url)
        response.raise_for_status()  # 检查响应状态

        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取网页所有链接
        for link in soup.find_all('a', href=True):
            # 构造完整的URL路径
            full_url = urljoin(domain, link['href'])
            # 检查URL是否属于同一域
            if urlparse(full_url).netloc == urlparse(domain).netloc:
                # 递归抓取链接指向的页面内容
                scrape_page.delay(full_url, domain)

        # 返回网页内容
        return soup.prettify()
    except SoftTimeLimitExceeded:
        logger.error(f'Scraping task timed out for {url}')
    except RequestException as e:
        logger.error(f'Request failed for {url}: {e}')
    except Exception as e:
        logger.error(f'An error occurred: {e}')
    return None

# 主函数，用于测试和启动Celery Worker
def main():
    '''
    定义主函数，用于测试和启动Celery Worker
    '''
    # 测试抓取网页内容的任务
    task = scrape_page.delay('http://example.com', 'http://example.com')
    # 等待任务完成并打印结果
    result = task.get()
    print(result)

if __name__ == '__main__':
    main()