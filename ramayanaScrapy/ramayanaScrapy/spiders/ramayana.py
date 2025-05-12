import scrapy
from scrapy.http import HtmlResponse

class RamayanaSpider(scrapy.Spider):
    name = "ramayana"
    allowed_domains = ["www.valmikiramayan.net"]
    start_urls = ["https://www.valmikiramayan.net/"]

    def parse(self, response):
        frame_src = response.css('frame::attr(src)').get()  

        if frame_src:
            full_url = response.urljoin(frame_src)
            yield scrapy.Request(url=full_url, callback=self.parse_frame)

        else:
            self.logger.info("No iframe found in the page")

    def parse_frame(self, response):
        body_content = response.xpath("/html/body").get()
        booksName = response.xpath("/html/body/ol/li/a/text()").getall()
        totalChapters = response.xpath("/html/body/ol/li/text()").getall()
        booksUrl = response.xpath("/html/body/ol/li/a/@href").getall()
        parentUrl = 'https://www.valmikiramayan.net/'

        for url in booksUrl:
            relativeUrl = parentUrl + url
            print(relativeUrl)
            if "ayodhya" in relativeUrl:
                yield scrapy.Request(url=relativeUrl,callback=self.parse_book_ayodha)
            elif "baala" in relativeUrl:
                yield scrapy.Request(url=relativeUrl,callback=self.parse_book_baala)
            elif "kish" in relativeUrl:
                yield scrapy.Request(url=relativeUrl,callback=self.parse_book_krish)
            elif "yuddha" in relativeUrl:
                yield scrapy.Request(url=relativeUrl,callback=self.parse_book_yuddha)
             

    def parse_book_baala(self,response):
        chapters = response.xpath('/html/body/center[2]/table/tr/td[2]/a/@href').getall()
        sargaUrl =  'https://www.valmikiramayan.net/utf8/baala/' + chapters[0]
        #yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)

    def parse_book_sarga(self,response):
        sarga = response.xpath("/html/body/h3[1]").getall()
        frame_url = response.css("frame::attr('src')").get()
        print(frame_url)
        if(frame_url):
            full_url = response.urljoin(frame_url)
            yield scrapy.Request(url=full_url, callback=self.parse_book_sarga)
        else:
            header = response.css('p.tat::text').getall()
            print(header)  

        
        
    def parse_book_ayodha(self,response):
        chapters=response.css("table a.nav::attr(href)").getall()
        #print("ayodha",chapters)
        #chapters = response.xpath('/html/body/center[2]/table/tr/td[2]/a/@href').getall()
        
        sargaUrl =  'https://www.valmikiramayan.net/utf8/ayodhya/' + chapters[0]
        #$#print("dargeffsdfsdf",sargaUrl)
       #yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)

    def parse_book_krish(self,response):
        chapters=response.css("table a.nav::attr(href)").getall()
        #print("krish",chapters)
    def parse_book_yuddha(self,response):
        chapters=response.css("table a.nav::attr(href)").getall()
        sargaUrl =  'https://www.valmikiramayan.net/utf8/yuddha/' + chapters[0]
        print("dargeffsdfsdf",sargaUrl)
        yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)
