class PredictionFailed(Exception):
    def __init__(self, msg):
        self.msg = msg

    def get_error_msg(self):
        return self.msg
