from app.libs.enums import PendingStatus


class DriftViewModel:
    def __init__(self, drift, current_user_id):
        self.recipient_name = drift.recipient_name
        self.address = drift.address
        self.message = drift.message
        self.mobile = drift.mobile
        self.book_title = drift.book_title
        self.book_author = drift.book_author
        self.book_img = drift.book_img
        self.data = drift.create_datatime.strftime('%Y-%m-%d')
        self.requestr_id = drift.requestr_id
        self.you_are = self.is_requester(current_user_id)
        self.status = drift.pending
        self.drift_id = drift.id
        self.operator = drift.requester_nicname if self.you_are == 'requester' \
            else drift.gifter_nickname
        self.status_str = PendingStatus.pending_status(drift.pending, self.you_are)
    

    
    def is_requester(self, current_user_id):
        if self.requestr_id == current_user_id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are


class DriftCollection:
    def __init__(self, drifts, current_user_id):
        self.data = []
        self._parse(drifts, current_user_id)
    
    def _parse(self, drifts, current_user_id):
        self.data = [DriftViewModel(drift,current_user_id) for drift in drifts]
