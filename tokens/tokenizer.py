import json
from typing import List
from tokens.bookTokenNode import BookTokenNode

class Tokenizer:
    def __init__(self) -> None:
        """
        Load and parse the Bible from data/KJV.json
        """

        # Load the Bible
        self.bible_df = self.load_Bible()
        self.parsed_verses = self.parse_verses()

        # Book name bookings between format in JSON and txt data files
        self.book_name_mapping = {
            'Gen': 'Genesis',
            'Exod': 'Exodus',
            'Lev': 'Leviticus',
            'Num': 'Numbers',
            'Deut': 'Deuteronomy',
            'Josh': 'Joshua',
            'Judg': 'Judges',
            'Ruth': 'Ruth',
            '1Sam': 'I Samuel',
            '2Sam': 'II Samuel',
            '1Kgs': 'I Kings',
            '2Kgs': 'II Kings',
            '1Chr': 'I Chronicles',
            '2Chr': 'II Chronicles',
            'Ezra': 'Ezra',
            'Neh': 'Nehemiah',
            'Esth': 'Esther',
            'Job': 'Job',
            'Ps': 'Psalms',
            'Prov': 'Proverbs',
            'Eccl': 'Ecclesiastes',
            'Song': 'Song of Solomon',
            'Isa': 'Isaiah',
            'Jer': 'Jeremiah',
            'Lam': 'Lamentations',
            'Ezek': 'Ezekiel',
            'Dan': 'Daniel',
            'Hos': 'Hosea',
            'Joel': 'Joel',
            'Amos': 'Amos',
            'Obad': 'Obadiah',
            'Jonah': 'Jonah',
            'Mic': 'Micah',
            'Nah': 'Nahum',
            'Hab': 'Habakkuk',
            'Zeph': 'Zephaniah',
            'Hag': 'Haggai',
            'Zech': 'Zechariah',
            'Mal': 'Malachi',
            'Matt': 'Matthew',
            'Mark': 'Mark',
            'Luke': 'Luke',
            'John': 'John',
            'Acts': 'Acts',
            'Rom': 'Romans',
            '1Cor': 'I Corinthians',
            '2Cor': 'II Corinthians',
            'Gal': 'Galatians',
            'Eph': 'Ephesians',
            'Phil': 'Philippians',
            'Col': 'Colossians',
            '1Thess': 'I Thessalonians',
            '2Thess': 'II Thessalonians',
            '1Tim': 'I Timothy',
            '2Tim': 'II Timothy',
            'Titus': 'Titus',
            'Phlm': 'Philemon',
            'Heb': 'Hebrews',
            'Jas': 'James',
            '1Pet': 'I Peter',
            '2Pet': 'II Peter',
            '1John': 'I John',
            '2John': 'II John',
            '3John': 'III John',
            'Jude': 'Jude',
            'Rev': 'Revelation of John'
        }

        # Store cross references
        self.cross_references = self.connect_cross_references()

        # Create the token nodes
        self.token_nodes = self.create_token_nodes()

    def load_Bible(self) -> dict:
        """
        Load the Bible from data/KJV.json
        """

        with open("data/KJV.json", "r") as bible_file:
            bible_data = json.load(bible_file)

        return bible_data
    
    def parse_verses(self) -> dict[str, dict[str, str]]:
        """
        Parse the verses of the Bible

        Returns:
            dict[str, dict[str, str]]: A dictionary of verses with the format:
                            { "book_name": { "full_verse_name": "verse_text" } }
        """

        # Store the verses
        verses = {}
        
        """
        Layout of the Bible JSON:
            self.bible_df["books"][book_number]["chapters"][chapter_number]["verses"][verse_number]

        Layout of each verse:
            verse -> {verse, chapter, name, text}
        """
        for book in self.bible_df["books"]:
            # Store the verses of the book
            book_tokens = {}

            # Store the verses of the chapters
            for chapter in book["chapters"]:
                # Store the verses of the chapter
                for verse in chapter["verses"]:
                    book_token_key = verse["name"]
                    book_tokens[book_token_key] = verse["text"]

            verses[book["name"]] = book_tokens

        return verses
    
    def connect_cross_references(self) -> None:
        """
        Connect the cross references of the Bible by connecting each verse
        to all of its cross references
        """

        # Create a dictionary to store the cross references
        stored_references = {}

        with open("data/cross_references.txt", "r") as cross_references_file:
            # Skip the header line
            cross_references_file.readline()

            # Read the rest of the file
            cross_references = cross_references_file.read().strip().split("\n")

            for cross_reference in cross_references:
                verse, reference, votes = cross_reference.strip().split("\t")

                # Store references in case there is a list of references
                references = []

                # Filter out verses with no votes or negative votes
                if votes == "0" or int(votes) < 0:
                    continue

                # Convert verse format
                verse_book_name, verse_chapter_number, verse_verse_number = verse.split(".")
                verse_book_name = self.book_name_mapping[verse_book_name]
                converted_verse_name = f"{verse_book_name} {verse_chapter_number}:{verse_verse_number}"

                # Check if the reference is a range
                if "-" not in reference:
                    # Convert reference as a single verse
                    reference_book_name, reference_chapter_number, reference_verse_number = reference.split(".")
                    reference_book_name = self.book_name_mapping[reference_book_name]
                    converted_reference_name = f"{reference_book_name} {reference_chapter_number}:{reference_verse_number}"

                    # Add the reference to the list
                    references.append(converted_reference_name)
                else:
                    # Convert reference as a range
                    start_reference, end_reference = reference.split("-")
                    start_info = start_reference.split(".")
                    end_info = end_reference.split(".")

                    # Book and chapter should be the same
                    reference_book_name, reference_chapter_number = start_info[0], start_info[1]

                    # Get the range of the verse numbers
                    start_verse_number = start_info[2]
                    end_verse_number = end_info[2]
                    range_of_verse_numbers = range(int(start_verse_number), int(end_verse_number) + 1)

                    # Add the references to the list
                    for verse_number in range_of_verse_numbers:
                        converted_reference_book_name = self.book_name_mapping[reference_book_name]
                        converted_reference_name = f"{converted_reference_book_name} {reference_chapter_number}:{verse_number}"
                        references.append(converted_reference_name)
                    
                # Store the cross reference
                if converted_verse_name not in stored_references:
                    stored_references[converted_verse_name] = []

                for reference in references:
                    if reference not in stored_references[converted_verse_name]:
                        stored_references[converted_verse_name].append(reference)

        return stored_references
    
    def create_token_nodes(self) -> List[BookTokenNode]:
        """
        Create the Bible book token nodes

        Returns:
            List[BookTokenNode]: A list of BookTokenNode objects
        """
        token_nodes = []

        # Loop through each book
        for book_name in self.parsed_verses.keys():
            book_verses = self.parsed_verses[book_name]

            # Loop through each verse
            for verse_name, verse_text in book_verses.items():
                # Get the chapter and verse numbers
                verse_info = verse_name.split(" ")
                chapter_number = int(verse_info[-1].split(":")[0])
                verse_number = int(verse_info[-1].split(":")[1])

                # Get the verse text
                verse_text = verse_text.strip()

                # Get the references
                if verse_name in self.cross_references:
                    references = self.cross_references[verse_name]
                else:
                    references = []

                # Create the book token node
                book_token_node = BookTokenNode(book_name, chapter_number, verse_number, verse_text, references)
                token_nodes.append(book_token_node)

        return token_nodes
    
Tokenizer()
