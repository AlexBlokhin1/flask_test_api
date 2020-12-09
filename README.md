Python script for putting data from csv files to postgres db.

Please install requirements.txt.

You can launch postgres from docker by using stack.yml.

Then to make a database do "flask create-db".

To add data to db do "flask prepopulate".

Endpoints:

          1) /id - put number to get asin, title and review by id.
          2) /review - to write a review.
