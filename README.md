# bookmyshow-be

## POST task

curl -X 'POST' \
 'http://127.0.0.1:8000/tasks' \
 -H 'accept: application/json' \
 -H 'Content-Type: application/json' \
 -d '{
"title": "test 1",
"description": "desc 1",
"completed": true
}'

## GET task

curl -X 'GET' \
 'http://127.0.0.1:8000/tasks' \
 -H 'accept: application/json'

## command to run locally

uvicorn app.main:app --reload
