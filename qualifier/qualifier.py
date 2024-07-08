from enum import auto, StrEnum
from warnings import warn


MAX_QUOTE_LENGTH = 50


# The two classes below are available for you to use
# You do not need to implement them
class VariantMode(StrEnum):
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()


class DuplicateError(Exception):
    """Error raised when there is an attempt to add a duplicate entry to a database"""


# Implement the class and function below
class Quote:
    def __init__(self, quote: str, mode: "VariantMode") -> None:
        self.quote = quote
        self.mode = mode
        self.transformed_quote = self._create_variant()

    def __str__(self) -> str:
        return self.transformed_quote

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """
        if self.quote[0] in '"“' and self.quote[-1] in '"”':
            quote = self.quote[1:-1]
        else:
            quote = self.quote

        if len(quote) > MAX_QUOTE_LENGTH:
            raise ValueError("Quote is too long")

        if self.mode == VariantMode.NORMAL:
            # Nothing to do for normal variant
            pass
        elif self.mode == VariantMode.UWU:
            is_transformable = False
            for val in ['L', 'l', 'R', 'r', ' U', ' u']:
                if val in quote:
                    is_transformable = True
            if not is_transformable:
                raise ValueError('Quote was not modified')
            quote = quote.replace('L', 'W')
            quote = quote.replace('l', 'w')
            quote = quote.replace('R', 'W')
            quote = quote.replace('r', 'w')
            quote_full = quote.replace(' U', ' U-U')
            quote_full = quote_full.replace(' u', ' u-u')
            if len(quote_full) > MAX_QUOTE_LENGTH:
                warn("Quote too long, only partially transformed")
            else:
                quote = quote_full
        elif self.mode == VariantMode.PIGLATIN:
            temp_quote = ''
            for word in quote.lower().split():
                if word[0] in 'aeiou':
                    temp_quote += f'{word}way '
                else:
                    for i, char in enumerate(word):
                        if char in 'aeiou':
                            temp_quote += f'{word[i:]}{word[:i]}ay '
                            break
            if len(temp_quote) > MAX_QUOTE_LENGTH:
                raise ValueError("Quote was not modified")
            quote = temp_quote.capitalize().strip()

        return quote


def run_command(command: str) -> None:
    """
    Will be given a command from a user. The command will be parsed and executed appropriately.

    Current supported commands:
        - `quote` - creates and adds a new quote
        - `quote uwu` - uwu-ifys the new quote and then adds it
        - `quote piglatin` - piglatin-ifys the new quote and then adds it
        - `quote list` - print a formatted string that lists the current
           quotes to be displayed in discord flavored markdown
    """
    database = Database()
    search_words = {1: 'quote ', 2: 'quote uwu ', 3: 'quote piglatin ', 4: 'quote list'}

    quote: str
    mode: VariantMode | None
    if command.startswith(search_words[2]):
        quote = command[len(search_words[2]):].strip()
        mode = VariantMode.UWU
    elif command.startswith(search_words[3]):
        quote = command[len(search_words[3]):].strip()
        mode = VariantMode.PIGLATIN
    elif command.startswith(search_words[4]):
        quote = command[len(search_words[4]):].strip()
        mode = None
    elif command.startswith(search_words[1]):
        # Normal quote must be checked last, otherwise all elifs would be skipped
        quote = command[len(search_words[1]):].strip()
        mode = VariantMode.NORMAL
    else:
        raise ValueError("Invalid command")

    if mode is not None:
        try:
            Database.add_quote(Quote(quote, mode))
        except DuplicateError:
            print("Quote has already been added previously")
    else:
        print('- ' + '\n- '.join(Database.get_quotes()))


# The code below is available for you to use
# You do not need to implement it, you can assume it will work as specified
class Database:
    quotes: list["Quote"] = []

    @classmethod
    def get_quotes(cls) -> list[str]:
        "Returns current quotes in a list"
        return [str(quote) for quote in cls.quotes]

    @classmethod
    def add_quote(cls, quote: "Quote") -> None:
        "Adds a quote. Will raise a `DuplicateError` if an error occurs."
        if str(quote) in [str(quote) for quote in cls.quotes]:
            raise DuplicateError
        cls.quotes.append(quote)
