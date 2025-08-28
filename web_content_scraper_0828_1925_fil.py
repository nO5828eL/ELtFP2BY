# 代码生成时间: 2025-08-28 19:25:36
import requests
from bs4 import BeautifulSoup
from celery import Celery

# 配置CELERY
app = Celery('web_content_scraper', broker='pyamqp://guest@localhost//')

# 抓取网页内容的任务
@app.task
def scrape_web_content(url):
    """
    异步抓取给定URL的网页内容。

    参数:
    url (str): 要抓取的网页URL。

    返回:
    str: 网页内容。

    异常:
    requests.RequestException: 如果请求失败。
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None

    # 解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.prettify()

# 测试抓取任务
if __name__ == '__main__':
    example_url = 'http://example.com'
    result = scrape_web_content.delay(example_url)
    print(f"抓取结果: {result.get()}")
