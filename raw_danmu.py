import requests
import re


def get_response(html_url):
    cookie = open("cookie.txt", "r").readlines()[0]
    headers = {
        'cookie': cookie,
        'origin': 'https://www.bilibili.com',
        'referer': 'https://www.bilibili.com/video/BV19E41197Kc',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }
    response = requests.get(url=html_url, headers=headers)
    return response


def get_date(html_url):
    response = get_response(html_url)
    json_data = response.json()
    date = json_data['data']
    print(date)
    return date


def save(content):
    for i in content:
        with open('B站弹幕.txt', mode='a', encoding='utf-8') as f:
            f.write(i)
            f.write('\n')
            # print(i)


def main(html_url, cid):
    data = get_date(html_url)
    for date in data:
        url = f'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={cid}&date={date}'
        html_data = get_response(url).text
        result = re.findall(".*?([\u4E00-\u9FA5]+).*?", html_data)
        save(result)


if __name__ == '__main__':
    oid = input("Enter oid")
    month = input("Enter month (i.e. 2022-01)")
    one_url = f'https://api.bilibili.com/x/v2/dm/history/index?type=1&oid={oid}&month={month}'
    main(one_url, oid)
