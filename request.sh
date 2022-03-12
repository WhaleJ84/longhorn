#!/bin/sh

curl -X POST \
  'http://127.0.0.1:5000/link-down/' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization': 'Bearer dGhpc19pc19pbnNlY3VyZQ==' \
  -d '{
  	"causing_ci": "hostname.example.com",
  	"event_text": "LINK DOWN | TRANSIT-LON<>CAR | A3",
  	"event_url": "https://example.com",
  	"timestamp": "2021-10-15 23:20:01"
  }'
