import datetime
from rest_framework.exceptions import PermissionDenied


def fixMissingSeconds(dateTimeStr):
    """ Expects a datetime string in format yyyy-mm-dd hh:mm:ss.
    If the :ss part is missing off the end, it adds ':00'
    to the end so that strptime will not bomb out with an error.
    """
    # FIXME - This would be a useful function to have!
        


def userFilter(queryset, user, authUser):
    """ return records for user 'user'.  authUser
    should be the authenticated user making the request so we can
    decide if we can return data for the requested user or not.
    FIXME - we need to get user group associations working so we can allow
    some users to access other users' data
    """
    if authUser is None:
        print("common.queryUtils.userFilter: authUser is None - returning None")
        return queryset.filter(pk=-1)
    else:
        print("common.queryUtils.userFilter: authUser is not None - filtering")
    print("common.queryUtils.userFilter: user=",user)
    print("common.queryUtils.userFilter: authUser=",(authUser))
    if user is not None:
        print("common.queryUtils.userFilter: userFilter: authUser=",(authUser))
        if (user == authUser):
            # the authenticated user is asking for his own data - OK
            queryset = queryset.filter(userId=user)
        else:
            if (authUser.is_staff):
                print("common.queryUtils.userFilter: staff user asking for someone else's data - OK");
                # we use the is_staff parameter to signify a researcher.
                queryset = queryset.filter(userId=user)
            else:
                print("common.queryUtils.userFilter: non-staff user asking for someone else's data returning error");
                #queryset = None
                raise PermissionDenied(detail="Non-Staff User")
    else:
        print("user is None - returning data for authUser")
        queryset = queryset.filter(userId=authUser)
    print("common.queryUtils.userFilter: returning queryset = ",queryset.query)
    return queryset

def dateFilter(queryset,
               startDateStr, endDateStr, durationMinStr):
    """
        gets a filtered dataset based on query parameters:
        start : start date/time yyyy-mm-dd hh:mm:ss
           end : end date/time yyyy-mm-dd hh:mm:ss
           duration:  required duration (minutes)
        If both start and end are specified, duration is ignored.
        duration is used if only start or end is specified.
        """
    # convert dates into datetime objects.
    if startDateStr is not None:
        startDate = datetime.datetime.strptime(
            startDateStr, "%Y-%m-%d %H:%M:%S")
    else:
        startDate = None

    if endDateStr is not None:
        endDate = datetime.datetime.strptime(
            endDateStr, "%Y-%m-%d %H:%M:%S")
    else:
        endDate = None

    # Decide which start and end date to use, based on which parameters
    # we have been given.
    if (startDate is None and endDate is None):
        print("no dates specified - returning all records")
    else:
        if (startDate is None):
            print("startDate not specified - trying to derive it from endDate")
            if (durationMinStr is not None):
                dt = datetime.timedelta(minutes=float(durationMinStr))
                startDate = endDate-dt
            else:
                print("duration not specified, so we can't!")
                startDate = None
                endDate = None
        if (endDate is None):
            print("endDate not specified - trying to derive it from endDate")
            if (durationMinStr is not None):
                dt = datetime.timedelta(minutes=float(durationMinStr))
                endDate = startDate+dt
            else:
                print("duration not specified, so we can't!")
                startDate = None
                endDate = None
            
            
    if startDate is not None and endDate is not None:
        queryset = queryset.filter(dataTime__gte=startDate, dataTime__lte=endDate)
    return queryset


def eventTypeFilter(queryset, eventType):
    #FIXME - this is not finished https://stackoverflow.com/questions/48319957/djangofilterbackend-field-null suggests that using filter_fields = {'eventType' : [isnull']} should work so may not need this
    """ return records where eventType is the specified event Type
    """
    print("common.queryUtils.eventTypeFilter: eventType=",eventType)
    if user is not None:
        print("common.queryUtils.userFilter: userFilter: authUser="+authUser)
        if (user == authUser):
            queryset = queryset.filter(userId=user)
        else:
            # FIXME: this should check if the authUser is an admin or
            # analyst, and if they are, return the data.
            queryset = queryset.filter(userId=authUser)
    else:
        print("user is None - returning data for authUser")
        queryset = queryset.filter(userId=authUser)
    print("common.queryUtils.userFilter: returning queryset = ",queryset.query)
    return queryset
