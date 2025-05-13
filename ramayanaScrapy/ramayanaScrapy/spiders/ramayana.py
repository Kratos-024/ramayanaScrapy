import scrapy
from scrapy.http import HtmlResponse

class RamayanaSpider(scrapy.Spider):
    name = "ramayana"
    allowed_domains = ["www.valmikiramayan.net"]
    start_urls = ["https://www.valmikiramayan.net/"]

    countt=0
    countttt=0
    listt = []
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
            #print(relativeUrl)
            
            if "baala" in relativeUrl:   
                yield scrapy.Request(url=relativeUrl,callback=self.parse_book_baala)
            elif "kish" in relativeUrl:
                  yield scrapy.Request(url=relativeUrl,callback=self.parse_book_krish)
            elif "yuddha" in relativeUrl:
                yield scrapy.Request(url=relativeUrl,callback=self.parse_book_yuddha)
            elif "ayodhya" in relativeUrl:
                yield scrapy.Request(url=relativeUrl,callback=self.parse_book_ayodha)
             

    def parse_book_baala(self,response):
        chapters = response.xpath('/html/body/center[2]/table/tr/td[2]/a/@href').getall()
        for chapter in chapters:
            sargaUrl =  'https://www.valmikiramayan.net/utf8/baala/' + chapter
            yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)

    def parse_book_sarga(self,response):
        frame_url = response.css("frame::attr(src)").get()
        if(frame_url):
            full_url = response.urljoin(frame_url)
            yield scrapy.Request(url=full_url, callback=self.parse_book_sarga)
            
        
        else:
            translations = response.css('p.tat::text').getall()
            if 'balasans' in f'{response}':
                book = "balasans"
                sarga= f'{response}'.split("balasans")[1][0:2]
            elif 'kishkindha' in f'{response}':
                book="kishkindha"
                sarga= f'{response}'.split("/kishkindhasans")[1][0:3]
            elif 'yuddha' in f'{response}':
                book="yuddha"
                sarga= f'{response}'.split("/yuddha")[1][0:3]
            elif 'ayodhya' in f'{response}':
                print("resseresr",response)
                book="ayodhya"
                sarga= f'{response}'.split("/ayodhya")[1][0:3]
            self.countttt+=1
            #self.listt.append(sarga)
            
            yield {
                'book':book,
                "chapter":self.countttt,
                "sarge":sarga,
                "Tat":translations
             }
      
            
             
                              

        
        
    def parse_book_ayodha(self,response):
        chapters=response.css("table a.nav::attr(href)").getall()
        for chapter in chapters:
            sargaUrl =  'https://www.valmikiramayan.net/utf8/ayodhya/' + chapter
            yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)

        
        #$#print("dargeffsdfsdf",sargaUrl)
        #yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)

    def parse_book_krish(self,response):
        chapters=response.css("table a.nav::attr(href)").getall()
        #chapters = response.xpath('/html/body/center[2]/table/tr/td[2]/a/@href').getall()
        for chapter in chapters:
            sargaUrl =  'https://www.valmikiramayan.net/utf8/kish/' + chapter
            yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)
        #print("krish",chapters)
    def parse_book_yuddha(self,response):
        chapters=response.css("table a.nav::attr(href)").getall()
        for chapter in chapters:
            sargaUrl =  'https://www.valmikiramayan.net/utf8/yuddha/' + chapter
            yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)
