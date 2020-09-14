# NeuralCoref service

Creates a docker container which is running a service to host the Neural coref system.

The API looks like this

```
curl --location --request POST 'localhost:22222/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "text": "My sister has a dog. She loves him."
}'
```