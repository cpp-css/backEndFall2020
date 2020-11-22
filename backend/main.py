import os
from random import shuffle
from config import app, db, GIT_COMMIT, VERSION
import api.organization
import api.user
import api.admin
import api.event
import error.http
import error.internal

authors = [
    {'name': 'Josh Garde', 'email': 'jagarde@cpp.edu', 'github': '@joshgarde'},
    {'name': 'Matthew Tootoonchi', 'github': '@mtootoonchi'},
    {'name': 'Dai Vuong', 'github': '@paulminhdai'},
    {'name': 'Phuong Nguyen', 'github': '@pnguyen-16'},
    {'name': 'Daeyoung Hwang', 'github': '@dyhwang7'},
    {'name': 'Khuong Le', 'github': 'lekhuong07'}
]

@app.route('/')
def hello_world():
    '''
    Get the application's version string
    ---
    responses:
        200:
            description: OK
            schema:
                type: object
                properties:
                    version:
                        type: string
                        description: A SEMVER version string that includes the git HEAD
                    authors:
                        type: array
                        description: The people behind the magic
                        items:
                            type: object
                            properties:
                                name:
                                    type: string
                                github:
                                    type: string
                                email:
                                    type: string
                    quote:
                        type: string
    '''
    shuffle(authors)

    return {
        'version': '{version}-{commit}'.format(version=VERSION, commit=GIT_COMMIT),
        'authors': authors,
        'quote': 'Written by the CSSPI Fall 2020 backend team'
    }

if __name__ == "__main__":
    port = os.getenv("PORT", 9090)
    app.run(host="localhost", port=port, threaded=True, debug=True)
