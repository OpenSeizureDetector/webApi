import datetime


def userFilter(queryset, user, authUser):
    """ return records for user 'user'.  authUser
    should be the authenticated user making the request so we can
    decide if we can return data for the requested user or not.
    FIXME - we need to get user group associations working so we can allow
    some users to access other users' data - this
    """
    if authUser is None:
        print("authUser is None - returning None")
        return queryset.filter(pk=-1)
    else:
        print("authUser is not None - filtering")
    
    if user is not None:
        print("userFilter: authUser="+authUser)
        if (user == authUser):
            queryset = queryset.filter(userId=user)
        else:
            # FIXME: this should check if the authUser is an admin or
            # analyst, and if they are, return the data.
            queryset = queryset.filter(userId=authUser)
    else:
        queryset = queryset.filter(userId=authUser)


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


