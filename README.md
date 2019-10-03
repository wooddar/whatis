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
- `RUNTIME_CONTEXT` - The runtime context environment variable decides which config
- `ADMIN_USER_IDS` - This variable sets individual admin Slack user IDs
- `ADMIN_CHANNEL_IDS` - This variable sets the channels where members are considered to be Terminology admins
- `SQLALCHEMY_DATABASE_URL` - This variable sets the database the Whatis bot will use {Sqlite, Postgres}

### Database setup
Whatis can run using Sqlite or Postgres database backends - it is strongly recommended that you use a Postgres backend in your production environment as this has the following benefits:

- `fuzzystrmatch` based terminology searching based on Levenshtein distance
- Thread safety  

## Running tests 
`pytest tests/`

## Contributing
Open up a pull request

# Companies using /Whatis!