from django.conf.urls import url
from usaspending_api.recipient.v2.views.states import StateMetaDataViewSet, StateAwardBreakdownViewSet, ListStates
from usaspending_api.recipient.v2.views.recipients import RecipientOverView
from usaspending_api.recipient.v2.views.recipients import ChildRecipients
from usaspending_api.recipient.v2.views.list_recipients import ListRecipients, ListRecipientsByDuns, RecipientCount

urlpatterns = [
    url(r"^$", ListRecipients.as_view()),
    url(r"^duns/$", ListRecipientsByDuns.as_view()),
    url(r"^count/$", RecipientCount.as_view()),
    url(r"^duns/(?P<recipient_id>.*)/$", RecipientOverView.as_view()),
    url(r"^children/(?P<duns_or_uei>[0-9a-zA-Z]{9,12})/$", ChildRecipients.as_view()),
    url(r"^state/(?P<fips>[0-9]{,2})/$", StateMetaDataViewSet.as_view()),
    url(r"^state/awards/(?P<fips>[0-9]{,2})/$", StateAwardBreakdownViewSet.as_view()),
    url(r"^state/$", ListStates.as_view()),
]
