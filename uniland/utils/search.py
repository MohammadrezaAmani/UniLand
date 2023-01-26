class SubmissionRecord:

  def __init__(self,
               id: int,
               search_text: str,
               type: str,
               likes: int,
               search_times: int = 0):
    self.id = id
    self.search_text = search_text
    self.type = type
    self.likes = likes
    self.search_times = search_times

  def __repr__(self):

    return str({
      "id": self.id,
      "search_text": self.search_text,
      "type": self.type,
      "likes": self.likes,
    })


# -----------------------------------------------------------------------


class SearchEngine:

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
    "ن‌ن"[1] : " " # Nim Fasele:)
  }

  def __init__(self):

    self.subs = {}  # int id -> Record record

    self.keywords = {}  # str keyword -> set of int ids

    self.total_searches = 0

  def __clean_text(self, text: str):

    text = ' ' + text + ' '

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

    self.total_searches += search_times

    search_text = self.__clean_text(search_text)

    if search_text is None:
      self.subs[id] = SubmissionRecord(id,
                                       search_text='',
                                       type=sub_type.strip(),
                                       likes=likes)
      return

    record = SubmissionRecord(id,
                              search_text=search_text,
                              type=sub_type.strip(),
                              likes=likes)

    self.subs[id] = record

    for word in search_text.split():

      if word not in self.keywords:

        self.keywords[word] = set()

      self.keywords[word].add(record)

  def update_record(self,
                    id: int,
                    search_text: str = None,
                    sub_type: str = None,
                    likes: int = -1):

    record = self.remove_record(id)

    record.search_text = record.search_text if search_text is None else search_text

    record.type = record.type if sub_type is None else sub_type

    record.likes = record.likes if likes == -1 else likes

    self.index_record(record.id, record.search_text, record.type, record.likes)

  def increase_likes(self, id: int):
    self.subs[id].likes += 1

  def decrease_likes(self, id: int):
    self.subs[id].likes -= 1

  def get_likes(self, id: int):
    if not id in self.subs:
      return 0
    return self.subs[id].likes

  def increase_search_times(self, id: int):
    self.subs[id].search_times += 1
    self.total_searches += 1

  @property
  def total_confirmed_subs(self):
    return len(self.subs)

  def remove_record(self, id: int):

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

    return (ignored_keyword, sorted(result,
                                    key=lambda x: x.likes,
                                    reverse=True))

  def __repr__(self):

    return f"SearchEngine with {len(self.subs)} records and {len(self.keywords)} keywords"
