# Naive Modern Search

### An implmentation of modern information retrieval based on magic of Freebase
--------------------------------------------------------------------------

## Dependency
Please make sure `prettytable` is installed.

```
easy_install prettytable
```
or run
"pip install prettytable --user"

## Usage
Two major features are supported: Infobox and Magic 8 Ball.
Note: I passed in my api key as the default so you don't have to pass it in.
      The option of mandating an api key can be easily supported.

### Infobox
===========================================================================
Inside the project directory. Sample test queries can be ran as the following:
```
python app/infobox.py "Bill Gates"
python app/infobox.py "Robert Downey Jr."
python app/infobox.py "Jackson"
python app/infobox.py "NFL"
python app/infobox.py "NBA"
python app/infobox.py "NY Knicks"
python app/infobox.py "Miami Heat"
```

## Question answer
### Magic 8 Ball
===========================================================================
Notes: the questions must closely follow the semantics of the question:
  "Who created [X]?", where [X] is replaced by your entitye of interest.

  Examples:
  - A valid question with valid format: "Who created Oprah Winfrey?"
  - An *invalid* question: "What created Oprah Windrey?"
  - A valid question with *invalid* format: "who creates Oprah Windfrey?"

Some sample test queries:
```
python app/magic8ball.py "Who created Google?"
python app/magic8ball.py "Who created Lord of the Rings?"
python app/magic8ball.py "Who created Microsoft?"
python app/magic8ball.py "Who created Romeo and Juliet?"
```


## Design overview

