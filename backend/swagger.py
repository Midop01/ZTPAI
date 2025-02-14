from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Social Media API"
    }
)

spec = APISpec(
    title="Social Media API",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
    info={
        'description': 'API dla aplikacji społecznościowej',
        'contact': {
            'email': 'twoj@email.com'
        }
    }
)

# Definicje schematów
spec.components.schema('User', {
    'properties': {
        'username': {'type': 'string', 'description': 'Nazwa użytkownika'},
        'email': {'type': 'string', 'format': 'email', 'description': 'Adres email'},
        'password': {'type': 'string', 'description': 'Hasło użytkownika'}
    },
    'required': ['username', 'email', 'password']
})

spec.components.schema('Post', {
    'properties': {
        'title': {'type': 'string', 'description': 'Tytuł posta'},
        'description': {'type': 'string', 'description': 'Treść posta'},
        'image_url': {'type': 'string', 'description': 'URL obrazka'}
    },
    'required': ['title', 'description']
})

spec.components.schema('Comment', {
    'properties': {
        'content': {'type': 'string', 'description': 'Treść komentarza'},
        'post_id': {'type': 'integer', 'description': 'ID posta'}
    },
    'required': ['content', 'post_id']
})

# Definicje endpointów
spec.path(
    path="/api/register",
    operations={
        'post': {
            'tags': ['Authentication'],
            'summary': 'Rejestracja nowego użytkownika',
            'requestBody': {
                'content': {
                    'application/json': {
                        'schema': {'$ref': '#/components/schemas/User'}
                    }
                }
            },
            'responses': {
                '201': {'description': 'Użytkownik zarejestrowany'},
                '400': {'description': 'Błędne dane'}
            }
        }
    }
)

spec.path(
    path="/api/login",
    operations={
        'post': {
            'tags': ['Authentication'],
            'summary': 'Logowanie użytkownika',
            'requestBody': {
                'content': {
                    'application/json': {
                        'schema': {
                            'properties': {
                                'username': {'type': 'string'},
                                'password': {'type': 'string'}
                            }
                        }
                    }
                }
            },
            'responses': {
                '200': {
                    'description': 'Zalogowano pomyślnie',
                    'content': {
                        'application/json': {
                            'schema': {
                                'properties': {
                                    'token': {'type': 'string'}
                                }
                            }
                        }
                    }
                },
                '401': {'description': 'Nieprawidłowe dane logowania'}
            }
        }
    }
)

spec.path(
    path="/api/posts",
    operations={
        'get': {
            'tags': ['Posts'],
            'summary': 'Pobierz wszystkie posty',
            'security': [{'bearerAuth': []}],
            'responses': {
                '200': {
                    'description': 'Lista postów',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'array',
                                'items': {'$ref': '#/components/schemas/Post'}
                            }
                        }
                    }
                }
            }
        },
        'post': {
            'tags': ['Posts'],
            'summary': 'Dodaj nowy post',
            'security': [{'bearerAuth': []}],
            'requestBody': {
                'content': {
                    'application/json': {
                        'schema': {'$ref': '#/components/schemas/Post'}
                    }
                }
            },
            'responses': {
                '201': {'description': 'Post dodany'},
                '400': {'description': 'Błędne dane'}
            }
        }
    }
)

spec.path(
    path="/api/comments/{post_id}",
    operations={
        'get': {
            'tags': ['Comments'],
            'summary': 'Pobierz komentarze do posta',
            'security': [{'bearerAuth': []}],
            'parameters': [
                {
                    'name': 'post_id',
                    'in': 'path',
                    'required': True,
                    'schema': {'type': 'integer'}
                }
            ],
            'responses': {
                '200': {
                    'description': 'Lista komentarzy',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'array',
                                'items': {'$ref': '#/components/schemas/Comment'}
                            }
                        }
                    }
                }
            }
        }
    }
) 