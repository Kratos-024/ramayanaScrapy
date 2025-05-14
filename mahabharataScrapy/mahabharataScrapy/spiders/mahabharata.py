import scrapy


class MahabharataSpider(scrapy.Spider):
    name = "mahabharata"
    allowed_domains = ["sacred-texts.com"]
    start_urls= ["https://sacred-texts.com/hin/maha/index.htm"]
    parent_url = 'https://sacred-texts.com/hin/'
    count = 0
    def parse(self, response):
        parva_list = response.css("span.c_e span.c_t a::attr('href')").getall()
        
        for parva in parva_list:
            relative_url = self.parent_url+parva[3:]
            yield scrapy.Request(url=relative_url,callback=self.parse_parva)
            
    def parse_parva(self,response):
        parava_name = response.xpath("//h3[text()='Kisari Mohan Ganguli, tr.']/following-sibling::h3/text()").getall()
        book_name = response.xpath("/html/body/h2/text()").get()
        self.count+=1
        sections = response.xpath("/html/body/a/@href").getall()
        
        for section in sections:
            
            relative_url = self.parent_url + f'{section[0:3]}/' + section
            yield scrapy.Request(url=relative_url,callback=self.parse_section,meta={    "BookName":book_name,            "section_no":section[3:]
            })
          
    def parse_section(self,response):
        book_name = response.meta.get("BookName")
        section_no = response.meta.get("section_no")[0:3]
        para = response.xpath("//hr[2]/preceding-sibling::p/text()").getall()
        if(len(para)==0):
            para= response.xpath("/html/body/p[2]/text()").getall()
            
        yield {
            "Book":book_name,
            "Section":section_no,
            "Translation":para
        }
        
        
        
        
        
        
        
