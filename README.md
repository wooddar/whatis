# whatis
Whatis bot for Slack - let your organisation explore, curate and create business Terminology

[![Actions Status](https://github.com/wooddar/whatis/workflows/Python+application/badge.svg)](https://github.com/wooddar/whatis/actions)


## Creating Terminology
Create new Business terminology straight from Slack with Slack Dialogs - Users adding new terminology are tagged in the Added by field

## Curating Terminology
By default, all users in your Slack workspace are able to Delete, Create, Update or rollback terminolgy - whatis allows you to specify "Terminology Admins" by indicating Admin Slack user IDs or Slack Channels to get Admin users from (**Note:** if you are using Admin Channels you must make sure your whatis bot is invited!)

## Exploring Terminology



## Installation 
`pip install whatis`

## Running whatis
Whatis can be run locally using the command `whatis deploy --db $DB_URL`

## Setting up a whatis bot on your workspace
- Create a new bot
- Set the bot name to be `/whatis`
- Grant the scopes to read conversation members
- Make a note of your bot's `slack signing secret` and `bot token`
- Set a bot icon! You can find one already made to size in the doc_images directory here.


### Environment variables
- `ADMIN_USER_IDS` - This variable sets individual admin Slack user IDs
- `ADMIN_CHANNEL_IDS` - This variable sets the channels where members are considered to be Terminology admins
- `SQLALCHEMY_DATABASE_URL` - This variable sets the database the Whatis bot will use {Sqlite, Postgres}

### Database setup
Whatis can run using Sqlite or Postgres database backends - it is strongly recommended that you use a Postgres backend in your production environment as this has the following benefits:

- `fuzzystrmatch` based terminology searching based on Levenshtein distance
- Thread safety  

## Adding existing terminology
If you have an existing company repository of terminology e.g. a shared GSheet you can migrate this over to whatis. Whatis accepts a `--preload-filepath` start argument. You can pass the path to a json records file containing your companies existing terminology to trigger a one-time load of this terminology the first time Whatis starts up, Whatis keeps track of the terminology it has already loaded so no need to worry about duplicates from the same file. 

**Note:** Editing a past records file will cause Whatis to load its contents again!

### Example terminology json records
**_load_20190929.json**
```json
[
{"terminology": "FBI", "definition":"The Federal Bureau of intelligence"},
{"terminology": "CSR", "definition":"Corporate social responsibility", "notes":"This is something we do by planting a tree every 6000 flights"},
...
{"terminology": "Lost customer", "definition":"A customer who has not requested new shoes in > 3 days", "links":"https://jira.com/issues/DE455"},
]
```

To load these records into whatis when it first starts:
```bash
whatis --preload-filepath /path/to/_load_20190929.json
```

# Running tests 
`pytest tests/` - you may need to install pytest first depending on your Python distribution

# What is planned for future Whatis releases
- Support for background tasks with Celery:
    - Letting previous terminology editors know when someone else edits their whatis
    - Allowing an action where the Whatis bot sends a CSV file of all company terminology to a user ("See all" button)
    - Support for multiple apps to use the same Whatis bot instace (verification for multiple signed secrets)
    
## Contributing
Open up a pull request

# Companies using /Whatis!