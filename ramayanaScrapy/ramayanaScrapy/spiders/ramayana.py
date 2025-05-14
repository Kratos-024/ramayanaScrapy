import scrapy
from scrapy.http import HtmlResponse

class RamayanaSpider(scrapy.Spider):
    name = "ramayana"
    allowed_domains = ["www.valmikiramayan.net"]
    start_urls = ["https://www.valmikiramayan.net/"]

    
    count=0
    S_no=0
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
            
            if "baala" in f'{relativeUrl}':   
                self.count=0
                yield scrapy.Request(url=relativeUrl,callback=self.parse_book_baala) 
            elif "kish" in f'{relativeUrl}':
                self.count=0
                yield scrapy.Request(url=relativeUrl,callback=self.parse_book_krish)
            elif "aranya" in f'{relativeUrl}':
                self.count=0
                yield scrapy.Request(url=relativeUrl,callback=self.parse_book_aranya)
            elif "yuddha" in f'{relativeUrl}':
                self.count=0
                yield scrapy.Request(url=relativeUrl,callback=self.parse_book_yuddha)
            elif "ayodhya" in f'{relativeUrl}':
                self.count=0
                yield scrapy.Request(url=relativeUrl,callback=self.parse_book_ayodha)
            elif "sundara" in f'{relativeUrl}':
                self.count=0
                yield scrapy.Request(url=relativeUrl,callback=self.parse_book_sundara)


    def parse_book_sundara(self,response):
        chapters = response.xpath('/html/body/center[2]/table/tr/td[2]/a/@href').getall()
        for chapter in chapters:
            sargaUrl =  'https://www.valmikiramayan.net/utf8/sundara/' + chapter
            yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)
    def parse_book_aranya (self,response):
        chapters = response.css("table tr td center table tr td a::attr('href')").getall()
        for chapter in chapters:
            sargaUrl =  'https://www.valmikiramayan.net/utf8/aranya/' + chapter
            yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)
    def parse_book_baala(self,response):
        chapters = response.xpath('/html/body/center[2]/table/tr/td[2]/a/@href').getall()
        for chapter in chapters:
            sargaUrl =  'https://www.valmikiramayan.net/utf8/baala/' + chapter
            yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)
         
    def parse_book_ayodha(self,response):
        chapters=response.css("table a.nav::attr(href)").getall()
        for chapter in chapters:
            sargaUrl =  'https://www.valmikiramayan.net/utf8/ayodhya/' + chapter
            yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)

    def parse_book_krish(self,response):
        chapters=response.css("table a.nav::attr(href)").getall()
        for chapter in chapters:
            sargaUrl =  'https://www.valmikiramayan.net/utf8/kish/' + chapter
            yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)
    def parse_book_yuddha(self,response):
        chapters=response.css("table a.nav::attr(href)").getall()
        for chapter in chapters:
            sargaUrl =  'https://www.valmikiramayan.net/utf8/yuddha/' + chapter
            yield scrapy.Request(url=sargaUrl,callback=self.parse_book_sarga)
  
    def parse_book_sarga(self,response):
        frame_url = response.css("frame::attr(src)").get()
        if(frame_url):
            full_url = response.urljoin(frame_url)
            yield scrapy.Request(url=full_url, callback=self.parse_book_sarga)
        else:
            yield from self.parse_verse(response)

    def parse_verse(self, response):
        if 'balasans' in f'{response}':
                # print("bala",self.count)
                book = "bala"
                sarga= f'{response}'.split("balasans")[1][0:2]
        elif 'kishkindha' in f'{response}':
                # print("kishkindha",self.count)
                book="kishkindha"
                
                sarga= f'{response}'.split("/kishkindhasans")[1][0:3]
        elif 'yuddha' in f'{response}':
                # print("yuddha",self.count)
                book="yuddha"
                sarga= f'{response}'.split("/yuddhasans")[1][0:3]
        elif 'ayodhya' in f'{response}':
                # print("ayodhya",self.count)

                book="ayodhya"
                sarga= f'{response}'.split("/ayodhyasans")[1][0:3]
        elif 'sundara' in f'{response}':
                # print("sundara",self.count)

                book="sundara"
                sarga= f'{response}'.split("/sundarasans")[1][0:3]
        elif 'aranya' in f'{response}':
                # print("aranya",self.count)
            
                book="aranya"
                sarga= f'{response}'.split("/aranyasans")[1][0:3]
        self.count+=1
        sarga = ''.join(c for c in sarga if c.isdigit())

        translations = response.css('p.tat::text').getall()
        Shloka = 0
        for translation in translations:
            self.logger.info(f"Translation: {translation}")  # Add debug log

            Shloka+=1
            self.S_no+=1
            yield {
            "S.No":self.S_no,
            "Chapter":self.count,
            "Kanda":book,
            "Sarga":sarga,
            "Shloka":Shloka,
            "Translation":translation  
            }



            
     
       
        
       