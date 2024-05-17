from django.urls import path
from .views import PagesView
from .views_misc import MiscPagesView



urlpatterns = [
    path(
        "pages/account_settings/account/",
        PagesView.as_view(template_name="pages_account_settings_account.html"),
        name="pages-account-settings-account",
    ), 
]
