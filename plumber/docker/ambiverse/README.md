# Ambiverse Entity linker

Follow instructions found on [Github](https://github.com/ambiverse-nlu/ambiverse-nlu).

The POST call will look like this:

```
curl --request POST \
  --url http://node4.research.tib.eu:12321/factextraction/analyze \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"docId": "doc1", "text": "Jack founded Alibaba with investments from SoftBank and Goldman.", "extractConcepts": "true", "language": "en" }'
```