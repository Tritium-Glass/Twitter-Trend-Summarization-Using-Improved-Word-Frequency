import datetime

class article:
    def __init__(self,url='',text='',date=datetime.datetime.now(),keywords=[]):
        self.url = url
        self.text = text
        self.datetime = date
        keywords = []
