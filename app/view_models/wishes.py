from app.view_models.book import BookViewBodel

class myWishes():
    def __init__(self, wishes_of_mine, giftCount) -> None:
        self._wishes_of_mine = wishes_of_mine
        self._giftCount = giftCount
        self.wishes = self._parse()

    def _parse(self):
        temp_wish = []
        for wish in self._wishes_of_mine:
            wishes = self._maching(wish)
            temp_wish.append(wishes)
        return temp_wish
    
    def _maching(self, wish):
        count = 0
        for giftcount in self._giftCount:
            if giftcount['isbn'] == wish.isbn:
                count = giftcount['count']
                bookview = BookViewBodel(wish.book)
        r = {
            'wishes_count' : count,
            'book': bookview
        }
        return r
                


