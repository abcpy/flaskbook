from app.models.base import Base
from app.view_models.book import BookViewBodel

class TradeInfo():
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self._prase(goods)

    def _prase(self, goods):
        self.total = len(goods)
        self.trades =  [self._map_to_trade(single) for single in goods]

    def _map_to_trade(self, single):
        if single.create_time:
            time = single.create_datatime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time = time,
            id = single.id
        )


"""
    gifts 和 wishes 的封装
"""
class MyTrade:
        def __init__(self, trades_of_mine, trade_count_list):
            self._trade_of_mine = trades_of_mine
            self._trade_count_list = trade_count_list
            self.trades = self._parse()
    
        # 双重循环
        def _parse(self):
            temp_trades = []
            for trade in self._trade_of_mine:
                my_trade = self._maching(trade)
                temp_trades.append(my_trade)
            return temp_trades
    
        def _maching(self, trade):
            count = 0
            for trade_count in self._trade_count_list:
                if trade.isbn == trade_count['isbn']:
                    count = trade_count['count']
            r = {
                'wishes_count':count,
                'book': BookViewBodel(trade.book),
                'id': trade.id
            }
            return r
        