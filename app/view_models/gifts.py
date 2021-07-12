from app.view_models.book import BookViewBodel
class MyGifts:
    def __init__(self, gifts_of_mine, wish_count_list):
        self._gift_of_mine = gifts_of_mine
        self._wish_count_list = wish_count_list
        self.gifts = self._parse()
    
    # 双重循环
    def _parse(self):
        temp_gifts = []
        for gift in self._gift_of_mine:
            my_gift = self._maching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts
    
    def _maching(self, gift):
        count = 0
        for wish_count in self._wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        r = {
            'wishes_count':count,
            'book': BookViewBodel(gift.book),
            'id': gift.id
        }
        return r