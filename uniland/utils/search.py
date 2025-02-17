class SubmissionRecord:
    """
    Represents a submission record.

    Attributes:
        id (int): The ID of the submission.
        search_text (str): The search text associated with the submission.
        type (str): The type of the submission.
        likes (int): The number of likes the submission has received.
        search_times (int, optional): The number of times the submission has been searched. Defaults to 0.
    """

    def __init__(
        self, id: int, search_text: str, type: str, likes: int, search_times: int = 0
    ):
        self.id = id
        self.search_text = search_text
        self.type = type
        self.likes = likes
        self.search_times = search_times

    def __repr__(self):
        return str(
            {
                "id": self.id,
                "search_text": self.search_text,
                "type": self.type,
                "likes": self.likes,
            }
        )


# -----------------------------------------------------------------------


class SearchEngine:
    """
    A class representing a search engine for indexing and searching records.

    Attributes:
        alts (dict): A dictionary mapping alternative characters to their replacements.
        subs (dict): A dictionary mapping record IDs to record objects.
        keywords (dict): A dictionary mapping keywords to sets of record IDs.
        total_searches (int): The total number of searches performed.

    Methods:
        __init__: Initializes a new instance of the SearchEngine class.
        __clean_text: Cleans the given text by replacing alternative characters and removing unnecessary spaces.
        index_record: Indexes a new record in the search engine.
        update_record: Updates an existing record in the search engine.
        increase_likes: Increases the number of likes for a record.
        decrease_likes: Decreases the number of likes for a record.
        get_likes: Returns the number of likes for a record.
        increase_search_times: Increases the search times for a record.
        total_confirmed_subs: Returns the total number of confirmed records.
        remove_record: Removes a record from the search engine.
        search: Performs a search based on the given search text.
        __repr__: Returns a string representation of the SearchEngine object.
    """

    alts = {
        "ي": "ی",
        "ك": "ک",
        "ة": "ه",
        "آ": "ا",
        "أ": "ا",
        "إ": "ا",
        "ئ": "ی",
        "ؤ": "و",
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
        "۰": "0",
        " یک ": " 1 ",
        " دو ": " 2 ",
        " سه ": " 3 ",
        " چهار ": " 4 ",
        " پنج ": " 5 ",
        " شش ": " 6 ",
        " هفت ": " 7 ",
        " هشت ": " 8 ",
        " نه ": " 9 ",
        " صفر ": " 0 ",
        ",": " ",
        "،": " ",
        "#": " ",
        "-": " ",
        "_": " ",
        ":": " ",
        "ایمیل": "اطلاعات",
        "شماره": "اطلاعات",
        "پروفایل": "اطلاعات",
        "ن‌ن"[1]: " ",  # Nim Fasele:)
    }

    def __init__(self):
        """
        Initialize the Search class.

        The Search class is responsible for managing search functionality.

        Attributes:
        - subs: A dictionary mapping integer IDs to Record objects.
        - keywords: A dictionary mapping string keywords to sets of integer IDs.
        - total_searches: An integer representing the total number of searches performed.
        """
        self.subs = {}  # int id -> Record record
        self.keywords = {}  # str keyword -> set of int ids
        self.total_searches = 0

    def __clean_text(self, text: str):
        """
        Cleans the given text by removing leading/trailing spaces, replacing alternative characters,
        and converting it to lowercase.

        Args:
            text (str): The text to be cleaned.

        Returns:
            str: The cleaned text.
        """
        text = " " + text + " "

        for key, value in self.alts.items():
            text = text.replace(key, value)

        text = " ".join(text.split())

        return text.strip().lower()

    def index_record(
        self,
        id: int,
        search_text: str,
        sub_type: str,
        likes: int = 0,
        search_times: int = 0,
    ):
        """
        Indexes a record for searching.

        Args:
            id (int): The ID of the record.
            search_text (str): The text to be indexed for searching.
            sub_type (str): The subtype of the record.
            likes (int, optional): The number of likes for the record. Defaults to 0.
            search_times (int, optional): The number of times the record has been searched. Defaults to 0.
        """
        self.total_searches += search_times

        search_text = self.__clean_text(search_text)

        if search_text is None:
            self.subs[id] = SubmissionRecord(
                id, search_text="", type=sub_type.strip(), likes=likes
            )
            return

        record = SubmissionRecord(
            id, search_text=search_text, type=sub_type.strip(), likes=likes
        )

        self.subs[id] = record

        for word in search_text.split():
            if word not in self.keywords:
                self.keywords[word] = set()

            self.keywords[word].add(record)

    def update_record(
        self, id: int, search_text: str = None, sub_type: str = None, likes: int = -1
    ):
        """
        Updates the specified record with the given parameters.

        Args:
            id (int): The ID of the record to be updated.
            search_text (str, optional): The new search text for the record. Defaults to None.
            sub_type (str, optional): The new sub type for the record. Defaults to None.
            likes (int, optional): The new number of likes for the record. Defaults to -1.
        """
        record = self.remove_record(id)

        record.search_text = record.search_text if search_text is None else search_text

        record.type = record.type if sub_type is None else sub_type

        record.likes = record.likes if likes == -1 else likes

        self.index_record(record.id, record.search_text, record.type, record.likes)

    def increase_likes(self, id: int):
        """
        Increases the number of likes for a specific subscription.

        Args:
            id (int): The ID of the subscription to increase the likes for.
        """
        self.subs[id].likes += 1

    def decrease_likes(self, id: int):
        """
        Decreases the number of likes for a specific item.

        Args:
            id (int): The ID of the item to decrease the likes for.
        """
        self.subs[id].likes -= 1

    def get_likes(self, id: int):
        """
        Returns the number of likes for a given ID.

        Args:
            id (int): The ID of the item.

        Returns:
            int: The number of likes for the item. Returns 0 if the ID is not found.
        """
        if id not in self.subs:
            return 0
        return self.subs[id].likes

    def increase_search_times(self, id: int):
        """
        Increases the search times for a specific ID and updates the total number of searches.

        Args:
            id (int): The ID of the item to increase the search times for.
        """
        self.subs[id].search_times += 1
        self.total_searches += 1

    @property
    def total_confirmed_subs(self):
        return len(self.subs)

    def remove_record(self, id: int):
        """
        Removes a record from the search database based on the given ID.

        Args:
            id (int): The ID of the record to be removed.

        Returns:
            record: The removed record.

        """
        record = self.subs.pop(id)

        self.total_searches -= record.search_times

        search_text = record.search_text

        for word in search_text.split():
            if word in self.keywords:
                self.keywords[word].discard(record)

                if len(self.keywords[word]) == 0:
                    del self.keywords[word]

        return record

    def search(self, search_text: str):
        """
        Search for keywords in the given search text and return the sorted results.

        Args:
            search_text (str): The text to search for keywords.

        Returns:
            tuple: A tuple containing a boolean value indicating whether any ignored keywords were found,
                   and a sorted list of results based on the number of likes in descending order.
        """
        search_text = self.__clean_text(search_text)

        result = set()

        first_flag = True
        ignored_keyword = False

        for word in search_text.split():
            if word in self.keywords:
                if not first_flag:
                    result = result.intersection(self.keywords[word])
                else:
                    result = self.keywords[word]
                    first_flag = False
            else:
                ignored_keyword = True

        return (ignored_keyword, sorted(result, key=lambda x: x.likes, reverse=True))

    def __repr__(self):
        return f"SearchEngine with {len(self.subs)} records and {len(self.keywords)} keywords"
