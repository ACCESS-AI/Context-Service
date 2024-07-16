
from app.model.utils.constants import COURSE_FOLDER_NAME_KEY, COURSE_SLUG_KEY

class PayloadParser:

    def __init__(self, payload: dict):
        self.payload = payload
    
    @property
    def folder_name(self):
        return self.payload.get(COURSE_FOLDER_NAME_KEY)  
    
    @property
    def course_slug(self):
        return self.payload.get(COURSE_SLUG_KEY)  

    

