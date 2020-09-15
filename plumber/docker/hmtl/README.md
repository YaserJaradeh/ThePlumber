# HMTL tool

Follow instructions found on [HMTL github page](https://github.com/huggingface/hmtl).

Add the Dockerfile to the folder, and replace inside the demo folder the server.py file with the one provided here.

The POST call will look like this:

```
curl --location --request POST 'http://localhost:11111/jmd/' \
--header 'accept: application/json' \
--header 'content-type: application/json' \
--data-raw '{
    "text": "My mother likes Goldman. She buys there clothes each month. She also like Dolce & Gabana."
}'
```

## Alternative setup method

you can just clone the docker image from docker hub

```
docker pull jaradeh/plumber:hmtl
```