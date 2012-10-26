#! /bin/bash

curl -X DELETE "http://localhost:9200/syslog";

curl -X PUT "http://localhost:9200/syslog" -d '{
    "mappings" : {
        "event" : {
            "_ttl" : {
                "enabled" : true,
                "default" : "1y"
            },
            "properties" : {
                "time" : {
                    "type" : "date",
                    "format" : "dateOptionalTime"
                },
                "host" : {
                    "type" : "string",
                    "index" : "not_analized"
                },
                "facility" : {
                    "type" : "integer",
                    "index" : "not_analized"
                },
                "severity" : {
                    "type" : "integer",
                    "index" : "not_analized"
                },
                "program" : {
                    "type" : "string",
                    "index" : "not_analized"
                },
                "message" : {
                    "type" : "string",
                    "analyzer" : "standard"
                }
            }
        }
    }
}'
