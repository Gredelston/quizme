# QuizMe

I wrote this doohickey to help me memorize certain datasets. Maybe you'll use it, too!

# Usage

To view usage instructions:

```> python quizme.py --help```

To run a quiz on Oscar Best Picture winners:

```> python quizme.py best-picture```

To run a quiz on Oscar Best Picture winners of the 1950s and 1960s:

```> python quizme.py best-picture 1950s 1960s```

To run a challenge for world capitals in South America: that is, see each question exactly once:

```> python quizme.py world-capitals south-america --challenge```

To display a list of categories for the best-picture quiz:

```> python quizme.py best-picture --show-categories```

# Adding data sets
Each data set should be a CSV with the following properties:

* File should live in the data/ dir, and have the .csv extension.
* The first row should be a header containing the following (comma-separated) fieldnames:
  * `prompt`
  * `answer`
  * `categories`
  * `other_answers`
* `prompt` and `answer` are mandatory for every row.
* If `categories` and/or `other_answers` are provided for a row, they should each be a semicolon-delimited string.

# Todo

* Add a few more datasets
  * National Parks and their states
* Add a `--reverse` mode: given the name of a Best Picture winner, you provide the year
  * How would this interface with, say, Olympic host cities, where Athens has hosted in 1896 and 2004? Ditto World Capitals, where both Israel and Palestine claim Jerusalem?
* Figure out how to display images -- this would allow us to do flags!
* Log stats about user's performance (and .gitignore them)
  * Ask more frequently about the questions the user isn't very good at (like on Duolingo!)
* Consolidate other_answers into the answers column
* When you provide an incorrect answer that would have been correct for multiple other answers, the game should tell you *all* the others, not just the first one.

# Other misc notes

* World capitals/countries are a hairy area, and I am not in the business of politics. For now, my definition of a "country" is "anything listed on the Wikipedia article 'List of sovereign states and dependent territories in $CONTINENT', under either the 'Near universally recognised' or 'Substantial, but limited, recognition' list". My definition of a "capital" is "Any city listed for each country (as previously defined) on the Wikipedia article 'List of national capitals', except for Abidjan, which just seems to be there for historical reasons".
