#! /bin/bash

#
# Copyright 2012 Sven Reissmann <sven@0x80.io>
#
# This file is part of pyLogView. It is licensed under the terms of the
# GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
#
# Recommended elasticsearch mapping
#

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
                "severity" : {
                    "type" : "integer",
                    "index" : "not_analyzed"
                },
                "facility" : {
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
