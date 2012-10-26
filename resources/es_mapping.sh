#! /bin/bash

curl -X DELETE "http://localhost:9200/syslog";

curl -X PUT "http://localhost:9200/syslog" -d '{
    "mappings" : {
        "event" : {
            "_ttl" : {
                "enabled" : true,
                "default" : "365d"
            },
            "properties" : {
                "time" : {
                    "type" : "date",
                    "format" : "dateOptionalTime"
                },
                "host" : {
                    "type" : "string",
                    "index" : "not_analyzed"
                },
                "facility" : {
                    "type" : "integer",
                    "index" : "not_analyzed"
                },
                "severity" : {
                    "type" : "integer",
                    "index" : "not_analyzed"
                },
                "program" : {
                    "type" : "string",
                    "index" : "not_analyzed"
                },
                "message" : {
                    "type" : "string",
                    "analyzer" : "standard"
                }
            }
        }
    }
}'
