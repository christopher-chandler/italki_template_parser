# Standard
import csv
import re

# Pip
# Noun

# Custom
# None

re_english = re.compile(r'[A-Za-z]+')
re_japanese = re.compile(
    r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF\uFF66-\uFF9F\(\)\uFF08\uFF09ー]+')

re_parenthesis = re.compile(r'\(([^)]+)\)')


class TemplateParser:

    def __init__(self, file_name,date):
        self.file_name = file_name
        self.template = self._open_template()
        self.date = date

    def _open_template(self):
        with open(self.file_name, mode="r", encoding="utf-8") as incoming_file:
            data = incoming_file.read()
            return data

    def __field_parser(self, field_name):
        template_split = self.template.split("##")
        header, content = template_split[field_name].split("---")
        results = dict()

        for row in content.split("-"):
            jp, en = re_japanese.findall(row), re_english.findall(row)
            if jp or en:
                kanji = re_parenthesis.sub("", "".join(jp))
                reading = re_parenthesis.findall("".join(jp))
                results[kanji] = "".join(reading), " ".join(en)

        return {header.strip():results}

    def __pack_parsed_data(self, header):
        date = self.date
        nouns = self.get_noun_content()
        content_results = list()
        for kanji in nouns.get(header):
            reading, english = nouns.get(header).get(kanji)
            content_results.append(
                (kanji, reading, english, f"JA::ITALKI::NAOKO::{date}::Noun"))

        return content_results


    def get_verb_content(self):
            data = self.__field_parser(6)

            for row in data:
                print(row, data.get(row))

    def get_noun_content(self):
        data = self.__field_parser(4)

        return  data

    def get_i_adjective_content(self):
        data = self.__field_parser(5)
        for row in data:
            print(row, data.get(row))

    def get_adjectival_nouns(self):
        pass

    def get_example_senteces(self):
        data = self.__field_parser(10)
        for row in data:
            print(row, data.get(row))

    def get_expressions(self):
        data = self.__field_parser(11)
        for row in data:
            print(row, data.get(row))

    def get_onomatopoeia(self):
        pass
    def get_grammar(self):
        pass


    def get_miscellaneous(self):
        pass


    def generate_csv_file(self):

        nouns = self.__pack_parsed_data("名詞")

        with open("results.csv", "w", encoding="utf-8") as outfile:
            writer = csv.writer(outfile)



if __name__ == '__main__':
    file_name = "template.md"

    parser = TemplateParser(file_name)
    parsed_template = parser.generate_csv_file()

