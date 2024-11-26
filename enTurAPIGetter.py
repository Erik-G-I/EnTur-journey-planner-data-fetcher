import requests
from datetime import datetime
query = ""
fileName = ""
now = datetime.now().strftime("%d%m%Y-%H:%M:%S")


# the routes require the NSR code for the origin and destination stops. These can easily be obtained from EnTurs online API IDE.
routes = {"Arna-Flaktveit": {"originName": '"Arna"', "originCode": '"NSR:GroupOfStopPlaces:46"', "destinationName": '"Flaktveit"', "destinationCode" : '"NSR:StopPlace:31228"'},
          "Nipedalen-BergenLufthavn": {"originName": '"Nipedalen"', "originCode": '"NSR:StopPlace:31856"', "destinationName": '"BergenLufthavn"', "destinationCode" : '"NSR:StopPlace:58536"'},
          "Nattlandsfjellet-Florida": {"originName": '"Nattlandsfjellet"', "originCode": '"NSR:StopPlace:29275"', "destinationName": '"Florida"', "destinationCode" : '"NSR:StopPlace:58544"'}}

times = {"08:00" : True,
         "10:00": True,
         "15:30": False,
         "17:00": False}


URL = "https://api.entur.io/journey-planner/v3/graphql"

# EnTur's API documentation says the "ET-Client-Name" header is important to include to avoid being rate limited when accessing their endpoint
HEADERS = {"Content-Type": "application/json", "ET-Client-Name": "UIB-MASTERPROJECT-SKYSS-ANALYSIS"}



# original direction
for x in routes:
    originName = routes[x]["originName"]
    originCode = routes[x]["originCode"]
    destinationName = routes[x]["destinationName"]
    destinationCode = routes[x]["destinationCode"]

    for y in times:
        # dateTime is the date used for the journey planning. This should be set to some time ahead of the current time to ensure data being fetched
        dateTime = '"2024-11-28T'+y+':00+01:00"'
        if times[y]:
            query =  "{trip(from:{name:"+originName+" place:"+originCode+"}to:{name:"+destinationName+" place:"+destinationCode+"}numTripPatterns:3 dateTime:"+dateTime+" walkSpeed:1.3 includeRealtimeCancellations:false arriveBy:true){tripPatterns{expectedStartTime expectedEndTime duration streetDistance legs{mode expectedStartTime expectedEndTime realtime distance duration serviceJourney{id}line{id publicCode}}}}}"
        else:
            query = "{trip(from:{name:"+originName+" place:"+originCode+"}to:{name:"+destinationName+" place:"+destinationCode+"}numTripPatterns:3 dateTime:"+dateTime+" walkSpeed:1.3 includeRealtimeCancellations:false arriveBy:false){tripPatterns{expectedStartTime expectedEndTime duration streetDistance legs{mode expectedStartTime expectedEndTime realtime distance duration serviceJourney{id}line{id publicCode}}}}}"
        
        fileName = now+".gql"
        BODY = {"query": query}
        r = requests.post(headers=HEADERS, url=URL, json=BODY)

        f= open(mode="a+", file="/Users/erikingebrigtsen/Documents/UIB/Master/"+fileName)
        f.write(x+y+": "+r.text+"\n")
        f.close()


# opposite direction
# the manual changes needed in the for-loop above is also needed here to make sure the opposite direction is requested correctly. THIS WILL BE FIXED TO BE EASIER TO USE
for x in routes:
    # swap the origin and destination to get the route in the opposite direction
    originName = routes[x]["destinationName"]
    originCode = routes[x]["destinationCode"]
    destinationName = routes[x]["originName"]
    destinationCode = routes[x]["originCode"]

    for y in times:
        dateTime = '"2024-11-28T'+y+':00+01:00"'
        if times[y]:
            query =  "{trip(from:{name:"+originName+" place:"+originCode+"}to:{name:"+destinationName+" place:"+destinationCode+"}numTripPatterns:3 dateTime:"+dateTime+" walkSpeed:1.3 includeRealtimeCancellations:false arriveBy:true){tripPatterns{expectedStartTime expectedEndTime duration streetDistance legs{mode expectedStartTime expectedEndTime realtime distance duration serviceJourney{id}line{id publicCode}}}}}"
        else:
            query = "{trip(from:{name:"+originName+" place:"+originCode+"}to:{name:"+destinationName+" place:"+destinationCode+"}numTripPatterns:3 dateTime:"+dateTime+" walkSpeed:1.3 includeRealtimeCancellations:false arriveBy:false){tripPatterns{expectedStartTime expectedEndTime duration streetDistance legs{mode expectedStartTime expectedEndTime realtime distance duration serviceJourney{id}line{id publicCode}}}}}"
        
        fileName = now+".gql"
        BODY = {"query": query}
        r = requests.post(headers=HEADERS, url=URL, json=BODY)
        
        f = open(mode="a+", file="/Users/erikingebrigtsen/Documents/UIB/Master/"+fileName)
        f.write(originName.strip('"')+"-"+destinationName.strip('"')+y+": "+r.text+"\n")
        f.close()





