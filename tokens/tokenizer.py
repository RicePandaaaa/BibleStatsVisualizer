from tokens.bookTokenNode import BookTokenNode

import polars as pl

class Tokenizer:
    def __init__(self) -> None:
        """
        Load and parse the Bible from data/KJV.json
        """
        self.bible_df = self.load_Bible()
        self.book_names = [book["name"] for book in self.bible_df["books"]]

    def load_Bible(self) -> pl.DataFrame:
        """
        Load the Bible from data/KJV.json
        """

        bible_df = pl.read_json("data/KJV.json")
        return bible_df