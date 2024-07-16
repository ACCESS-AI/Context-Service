import os

CONFIG_PATH = "app/config.yaml"
CONNECTION_ARGS = "connection_args"

EMBEDDER_KEY = "embedder"
VECTORSTORE_KEY = "vectorstore"

ASSIGNMENT_START = "start"
ASSIGNMENT_END = "end"
ASSIGNMENTS_KEY = "assignments"

CONTEXT_FOLDER = "context"


COURSE_FOLDER_NAME_KEY = "course"
COURSE_SLUG_KEY = "slug"
COURSES_PATH = os.getenv('WORKDIR_INTERNAL', '/usr/data') + "/courses/"
 