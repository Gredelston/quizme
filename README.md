# QuizMe

I wrote this doohickey to help me memorize certain datasets. Maybe you'll use it, too!

# Usage

To view usage instructions:

```> python quizme.py --help```

To run a quiz on Oscar Best Picture winners:

```> python quizme.py best-picture```

To display a list of categories for the best-picture quiz:

```> python quizme.py best-picture --categories```

To run a quiz on Oscar Best Picture winners of the 1950s:

```> python quizme.py best-picture --category 1950s```

# Adding data sets
Each data set should be a CSV with the following properties:

* File should have the .csv extension.
* The first row should be a header containing the following (comma-separated) fieldnames:
  * `prompt`
  * `answer`
  * `categories`
  * `other_answers`
* `prompt` and `answer` are mandatory for every row.
* If `categories` and/or `other_answers` are provided for a row, they should each be a semicolon-delimited string.

# Todo

* Add a few more datasets
  * The Muses
  * Olympic host cities
  * National Parks and their states
  * World capitals
* Add a `--reverse` mode: given the name of a Best Picture winner, you provide the year
* Figure out how to display images -- this would allow us to do flags!
