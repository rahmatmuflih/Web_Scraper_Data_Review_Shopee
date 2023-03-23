import requests
import json
import pandas as pd
from seleniumwire import webdriver
from seleniumwire.utils import decode
import time
from os.path import exists

start_time = time.time()
cari = 'ssd'
start_page = 21
finish_page = 26
op = webdriver.ChromeOptions()

op.add_argument('headless')
driver = webdriver.Chrome(options=op)

data = []

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
}

def getUrl():
    urls = []
    page_urls = []

    for i in range(start_page, finish_page):
        url =  'https://shopee.co.id/api/v4/search/search_items?by=relevancy&keyword={}&limit=60&newest={}'.format(cari, i*60)
        page_url = 'https://shopee.co.id/search?keyword={}&page={}'.format(cari, i)
        urls.append(url)
        page_urls.append(page_url)

    return page_urls, urls

def getAccess(page_url, url):
    driver.get(page_url)
    
    driver.implicitly_wait(10)

    rows = ''

    for request in driver.requests:
        if request.response:
            if request.url.startswith(url):
                response = request.response
                body = decode(response.body, response.headers.get('Content-Encoding', 'Identity'))
                decoded_body = body.decode('utf8')
                json_data = json.loads(decoded_body)
                rows = json_data['items']

    return rows

def scrapeData(rows):

    data = []
    itemid = ''
    shopid = ''
    rating = ''
    comment = ''
    rating_count4 = ''
    rating_count0 = ''
    rating_count1 = ''
    rating_count2 = ''
    rating_count3 = ''
    rating_count5 = ''
    rating_star = ''
    anonymous = ''
    author_shopid = ''
    author_username = ''
    cat_id = ''
    author_username = ''
    cmtid = ''
    count_rating_with_image = ''
    count_with_context = ''
    ctime = ''
    editable = ''
    mtime = ''
    orderid = ''
    product_title = ''
    userid = ''
    
    for i in range(0, len(rows)):

        itemid = rows[i]['itemid']
        shopid = rows[i]['shopid']
        rating_count0 = rows[i]['item_basic']['item_rating']['rating_count'][0]
        rating_count1 = rows[i]['item_basic']['item_rating']['rating_count'][1]
        rating_count2 = rows[i]['item_basic']['item_rating']['rating_count'][2]
        rating_count3 = rows[i]['item_basic']['item_rating']['rating_count'][3]
        rating_count4 = rows[i]['item_basic']['item_rating']['rating_count'][4]
        rating_count5 = rows[i]['item_basic']['item_rating']['rating_count'][5]
        rating_star = rows[i]['item_basic']['item_rating']['rating_star']
        count_rating_with_image = rows[i]['item_basic']['item_rating']['rcount_with_image']
        count_with_context = rows[i]['item_basic']['item_rating']['rcount_with_context']
        cat_id = rows[i]['item_basic']['catid']
        url_detail = 'https://shopee.co.id/api/v2/item/get_ratings?filter=0&flag=1&itemid={}&limit=6&offset=0&shopid={}&type=0'.format(itemid,shopid)   

        req = requests.get(url_detail, headers=headers).json()

        rows2 = req['data']
        rating = rows2['item_rating_summary']['rating_total']
        try:
            comment = rows2['ratings'][0]['comment']
            anonymous = rows2['ratings'][0]['anonymous']
            author_shopid = rows2['ratings'][0]['author_shopid']
            author_username = rows2['ratings'][0]['author_username']
            cmtid = rows2['ratings'][0]['cmtid']
            ctime = rows2['ratings'][0]['ctime']
            editable = rows2['ratings'][0]['editable']
            mtime = rows2['ratings'][0]['mtime']
            orderid = rows2['ratings'][0]['orderid']
            product_title = rows2['ratings'][0]['product_items'][0]['name']
            userid = rows2['ratings'][0]['userid']
        except Exception as e:
            print(e)

        data.append(
            (
                anonymous,
                author_shopid,
                author_username,
                cat_id,
                cmtid,
                comment,
                count_rating_with_image,
                count_with_context,
                ctime,
                editable,
                itemid,
                mtime,
                orderid,
                product_title,
                rating,
                rating_count0,
                rating_count1,
                rating_count2,
                rating_count3,
                rating_count4,
                rating_count5,
                rating_star,
                shopid,
                userid
            )
        )

    return data

def importToCSV():
    df = pd.DataFrame(
        all_data, 
        columns=[
                'anonymous',
                'author_shopid',
                'author_username',
                'cat_id',
                'cmtid',
                'comment',
                'count_rating_with_image',
                'count_with_context',
                'ctime',
                'editable',
                'item_id',
                'mtime',
                'orderid',
                'product_title',
                'rating',
                'rating_count0',
                'rating_count1',
                'rating_count2',
                'rating_count3',
                'rating_count4',
                'rating_count5',
                'rating_star',
                'shopid',
                'userid'
            ])

    print()
    print(df)

    file_exist = exists('hasil\\scrape_shopee.csv')

    if file_exist:
        df.to_csv('hasil\\scrape_shopee.csv', mode='a', header=False, index=False)
    else:
        df.to_csv('hasil\\scrape_shopee.csv', index=False)

    print('\nData Telah Tersimpan')
    print("\n--- {} minutes ---".format(((time.time() - start_time)/60)))


if __name__ == '__main__':
    all_data = []
    all_url = getUrl()

    for i in range(0, len(all_url[0])):
        page_url = all_url[0][i]
        url = all_url[1][i]
        access_bypass = getAccess(page_url, url)
        time.sleep(5)
        data = scrapeData(access_bypass)
        all_data.extend(data)

    importToCSV()
    driver.quit()