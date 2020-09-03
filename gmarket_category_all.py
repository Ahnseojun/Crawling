import scrapy


class GmarketCategoryAllSpider(scrapy.Spider):
    name = 'gmarket_category_all'
    def start_requests(self):
        yield scrapy.Request(url ='http://corners.gmarket.co.kr/Bestsellers', callback=self.parse_mainpages)

    def parse_mainpages(self, response):
        print('parse_mainpages')

        category_links = response.css('div.gbest-cate ul.by-group li a::attr(href)').getall()
        category_names = response.css('div.gbest-cate ul.by-group li a::text').getall()
        for index, category_link in enumerate(category_links):
            #메인 카테고리 주소 / 이름을 가져오는 소스
            #category_names[index]
            yield scrapy.Request(url = 'http://corners.gmarket.co.kr' + category_link, callback=self.parse_main_category, meta={'main_category_name':category_names[index]})

    def parse_main_category(self, response):
        print('parse_main_category', response.meta['main_category_name']) #meta['main_category_name']는 해당 메인카테고리에 맞는 딕셔너리를 가져옴

        best_items = response.css('div.best-list')
        for index, item in enumerate(best_items[1].css('li')):
            ranking = index + 1
            title = item.css('a.itemname::text').get()
            ori_price = item.css('div.o-price span::text').get()
            dis_price = item.css('div.s-price strong span span::text').get()
            discount_percent = item.css('div.s-price em::text').get()

            if ori_price == None :
                ori_price = dis_price
            
            ori_price = ori_price.replace(',','').replace('원','')
            dis_price = dis_price.replace(',','').replace('원','')

            if discount_percent == None :
                discount_percent = '0'
            else :
                discount_percent = discount_percent.replace('%','')            
            print(ranking, title, ori_price, dis_price, discount_percent)