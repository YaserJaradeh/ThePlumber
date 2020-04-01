import stanza
from openie import StanfordOpenIE

# stanza.download('en')        # This downloads the English models for the neural pipeline
# nlp = stanza.Pipeline('en')  # This sets up a default neural pipeline in English

if __name__ == '__main__':
    # doc = nlp("Barack Obama was born in Hawaii.  He was elected president in 2008.")
    # doc.sentences[0].print_dependencies()
    with StanfordOpenIE() as client:
        text = 'Barack Obama was born in Hawaii.  He was elected president in 2008.'
        print('Text: %s.' % text)
        for triple in client.annotate(text):
            print('|-', triple)
