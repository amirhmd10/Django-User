from django.apps import AppConfig


#____for run this file must in settings set the app name in install app
#whith this format     'account.apps.AccountConfig',


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'


    def ready(self):
        import account.signals

