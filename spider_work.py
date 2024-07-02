import requests
from lxml import etree
import time
from dbUtils import DBUtils
from multiprocessing import Pool

# 加入请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
    'Connection': 'close'}

# 创建数据库工具类
db = DBUtils()

# 数组，存放每页数据
# list_page_info = []

# 标志，是否第一次爬取数据
flag_first_access = True
# 存放基本属性名称
list_basic_attribute_name = []


def get_sub_links(url):
    try:
        res = requests.get(url, headers=headers, timeout=2)
    except (requests.Timeout, requests.ConnectTimeout,):
        print("网络连接失败")
        return
    except requests.exceptions.ConnectionError:
        print("网络连接错误，需要休息。。。")
        time.sleep(3)
        return

    selector = etree.HTML(res.text)
    # 获取详情页urls
    sub_links = selector.xpath('/html/body/div[4]/div[1]/ul/li/div[1]/div[1]/a/@href')
    for sub_link in sub_links:
        print('详情地址：', sub_link)
        # 获取详情页的数据
        get_info(sub_link)
        # dict_item = get_info(sub_link)
        # 将数据放入数组中
        # list_page_info.append(dict_item)
        # 睡眠0.5s，防止访问过快
        time.sleep(0.5)
    # 插入一页数据
    # data_process(list_page_info)
    return

def get_info(url):
    dict_house_info = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    try:
        res = requests.get(url, headers=headers, timeout=2)
        res.raise_for_status()
    except (requests.Timeout, requests.ConnectionError) as e:
        print(f"网络异常: {e}")
        return

    selector = etree.HTML(res.text)

    try:
        # 提取标题
        title = selector.xpath('//h1[@class="main"]/text()')
        dict_house_info['标题名称'] = title[0].strip() if title else "未提供标题"

        # 提取总价
        price = selector.xpath('//span[@class="total"]/text()')
        dict_house_info['房屋总价'] = price[0] + "万" if price else "未提供价格"

        # 提取小区名称和行政区域
        community = selector.xpath('//div[@class="communityName"]/a[@class="info "]/text()')
        dict_house_info['小区名称'] = community[0].strip() if community else "未提供"

        area = selector.xpath('//div[@class="areaName"]/span[@class="info"]/a/text()')
        dict_house_info['行政区域'] = ' '.join([a.strip() for a in area]) if area else "未提供"

        # 提取地址
        address = selector.xpath('//div[@class="areaName"]/span[@class="info"]/text()')
        dict_house_info['房屋地址'] = address[-1].strip() if address else "未提供具体地址"

        # 提取房屋信息
        house_info = selector.xpath('//div[@class="base"]/div[@class="content"]/ul/li')
        for item in house_info:
            key = item.xpath('./span/text()')[0].strip()
            value = ''.join(item.xpath('./text()')).strip()
            dict_house_info[key] = value if value else "未提供"

        # 提取单价
        unit_price = selector.xpath('//span[@class="unitPriceValue"]/text()')
        dict_house_info['单位价格'] = unit_price[0] if unit_price else "未提供"

        # 提取关注人数
        follow_info = selector.xpath('//span[@id="favCount"]/text()')
        dict_house_info['关注人数'] = follow_info[0] if follow_info else "未提供"

    except IndexError as e:
        print(f"处理 {url} 时出现索引错误: {e}")

    # 打印提取的信息
    for k, v in dict_house_info.items():
        print(k, ':', v)

    # 插入单个数据
    data_process(dict_house_info)
    return dict_house_info



def data_process(info):
    # 连接数据库
    db.db_connect()

    db.db_insert_one(info)

    db.db_close()

    return


if __name__ == '__main__':
    urls = ['https://nj.lianjia.com/ershoufang/pg{}sf1//'.format(num) for num in range(1, 40)]

    # 单进程
    # for url in urls:
    #     print(url)
    #     # 获得爬取数据的详细url
    #     get_sub_links(url)

    # 多进程
    start_time = time.time()
    pool = Pool(processes=3)
    pool.map(get_sub_links, urls)
    end_time = time.time()
    print('运行时间：', end_time - start_time)

    # 测试
    # url = 'https://nj.lianjia.com/ershoufang/103102604811.html'
    # get_info(url)
