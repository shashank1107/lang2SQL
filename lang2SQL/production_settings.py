import os
import dj_database_url

# DATABASE
DATABASES = dict()
DATABASES['default'] = dj_database_url.parse(os.environ['DATABASE_URL'])
