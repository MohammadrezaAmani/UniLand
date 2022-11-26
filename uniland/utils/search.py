
class Record():
    
    def __init__(self, id:int, search_text:str, type:str, likes:int):
        self.id = id
        self.search_text = search_text
        self.type = type
        self.likes = likes
        
    def __repr__(self):
        return str({'id':self.id,
                    'search_text':self.search_text,
                    'type':self.type,
                    'likes':self.likes})

class SearchEngine():
    
    alts = {
        'ي': 'ی',
        'ك': 'ک',
        'ة': 'ه',
        'أ': 'ا',
        'إ': 'ا',
        'ئ': 'ی'
    }
    
    def __init__(self):
        self.subs = {} # int id -> Record record
        self.keywords = {} # str keyword -> set of int ids
        
    def __clean_text(self, text:str):
        for key, value in self.alts.items():
            text = text.replace(key, value)
        return text.strip()
    
    def index_record(self, id:int, search_text:str, sub_type:str, likes:int = 0):
        
        search_text = self.__clean_text(search_text)
        
        record = Record(id, search_text=search_text, type=sub_type.strip(), likes=likes)
        
        self.subs[id] = record
            
        for word in search_text.split():
            if word not in self.keywords:
                self.keywords[word] = set()
            self.keywords[word].add(record)
            
    def increase_likes(self, id:int):
        record = self.subs[id]
        record.likes += 1
        
    def decrease_likes(self, id:int):
        record = self.subs[id]
        record.likes -= 1
    
    def remove_record(self, id:int):
        record = self.subs.pop(id)
        
        search_text = record.search_text
         
        for word in search_text.split():
            if word in self.keywords:
                self.keywords[word].remove(record)
                if len(self.keywords[word]) == 0:
                    del self.keywords[word]
    
    def search(self, search_text:str):
        search_text = self.__clean_text(search_text)
        
        result = set()
        first_flag = True
        for word in search_text.split():
            if word in self.keywords:
                if not first_flag:
                    result = result.intersection(self.keywords[word])
                else:
                    result = self.keywords[word]
                    first_flag = False
                    
        return sorted(result, key=lambda x: x.likes, reverse=True)
    
    def __repr__(self):
        return f"SearchEngine with {len(self.subs)} records and {len(self.keywords)} keywords"