### Main workflow of Infobox
===========================================================================
- 6 entities of interest are included in the infobox, each entity is established as a model.
- Each model has its own attributes to extract, has its own way to print out a sub infobox.
- All models share 4 common methods of extracting values:
    * `extract_value_by_text`
       extract a single value from a structured freebase JSON response:

       extract_value_by_text('slogan')

          {"sports/sports_league":
              {"slogan": {"values": [{"lang": "en", "text": "Where Amazing Happens"}]}}}

    * `extract_values_by_text`
       extract an array of values from a structured freebase JSON response:

       extract_values_by_text('organization_founded')

           {"organization/founder":
              {"organization_founded": {"values": [{"lang": "en", "text": "Microsoft" ...}, {"lang": "en", "text": "Microsoft Research"...}]}}}

    * `extract_values_by_property`
       extract an array of values by decomposing property from a structured freebase JSON response, which requires a primary key and a secondary key:

       extract_values_by_property(extracted_hash, 'sibling_s', '/people/sibling_relationship/sibling')

           {u'count': 2.0,
            u'values': [{u'creator': u'/user/igupta',
                         u'id': u'/m/0j8ryqd',
                         u'lang': u'en',
                         u'property': {u'/people/sibling_relationship/sibling': {u'count': 2.0,
                                                                                 u'values': [{u'creator': u'/user/igupta',
                                                                                              u'id': u'/m/0j8ryqf',
                                                                                              u'lang': u'en',
                                                                                              u'text': u'Libby Gates',
                                                                                              u'timestamp': u'2012-04-20T02:56:29Z'}],
                                                                                 u'valuetype': u'object'},
                                       u'/type/object/attribution': {u'count': 1.0,
                                                                     u'values': [{u'creator': u'/user/igupta',
                                                                                  u'id': u'/m/0j67w4s',
                                                                                  u'lang': u'en',
                                                                                  u'text': u'igupta',
                                                                                  u'timestamp': u'2012-04-20T02:56:29Z'}],
                                                                     u'valuetype': u'object'},
                                       u'/type/object/type': {u'count': 1.0,
                                                              u'values': [{u'creator': u'/user/igupta',
                                                                           u'id': u'/people/sibling_relationship',
                                                                           u'lang': u'en',
                                                                           u'text': u'Sibling Relationship',
                                                                           u'timestamp': u'2012-04-20T02:56:29Z'}],
                                                              u'valuetype': u'object'}},
                         u'text': u'igupta - Libby Gates - Sibling Relationship',
                         u'timestamp': u'2012-04-20T02:56:29Z'},
                        {u'creator': u'/user/igupta',
                         u'id': u'/m/0j8ryqq',
                         u'lang': u'en',
                         u'property': {u'/people/sibling_relationship/sibling': {u'count': 2.0,
                                                                                 u'values': [{u'creator': u'/user/igupta',
                                                                                              u'id': u'/m/0j8ryqr',
                                                                                              u'lang': u'en',
                                                                                              u'text': u'Kristi Gates',
                                                                                              u'timestamp': u'2012-04-20T02:56:29.001Z'}],
                                                                                 u'valuetype': u'object'},
                                       u'/type/object/attribution': {u'count': 1.0,
                                                                     u'values': [{u'creator': u'/user/igupta',
                                                                                  u'id': u'/m/0j67w4s',
                                                                                  u'lang': u'en',
                                                                                  u'text': u'igupta',
                                                                                  u'timestamp': u'2012-04-20T02:56:29.001Z'}],
                                                                     u'valuetype': u'object'},
                                       u'/type/object/type': {u'count': 1.0,
                                                              u'values': [{u'creator': u'/user/igupta',
                                                                           u'id': u'/people/sibling_relationship',
                                                                           u'lang': u'en',
                                                                           u'text': u'Sibling Relationship',
                                                                           u'timestamp': u'2012-04-20T02:56:29.001Z'}],
                                                              u'valuetype': u'object'}},
                         u'text': u'igupta - Kristi Gates - Sibling Relationship',
                         u'timestamp': u'2012-04-20T02:56:29.001Z'}],
            u'valuetype': u'compound'}

    * `extract_nested_values_by_property`
       extract a list related attributes (i.e. information about player roster: what is the postion? when did the player start & end playing?),
       the method requires a primary key and a list of secondary keys.

       An example freebase JSON response:

       extract_nested_values_by_property(extracted_hash, 'film', ['film', 'character'])

         {u'count': 72.0,
          u'values': [{u'creator': u'/user/mwcl_infobox',
                       u'id': u'/m/0jsh5q',
                       u'lang': u'en',
                       u'property': {u'/film/performance/character': {u'count': 1.0,
                                                                      u'values': [{u'creator': u'/user/starbuckz',
                                                                                   u'id': u'/m/0gxttdp',
                                                                                   u'lang': u'en',
                                                                                   u'text': u'Ralph Carr',
                                                                                   u'timestamp': u'2011-07-11T03:00:12.008Z'}],
                                                                      u'valuetype': u'object'},
                                     u'/film/performance/film': {u'count': 1.0,
                                                                 u'values': [{u'creator': u'/user/mwcl_infobox',
                                                                              u'id': u'/m/0372h4',
                                                                              u'lang': u'en',
                                                                              u'text': u'1969',
                                                                              u'timestamp': u'2006-11-30T18:39:50.003Z'}],
                                                                 u'valuetype': u'object'},
                                     u'/type/object/attribution': {u'count': 1.0,
                                                                   u'values': [{u'creator': u'/user/mwcl_infobox',
                                                                                u'id': u'/m/0jsg18',
                                                                                u'lang': u'en',
                                                                                u'text': u'Freebase Data Team',
                                                                                u'timestamp': u'2006-11-30T18:39:50.003Z'}],
                                                                   u'valuetype': u'object'},
                                     u'/type/object/type': {u'count': 1.0,
                                                            u'values': [{u'creator': u'/user/mwcl_infobox',
                                                                         u'id': u'/film/performance',
                                                                         u'lang': u'en',
                                                                         u'text': u'Film performance',
                                                                         u'timestamp': u'2006-11-30T18:39:50.003Z'}],
                                                            u'valuetype': u'object'}},
                       u'text': u'Ralph Carr - 1969 - Freebase Data Team - Film performance',
                       u'timestamp': u'2006-11-30T18:39:50.003Z'},
                      {u'creator': u'/user/mwcl_infobox',
                       u'id': u'/m/0jy7tw',
                       u'lang': u'en',
                       u'property': {u'/film/performance/character': {u'count': 1.0,
                                                                      u'values': [{u'creator': u'/user/starbuckz',
                                                                                   u'id': u'/m/0gxtth2',
                                                                                   u'lang': u'en',
                                                                                   u'text': u'Lee',
                                                                                   u'timestamp': u'2011-07-11T03:00:13.004Z'}],
                                                                      u'valuetype': u'object'},
                                     u'/film/performance/film': {u'count': 1.0,
                                                                 u'values': [{u'creator': u'/user/mwcl_infobox',
                                                                              u'id': u'/m/09kml0',
                                                                              u'lang': u'en',
                                                                              u'text': u'Firstborn',
                                                                              u'timestamp': u'2006-11-30T19:02:47.006Z'}],
                                                                 u'valuetype': u'object'},
                                     u'/type/object/attribution': {u'count': 1.0,
                                                                   u'values': [{u'creator': u'/user/mwcl_infobox',
                                                                                u'id': u'/m/0jsg18',
                                                                                u'lang': u'en',
                                                                                u'text': u'Freebase Data Team',
                                                                                u'timestamp': u'2006-11-30T19:02:47.006Z'}],
                                                                   u'valuetype': u'object'},
                                     u'/type/object/type': {u'count': 1.0,
                                                            u'values': [{u'creator': u'/user/mwcl_infobox',
                                                                         u'id': u'/film/performance',
                                                                         u'lang': u'en',
                                                                         u'text': u'Film performance',
                                                                         u'timestamp': u'2006-11-30T19:02:47.006Z'}],
                                                            u'valuetype': u'object'}},
                       u'text': u'Lee - Firstborn - Freebase Data Team - Film performance',
                       u'timestamp': u'2006-11-30T19:02:47.006Z'}
          u'valuetype': u'compound'}

Examples of how a model uses the 4 methods to populate values:

  ---------------------------------------------------------------------------------------------------------------
  |Model type        |Attribute               |Extract method                                                   |
  |------------------|------------------------|-----------------------------------------------------------------|
  |Author            |books                   |extract_values_by_text('books')                                  |
  |                  |books_about             |extract_values_by_text(extracted_hash, 'book_editions_published')|
  ---------------------------------------------------------------------------------------------------------------

  Note: each model closely follow the same template. If you look at app/models/[model_name].py, the logic of how the information got extracted should be self-explanatory.

### Main workflow of Magic 8 Ball
===========================================================================
Two types mql qureies can be made for business person and author
The queries are able to answer questions such as "Who created [X]".

- Business Person:
  Example: query "Who created Mircrosoft?"

          [{
                  "/organization/organization_founder/organizations_founded": [{
                    "a:name": None,
                    "name~=": "Microsoft"
                  }],
                "name": None,
                "type": "/organization/organization_founder"
           }]

- Author:
Example: query "Who created Mircrosoft?"

        [{
                "/organization/organization_founder/organizations_founded": [{
                  "a:name": None,
                  "name~=": "Microsoft"
                }],
              "name": None,
              "type": "/organization/organization_founder"
         }]
