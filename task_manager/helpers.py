from django.test import modify_settings, override_settings


test_english = override_settings(
    LANGUAGE_CODE='en-US',
    LANGUAGES=(('en', 'English'),),
)

remove_rollbar = modify_settings(
    MIDDLEWARE={
        'remove':
            ['rollbar.contrib.django.middleware.RollbarNotifierMiddleware', ]
    }
)
