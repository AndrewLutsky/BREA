# Downloading Relevant Data

To download the relevant data first go create an entrez account and api key. Then
run the following code.

```
cd scripts
cp config.json.example config.json
```

Then in config.json change the ENTREZ_API key to be the api key that you have created through pubmed. This api key will be used
to generate the relevant pubmed data required for this. Additionally, you need to enter your ENTREZ_EMAIL key into your config.json
to agree with NCBI's term's and conditions for their API. You can find more information [here][https://www.ncbi.nlm.nih.gov/books/NBK25497/]
at the e-utilities for NCBI.


