# Standard
import csv
import re
import time

from typing import Dict, List, Tuple

# Pip
import typer


# Custom
# None

# Regex var
RE_ENGLISH = re.compile(r"[A-Za-z]+")
RE_JAPANESE = re.compile(
    r"[\d+\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF\uFF66"
    r"-\uFF9F\("
    r"\)\uFF08\uFF09ー]+"
)
RE_PARENTHESIS = re.compile(r"[（(]([^（）()]+)[）)]")
WAITING_TIME = 0


class JapaneseTemplateParser:
    """
    A parser for Japanese lesson notes formatted in a specific template.

    This class reads and parses notes taken during Japanese lessons, extracting
    various types of content such as nouns, verbs, adjectives, and example sentences.

    Attributes:
        note_file (str): The file path of the note template.
        template (str): The content of the note template file.
        date (str): The date associated with the notes.
    """

    def __init__(self, note_file: str, date: str):
        """
        Initializes the JapaneseTemplateParser with a note file and date.

        Args:
            note_file (str): The file path to the note template.
            date (str): The date associated with the notes.
        """
        self.note_file = note_file
        self.template = self._open_template()
        self.date = date
        self.outgoing = note_file.replace("incoming", "outgoing").replace(".md", "")

    def _open_template(self) -> str:
        """
        Opens and reads the note template file.

        Returns:
            str: The content of the note template file.
        """
        with open(self.note_file, mode="r", encoding="utf-8") as incoming_file:
            data = incoming_file.read()
            typer.echo(f"File {self.note_file} opened.")
            return data

    def __field_parser(
        self, field_number: int = 1
    ) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """
        Parses a specific field in the note template.

        Args:
            field_number (int): The index of the field to be parsed.

        Returns:
            dict: A dictionary with the header as the key and the parsed content as the value.
            :param field_number:
            :return:
        """

        template_split = self.template.split("##")

        header, content = template_split[field_number].split("---")

        parsing_results = dict()

        for row in content.split("-"):

            japanese, english = RE_JAPANESE.findall(row), RE_ENGLISH.findall(row)
            if japanese or english:
                kanji = RE_PARENTHESIS.sub("", "".join(japanese))
                reading = RE_PARENTHESIS.findall("".join(japanese))
                parsing_results[kanji] = "".join(reading), " ".join(english)

        words = [word for word in parsing_results]

        typer.echo(f"##{header.strip()}: {len(words)}")
        time.sleep(WAITING_TIME)
        for i in parsing_results:

            if i:
                print("\t" + i, *parsing_results.get(i))
        else:
            typer.echo("/")

        template_results = {header.strip(): parsing_results}
        return template_results

    def __pack_parsed_data(
        self, content: Dict[str, Dict[str, Tuple[str, str]]], header: str, type: str
    ) -> List[Tuple[str, str, str, str]]:
        """
        Packs the parsed data into a list suitable for CSV writing.

        Args:
            content (dict): The parsed content.
            header (str): The header of the content.
            type (str): The type of the content (e.g., noun, verb).

        Returns:
            list: A list of tuples with parsed content.
        """
        date = self.date.replace(".md","")

        content_results = list()

        for kanji in content.get(header):
            reading, english = content.get(header).get(kanji)

            content_results.append(
                (kanji, reading, english, f"JA::ITALKI::NAOKO::{date}::{type} JA::ITALKI::NAOKO::{type}")
            )

        return content_results

    def get_verb_content(self) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """
        Retrieves and parses verb content from the note template.

        Returns:
            dict: The parsed verb content.
        """
        verb_content = self.__field_parser(6)
        return verb_content

    def get_noun_content(self) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """
        Retrieves and parses noun content from the note template.

        Returns:
            dict: The parsed noun content.
        """

        noun_content = self.__field_parser(4)

        return noun_content

    def get_i_adjective_content(self) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """
        Retrieves and parses i-adjective content from the note template.

        Returns:
            dict: The parsed i-adjective content.
        """
        i_adjective_content = self.__field_parser(5)
        return i_adjective_content

    def get_adjectival_nouns(self) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """
        Retrieves and parses adjectival noun content from the note template.

        Returns:
            dict: The parsed adjectival noun content.
        """
        adjectival_nouns_content = self.__field_parser(7)
        return adjectival_nouns_content

    def get_example_sentences(self) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """
        Retrieves and parses example sentences from the note template.

        Returns:
            dict: The parsed example sentences.
        """
        example_sentences_content = self.__field_parser(10)

        return example_sentences_content

    def get_expressions(self) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """
        Retrieves and parses expressions from the note template.

        Returns:
            dict: The parsed expressions.
        """
        expressions_content = self.__field_parser(11)

        return expressions_content

    def get_onomatopoeia(self) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """
        Retrieves and parses onomatopoeia from the note template.

        Returns:
            dict: The parsed onomatopoeia.
        """

        onomatopoeia_content = self.__field_parser(9)
        return onomatopoeia_content

    def get_grammar(self) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """
        Retrieves and parses grammar notes from the note template.

        Returns:
            dict: The parsed grammar notes.
        """
        grammar_content = self.__field_parser(12)
        return grammar_content

    def get_miscellaneous(self) -> Dict[str, Dict[str, Tuple[str, str]]]:
        """
        Retrieves and parses miscellaneous notes from the note template.

        Returns:
            dict: The parsed miscellaneous notes.
        """
        miscellaneous_content = self.__field_parser(13)
        return miscellaneous_content

    def generate_csv_file(self) -> None:
        """
        Generates a CSV file with the parsed content from the note template.
        """
        typer.echo("Parsing template data....")
        time.sleep(WAITING_TIME)

        typer.echo("The results are as follows....")
        # Nouns
        nouns = self.get_noun_content()
        noun_results = self.__pack_parsed_data(nouns, "名詞", "名詞")

        # Verbs
        verbs = self.get_verb_content()
        verb_results = self.__pack_parsed_data(verbs, "動詞", "動詞")

        # Adjectives
        i_adjectives = self.get_i_adjective_content()
        i_adjective_results = self.__pack_parsed_data(i_adjectives, "形容詞", "形容詞")

        # Adjectival Nouns
        adjectival_nouns = self.get_adjectival_nouns()
        adjectival_nouns_results = self.__pack_parsed_data(
            adjectival_nouns, "形容動詞", "形容動詞"
        )

        # Example sentences
        example_sentences = self.get_example_sentences()
        example_sentences_results = self.__pack_parsed_data(
            example_sentences, "例文", "例文"
        )

        # Expressions
        expressions = self.get_expressions()
        expression_results = self.__pack_parsed_data(expressions, "表現", "表現")

        # Onomatopoeia
        onomatopoeia = self.get_onomatopoeia()

        onomatopoeia_results = self.__pack_parsed_data(
            onomatopoeia, "オノマトペ", "オノマトペ"
        )

        # Grammar
        grammar = self.get_grammar()

        grammar_results = self.__pack_parsed_data(grammar, "文法", "文法")

        # Miscellaneous
        miscellaneous = self.get_miscellaneous()
        miscellaneous_results = self.__pack_parsed_data(miscellaneous, "雑記", "雑記")

        with open(f"{self.outgoing}.csv", "w", encoding="utf-8") as outfile:
            csv_writer = csv.writer(outfile)

            template_results = (
                noun_results,
                i_adjective_results,
                verb_results,
                adjectival_nouns_results,
                expression_results,
                example_sentences_results,
                onomatopoeia_results,
                grammar_results,
                miscellaneous_results,
            )
            # Header

            csv_writer.writerow(["Target Word", "Notes", "Definitions", "Tags"])

            for res in template_results:
                csv_writer.writerows(res)

        time.sleep(WAITING_TIME)
        typer.echo(f"Data successfully parsed and saved to '{self.outgoing}'")


if __name__ == "__main__":
    file_name = "incoming/incoming.md"

    parser = JapaneseTemplateParser(note_file=file_name, date="12.11.2024")
    parser.generate_csv_file()
