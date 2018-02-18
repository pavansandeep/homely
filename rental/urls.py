__author__ = 'pavanchitrapu'
from django.conf.urls import include, url
from rental import views

urlpatterns = [

    # This is to indicate all the available apis
    url(r'^$', views.api_root, name='api'),

    # Owner Accounts. This is for both POST and GET methods.
    url(r'^owners$', views.OwnerList.as_view(), name='owner'),

    # GET, PUT, PATCH, DELETE methods on owner account.
    url(r'^owners/(?P<pk>[0-9]+)$', views.OwnerDetail.as_view(), name='owner-detail'),

    # Renter Accounts. This is for both POST and GET methods.
    url(r'^renters$', views.RenterList.as_view(), name='renter'),

    # GET, PUT, PATCH, DELETE methods on renter account. Cannot delete renter account if he has any properties reserved.
    url(r'^renters/(?P<pk>[0-9]+)$', views.RenterDetail.as_view(), name='renter-detail'),

    # Create properties for a owner. Assuming only owners can add properties. POST and GET of all properties for a owner.
    url(r'^owners/(?P<pk>[0-9]+)/properties$', views.OwnerPropertyList.as_view(), name='ownerproperty'),

    # GET, PUT, PATCH, DELETE methods on properties by a owner.
    url(r'^owners/(?P<pk>[0-9]+)/properties/(?P<pk>[0-9]+)$', views.OwnerPropertyDetail.as_view(), name='ownerproperty-detail'),

    # API to find all properties, dates can be passed in query params to find list of all available properties in a date
    # range.
    url(r'^properties$', views.PropertyList.as_view(), name='property'),

    # API for GET, PUT, PATCH, DELETE given an id
    url(r'^properties/(?P<pk>[0-9]+)$', views.PropertyDetail.as_view(), name='property-detail'),

    # API to search all properties and can pass any property related fields as query params
    url(r'^search/properties$', views.SearchProperties.as_view(), name='search-properties'),

    # API to create and get reservations.
    url(r'^reservations$', views.Reservationlist.as_view(), name='reservation'),

    # API for PUT, PATCH, DELETE method on reservations.
    url(r'^reservations/(?P<pk>[0-9]+)$', views.ReservationDetail.as_view(), name='reservation-detail')

    # API to create and get list of addresses.
    url(r'^addresses$', views.AddressList.as_view(), name='address'),

    # API to GET, PUT, PATCH, DELETE an address. Cannot delete an address if it's associated with a user or property.
    url(r'^addresses/(?P<pk>[0-9]+)$', views.AddressDetail.as_view(), name='address-details'),
]

