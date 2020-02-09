API Test Cases
==============

Front End
---------
/ Unauthenticated shows about page.
 




API Endpoints
-------------
Auth = Authenticated as normal user
Admin = Authenticated as admin user
Analyst = Authenticated as analyst user
NoAuth = Not Authenticated

where id=n, n is not the authenticated user id.

| url             | Action   | Auth        | response code | payload             | Comment
| ---             | ---      | ---         | ---           | ---                 | ---
| /accounts/      | GET      | Auth/NoAuth | 404           | none                |
| /accounts/register | POST     | Auth/NoAuth | 200 or 403    | Not sure!               | check what happens if inv| alid data provided.
| /accounts/register | not POST | Auth/NoAuth | 403           | none                |
| /accounts/login | POST     | Auth/NoAuth | 200 or 403    | token               |
| /accounts/login | not POST | Auth/NoAuth | 403           | none                |
| /profile/       | GET      | Auth        | 200           | auth user profile   |
| /profile/?id=n  | GET      | Auth        | 403           | none                |
| /profile/?id=n  | GET      | Aanalyst    | 200           | Anonymised profile  | No name or email, just user id
| /profile/?id=n  | GET      | Admin       | 200           | user profile        |
| /profile/       | POST     | Any         | 403           | none                | Profile created with user
| /profile/       | PUT      | Auth-Analyst| 200           | modified profile    | if userid is auth user id
| /profile/       | PUT      | Auth-Analyst| 403           | none                | if userid is not auth user id
| /profile/       | PUT      | Admin       | 200           | modified profile    | 
| /profile/       | DELETE   | Auth-Analyst| 200           | none                | if userid is auth user id
| /profile/       | DELETE   | Auth-Analyst| 403           | none                | if userid is not auth user id
| /profile/       | DELETE   | Admin       | 200           | none                | 
| /events/        | GET      | any Auth    | 200           | list of events      | returns events for auth user id.
| /events/?user=n | GET      | Auth        | 403           | none                | unless user = auth user id
| /events/?user=n | GET      | Analyst,Admin|200           | events for user     | 
| /events/?id=n   | GET      | Auth        | 403           | none                | unless user = auth user id
| /events/?id=n   | GET      | Auth        | 200           | event no id         | provided user = auth user id
| /events/?id=n   | GET      | Analyst,Admin|200           | events no id        | 
| /events/        | POST     | Auth,Analyst| 200           | event data          | create event if user=auth user | id| 
| /events/        | POST     | Auth,Analyst| 403           | none                | if user != auth user id
| /events/        | POST     | Admin       | 200           | event data          | create event for any user
| /events/        | PUT      | Auth-Analyst| 200           | modified event      | if userid is auth user id
| /events/        | PUT      | Auth-Analyst| 403           | none                | if userid is not auth user id
| /events/        | PUT      | Admin       | 200           | modified event    | 
| /events/        | DELETE   | Auth-Analyst| 200           | none                | if userid is auth user id
| /events/        | DELETE   | Auth-Analyst| 403           | none                | if userid is not auth user id
| /events/        | DELETE   | Admin       | 200           | none                | 
| /datapoints/    | GET      | any Auth    | 200           | list of events      | returns events for auth user id.
| /datapoints/?user=n | GET      | Auth        | 403           | none                | unless user = auth user id
| /datapoints/?user=n | GET      | Analyst,Admin|200           | events for user     | 
| /datapoints/?id=n   | GET      | Auth        | 403           | none                | unless user = auth user id
| /datapoints/?id=n   | GET      | Auth        | 200           | event no id         | provided user = auth user id
| /datapoints/?id=n   | GET      | Analyst,Admin|200           | events no id        | 
| /datapoints/    | POST     | Auth,Analyst| 200           | event data          | create event if user=auth user | id 
| /datapoints/    | POST     | Auth,Analyst| 403           | none                | if user != auth user id
| /datapoints/    | POST     | Admin       | 200           | event data          | create event for any user
| /datapoints/    | PUT      | Auth-Analyst| 200           | modified event      | if userid is auth user id
| /datapoints/    | PUT      | Auth-Analyst| 403           | none                | if userid is not auth user id
| /datapoints/    | PUT      | Admin       | 200           | modified event    | 
| /datapoints/    | DELETE   | Auth-Analyst| 200           | none                | if userid is auth user id
| /datapoints/    | DELETE   | Auth-Analyst| 403           | none                | if userid is not auth user id
| /datapoints/    | DELETE   | Admin       | 200           | none                | 

Note: /datapoints/ and /events/ urls also support the following url parameters to filter by date/time:
 - start - start date/time yyyy-mm-dd hh:mm:ss
 - end   - end   date/time yyyy-mm-dd hh:mm:ss
 - duration - duration in minutes (if specified, only need either start or end parameter - ignored if both start and end specified).

