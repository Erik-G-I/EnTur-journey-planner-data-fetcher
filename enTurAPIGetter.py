import requests
from datetime import datetime
now = datetime.now().strftime("%d%m%Y-%H:%M:%S")



# the routes require the NSR code for the origin and destination stops. These can easily be obtained from EnTurs online API IDE.
routes = {"Arna-Flaktveit": {"originName": '"Arna"', "originCode": '"NSR:GroupOfStopPlaces:46"', "destinationName": '"Flaktveit"', "destinationCode" : '"NSR:StopPlace:31228"'},
          "Nipedalen-BergenLufthavn": {"originName": '"Nipedalen"', "originCode": '"NSR:StopPlace:31856"', "destinationName": '"BergenLufthavn"', "destinationCode" : '"NSR:StopPlace:58536"'},
          "Nattlandsfjellet-Florida": {"originName": '"Nattlandsfjellet"', "originCode": '"NSR:StopPlace:29275"', "destinationName": '"Florida"', "destinationCode" : '"NSR:StopPlace:58544"'},
          "Hylkje-Bontveit" :{"originName": '"Hylkje"', "originCode": '"NSR:StopPlace:31175"', "destinationName": '"Bontveit"', "destinationCode": '"NSR:StopPlace:31622"'},
          "Hilleren-Nordbø" :{"originName": '"Hilleren"', "originCode": '"NSR:StopPlace:32059"', "destinationName": '"Nordbø"', "destinationCode": '"KVE:TopographicPlace:4601-Nordbøveien"'}}

times = {"08:00" : True,
         "10:00": True,
         "15:30": False,
         "17:00": False}


URL = "https://api.entur.io/journey-planner/v3/graphql"

# EnTur's API documentation says the "ET-Client-Name" header is important to include to avoid being rate limited when accessing their endpoint
HEADERS = {"Content-Type": "application/json", "ET-Client-Name": "UIB-MASTERPROJECT-SKYSS-ANALYSIS"}


def saveRoutes(routes, times, date):
    for x in routes:
        
        originCode = routes[x]["originCode"]
        originName = routes[x]["originName"]
        destinationName = routes[x]["destinationName"]
        destinationCode = routes[x]["destinationCode"]

        for y in times:
            dateTime = '"'+date+y+':00+01:00"'
            if times[y]:
                queryForward =  "{trip(from:{name:"+originName+" place:"+originCode+"}to:{name:"+destinationName+" place:"+destinationCode+"}numTripPatterns:3 dateTime:"+dateTime+" walkSpeed:1.3 includeRealtimeCancellations:false arriveBy:true){tripPatterns{expectedStartTime aimedStartTime expectedEndTime aimedEndTime duration streetDistance legs{mode expectedStartTime aimedStartTime expectedEndTime aimedEndTime realtime distance duration serviceJourney{id}line{id publicCode}}}}}"
                queryBackward = "{trip(from:{name:"+destinationName+" place:"+destinationCode+"}to:{name:"+originName+" place:"+originCode+"}numTripPatterns:3 dateTime:"+dateTime+" walkSpeed:1.3 includeRealtimeCancellations:false arriveBy:true){tripPatterns{expectedStartTime aimedStartTime expectedEndTime aimedEndTime duration streetDistance legs{mode expectedStartTime aimedStartTime expectedEndTime aimedEndTime realtime distance duration serviceJourney{id}line{id publicCode}}}}}"
            else:
                queryForward = "{trip(from:{name:"+originName+" place:"+originCode+"}to:{name:"+destinationName+" place:"+destinationCode+"}numTripPatterns:3 dateTime:"+dateTime+" walkSpeed:1.3 includeRealtimeCancellations:false arriveBy:false){tripPatterns{expectedStartTime aimedStartTime expectedEndTime aimedEndTime duration streetDistance legs{mode expectedStartTime aimedStartTime expectedEndTime aimedEndTime realtime distance duration serviceJourney{id}line{id publicCode}}}}}"
                queryBackward = "{trip(from:{name:"+destinationName+" place:"+destinationCode+"}to:{name:"+originName+" place:"+originCode+"}numTripPatterns:3 dateTime:"+dateTime+" walkSpeed:1.3 includeRealtimeCancellations:false arriveBy:false){tripPatterns{expectedStartTime aimedStartTime expectedEndTime aimedEndTime duration streetDistance legs{mode expectedStartTime aimedStartTime expectedEndTime aimedEndTime realtime distance duration serviceJourney{id}line{id publicCode}}}}}"
            fileName = now+".gql"

            BODY = {"query": queryForward}
            rForward = requests.post(headers=HEADERS, url=URL, json=BODY)
            BODY = {"query": queryBackward}
            rBackward = requests.post(headers=HEADERS, url=URL, json=BODY)
            
            f = open(mode="a+", file="/Users/erikingebrigtsen/Documents/UIB/Master/"+fileName)
            f.write(originName.strip('"')+"-"+destinationName.strip('"')+y+": "+rForward.text+"\n")
            f.write(destinationName.strip('"')+"-"+originName.strip('"')+y+": "+rBackward.text+"\n")
            f.close()

saveRoutes(routes, times, "2024-12-17T")


