import nltk 
import json
nltk.download('punkt_tab')
mahabharata = "mahabharataScrapy/mahabharataScrapy/spiders/parava.json"
with open(mahabharata,'r') as f:
    mahabharata = json.load(f)

new_json_mahabharata = []

for mahabharat in mahabharata:
    # print(mahabharat['Translation'])
    the_translation = mahabharat.get("Translation","")
    the_translation = "".join(the_translation)
    new_sentences = nltk.sent_tokenize(the_translation)
    for new_sentence in new_sentences:
        new_json_mahabharata.append({
                                    "Book":mahabharat.get("Book",""),
                                    "Section":mahabharat.get("Section",""),
                                    "Translation":new_sentence})      

output_file = "mahabharata_dataset.json"
with open(output_file, 'w') as f:
    json.dump(new_json_mahabharata, f, indent=4)