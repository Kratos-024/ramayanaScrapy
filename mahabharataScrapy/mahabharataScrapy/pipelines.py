from itemadapter import ItemAdapter
import re

class MahabharatascrapyPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if 'Section' in adapter:
            adapter['Section'] = self.extract_digits(adapter['Section'])

        if 'Translation' in adapter and isinstance(adapter['Translation'], list):
            adapter['Translation'] = [self.clean_text(line) for line in adapter['Translation']]

        return adapter.item

    def clean_text(self, text):
        if not isinstance(text, str):
            return text
        text = re.sub(r'^\\?"', '', text)  
        text = re.sub(r'\\"', '"', text)   
        text = text.replace('\"', '')      
        text = re.sub(r"[\u200c\u200b\xa0]", ' ', text) 
        text = re.sub(r"\s+", ' ', text)
        return text.strip()

    def extract_digits(self, text):
        if not isinstance(text, str):
            return text
        return ''.join(re.findall(r'\d+', text))  # Extract digits like '02' from 'a02 and'
