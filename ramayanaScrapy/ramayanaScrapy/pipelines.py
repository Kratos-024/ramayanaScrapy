from itemadapter import ItemAdapter
import re

class RamayanascrapyPipeline:
    def process_item(self, item, spider):
        if 'Translation' in item:
            item['Translation'] = self.remove_extra_char(item['Translation'])
        return item

    def remove_extra_char(self, text):
        cleaned = re.sub(r'[\n\t\\\"]', ' ', text)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = re.sub(r'\[\d{1,2}-\d{1,2}-\d{1,2}\]', '', cleaned)

        return cleaned.strip()
