import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class TimeStampedModel(models.Model):
    """
    Base class for models that need to maintain when objects were created and last_modified
    """
    create_time = models.DateTimeField(auto_now_add=True)
    last_modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Address(models.Model):
    """
        Address details
    """
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=32, null=True, blank=True)

    # we can have more attributes on the model such as lattitude, longitude (GeoSpatial location and all such) etc.


class PhoneModel(TimeStampedModel):

    # Key/val, val is stored in db
    HOME = u'Home'
    MOBILE = u'Mobile'
    OFFICE = u'Office'

    # This is select field choices displayed in UI
    CONTACT_TYPES = (
        (HOME, u'Home'),
        (MOBILE, u'Mobile'),
        (OFFICE, u'Office')
    )

    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$', message='Phone number must be a 10 digit number.')

    # Primary Contact Number. Required
    primary_contact_number = models.CharField(validators=[phone_regex], max_length=12, blank=False, null=False)
    primary_contact_type = models.CharField(max_length=10, choices=CONTACT_TYPES, default=HOME)

    # Secondary Contact Number. Optional
    secondary_contact_number = models.CharField(validators=[phone_regex], max_length=12, blank=True, null=True)
    secondary_contact_type = models.CharField(max_length=10, null=True, blank=True, choices=CONTACT_TYPES,
                                              default=MOBILE)

    class Meta:
        abstract = True


class OwnerProfile(PhoneModel):

    # One Owner profile should be associated with only one user.
    user = models.OneToOneField(User)

    # Primary Address of the owner
    primary_address = models.ForeignKey(Address, related_name='owner_profiles_primary')

    # Secondary Address of the owner
    secondary_address = models.ForeignKey(Address, null=True, blank=True, related_name='owner_profiles_secondary')


class RenterProfile(PhoneModel):

    # One Owner profile should be associated with only one user.
    user = models.OneToOneField(User)

    # Primary Address of the owner
    primary_address = models.ForeignKey(Address, related_name='renter_profiles_primary')

    # Secondary Address of the owner
    secondary_address = models.ForeignKey(Address, null=True, blank=True, related_name='renter_profiles_secondary')


class Property(TimeStampedModel):

    # Location of the property
    location = models.OneToOneField(Address)

    # Owner of the property
    owner = models.ForeignKey(OwnerProfile, related_name='properties')

    # This Flag is to indicate if the property is available for rent marked by the owner. Sometimes a property may not
    # be available for rental for various reasons like renovating it or might be using for personal use. Instead of
    # deleting the property owner can mark inactive/active.
    isActive = models.BooleanField(default=True)

    # Rent per day. Owner can vary the rent expectation.
    rental_price = models.DecimalField(max_digits=18, decimal_places=3)

    # Number of bed rooms
    bedroom_count = models.PositiveIntegerField(default=0)

    # can have more attributes on the models such as availbility of amenities like heating, a/c, swimming pool, sauna,
    #  laundry etc or even can have a separate model to track all amenities and have a Foreign Key relation.

    # We can filter all the available properties in a date range, default start date is current system date and
    #  end date is a week from now.
    @staticmethod
    def filter_available_properties(start_date=datetime.datetime.now(), end_date=datetime.datetime.now()+datetime.timedelta(7)):
        # If start_date and end_date are provided by the user, inputs needs to be sanitized and check if they are
        #  instances of datetime.datetime.
        exceptions = []
        if not isinstance(start_date, datetime.datetime):
            exceptions.append("Enter a Valid start date time")

        if not isinstance(end_date, datetime.datetime):
            exceptions.append("Enter a Valid end date time")

        if exceptions:
            raise Exception(exceptions)

        if start_date > end_date:
            raise Exception("End date should be greater than start date")


        active_properties = Properties.objects.filter(isActive=True)

        # Excludes all the properties that have start_date or end_date between the selected date ranges.
        available_properties = active_properties.exclude(reservation__is_cancelled=False,
            reservation__start_date__gte=start_date, reservation__start_date__lte=end_date,
            reservation__end_date__gte=start_date, reservation__end_date__lte=end_date)

        return available_properties

    # Filter all the available dates for a property between the start_date and end_date.
    # Default is the current system's date and end_date is 30 days from now.
    def filter_available_dates(self, start_date=datetime.datetime.now(), end_date=datetime.datetime.now()+datetime.timedelta(30)):
        # If start_date and end_date are provided by the user, inputs needs to be sanitized and check if they are
        #  instances of datetime.datetime.
        exceptions = []
        if not isinstance(start_date, datetime.datetime):
            exceptions.append("Enter a Valid start date time")

        if not isinstance(end_date, datetime.datetime):
            exceptions.append("Enter a Valid end date time")

        if exceptions:
            raise Exception(exceptions)

        if start_date > end_date:
            raise Exception("End date should be greater than start date")

        if not self.isActive:
            raise Exception("Property is not available for rent now")

        # return a list of all available dates.
        return


class Reservation(TimeStampedModel):

    # start date of the reservation. A Rental day begins at any time after 3:00PM
    start_date = models.DateTimeField(null=False, blank=False)

    # end date of the reservation. A Rental day will end at 2:59PM on each day no matter when the start date was.
    #  More validation can be written to check end_date > start_date.
    end_date = models.DateTimeField(null=False, blank=False)

    # property rented. Each reservation should have a property.
    property = models.ForeignKey(Property, related_name='reservations')

    # Person for whom the reservation was made on a property.
    renter = models.ForeignKey(RenterProfile, related_name='reservations')

    # Rent signed on reservation
    rental_price = models.DecimalField(max_digits=18, decimal_places=3)

    # If a reservation was cancelled.
    is_cancelled = models.BooleanField(default=False)

    # Notes made on the reservation.
    notes = models.TextField(null=True, blank=True)

    # Further can add more attributes like reserved_by field to indicate if a different user has reserved on behalf of
    # the renter.

    # Further validations have to be made on the save method of the reservation model where multilple reservations
    #  cannot be made between the start and end dates on a property.

    # Can add validation for the ability to cancel the reservation only before 48 hours of the start_date.