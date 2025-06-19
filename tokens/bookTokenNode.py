class BookTokenNode:
    def __init__(self, book_name, chapter_number, verse_number, verse_text, references):
        """
        A node consisting of a verse of the Bible
        and its information and references

        Args:
            book_name (str): The name of the book
            chapter_number (int): The chapter number
            verse_number (int): The verse number
            verse_text (str): The verse text
            references (list): A list of references to the verse
        """
        self.book_name = book_name
        self.chapter_number = chapter_number
        self.verse_text = verse_text
        self.verse_number = verse_number
        self.references = references

    def __str__(self) -> str:
        """
        Return the string representation of the book token node
        """
        return f"{self.book_name} {self.chapter_number}:{self.verse_number}\nReferences: {"\n- ".join(self.references)}"
    
    def __repr__(self) -> str:
        """
        Return the string representation of the book token node
        """
        return self.__str__()
        