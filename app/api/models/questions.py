from app import generate_id

qtns_list = []
qtn_id = generate_id(qtns_list)

class Question:
    
    """Model to fine the structure of a user Question"""

    def __init__(self, user_id, title, subject, qtn_desc):
        self.qtn_id = generate_id(qtns_list)
        self.title = title
        self.subject = subject
        self.qtn_desc = qtn_desc
