from typing import List
import toml
from app.model.core.assignment_context import AssignmentContext
from app.model.utils.constants import ASSIGNMENT_START, ASSIGNMENT_END, ASSIGNMENTS_KEY, COURSES_PATH

class RepositoryHandler:

    def __init__(self, folder_name:str, course_path: str= COURSES_PATH) -> None:
        self.__directory_name = folder_name
        self.__assignments = []
        self.__course_path = course_path

    def get_assignment_contexts(self) -> List[AssignmentContext]:
        self.__assignments = []
        with open( self.__course_path + self.__directory_name + "/config.toml", "r") as file: 
            toml_content = file.read()
        assignment_names = toml.loads(toml_content)[ASSIGNMENTS_KEY]
        for assignment_name in assignment_names:
            with open( self.__course_path + self.__directory_name + "/" + assignment_name + "/" + "config.toml", "r") as file:
                toml_parsed = toml.loads(file.read())
                start_timestamp = int(toml_parsed[ASSIGNMENT_START].timestamp() * 1000)
                end_timestamp = int(toml_parsed[ASSIGNMENT_END].timestamp() * 1000)
                metadata = {ASSIGNMENT_START: start_timestamp, 
                                    ASSIGNMENT_END: end_timestamp}
                self.__assignments.append(AssignmentContext(self.__course_path + self.__directory_name + "/" + assignment_name, metadata=metadata ))
        return self.__assignments