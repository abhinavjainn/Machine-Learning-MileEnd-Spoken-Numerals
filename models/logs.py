from db import db

# Database table: logs
class LogsModel(db.Model):
    __tablename__ = 'logs'

    # Declare table columns
    guid           = db.Column(db.String(36), primary_key=True)
    data_in        = db.Column(db.String(5000))    
    prediction_num = db.Column(db.Integer())
    prediction_str = db.Column(db.String(20))
    date           = db.Column(db.String(20))
    time           = db.Column(db.String(20))
    timezone       = db.Column(db.String(10))

    # Constructor for table instance
    def __init__(self, guid, data_in=None, prediction_num=None, 
                    prediction_str=None, date=None, time=None, timezone=None):
        self.guid           = guid
        self.data_in        = data_in
        self.prediction_num = prediction_num
        self.prediction_str = prediction_str
        self.date           = date
        self.time           = time
        self.timezone       = timezone

    # Save data in table
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
