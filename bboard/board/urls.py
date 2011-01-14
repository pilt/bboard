from django.conf.urls.defaults import *
from board.views import SearchView

urlpatterns = patterns('board.views',
    url(r'^$', SearchView(), name='board_search'),
    )
