
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
        self.subs = {}
    
    def index_record(self, id, search_text):
        for key, value in self.alts.items():
            search_text = search_text.replace(key, value)
            
        for word in search_text.split():
            if word not in self.subs:
                self.subs[word] = set()
            self.subs[word].add(id)
    
    def remove_record(self, id, search_text):
        for key, value in self.alts.items():
            search_text = search_text.replace(key, value)
            
        for word in search_text.split():
            if word in self.subs:
                self.subs[word].remove(id)
                if len(self.subs[word]) == 0:
                    del self.subs[word]
    
    def search(self, search_text):
        for key, value in self.alts.items():
            search_text = search_text.replace(key, value)
        
        # find all records with all keywords in search_text
        result = set()
        first_flag = True
        for word in search_text.split():
            if word in self.subs:
                if not first_flag:
                    result = result.intersection(self.subs[word])
                else:
                    result = self.subs[word]
                    first_flag = False
                    
