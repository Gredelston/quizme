# QuizMe

I wrote this doohickey to help me memorize certain datasets. Maybe you'll use it, too!

# Usage

To view usage instructions:

```> python main.py --help```

To run a quiz on Oscar Best Picture winners:

```> python main.py best-picture```

To run a quiz on Oscar Best Picture winners of the 1950s and 1960s:

```> python main.py best-picture 1950s 1960s```

To run a challenge for world capitals in South America: that is, see each question exactly once:

```> python main.py world-capitals south-america --challenge```

To display a list of categories for the best-picture quiz:

```> python main.py best-picture --show-categories```

# Adding data sets
Each data set should be a CSV with the following properties:

* File should live in the data/ dir, and have the .csv extension.
  * If you want the file to be .gitignore'd, it should instead live in data/private/.
    * If a CSV in data/private shares its name with a CSV in data/, the game will load the private version.
    * NOTE: These files may not be included in an installed bundle.
* The first row should be a header containing the following (comma-separated) fieldnames:
  * `prompt`
  * `answer`
  * `categories`
  * `other_answers`
* `prompt` and `answer` are mandatory for every row.
* If `categories` and/or `other_answers` are provided for a row, they should each be a semicolon-delimited string.

# Todo

* Polish off the GUI
  * Add the ability to load a data-set after the program has already begun
  * Add the ability to set category filters, probably via a popup
  * Add the ability to set --forced-order or --ask-each-question-once
  * Add a way to display images, which would allow us to do a flags quiz
  * Make it prettier
    * Fonts!
    * Icon!
* Add a few more datasets
  * National Parks and their states
  * Big Four sports teams by city
  * Big Four stadium names
* Add a `--reverse` mode: given the name of a Best Picture winner, you provide the year
  * How would this interface with, say, Olympic host cities, where Athens has hosted in 1896 and 2004? Ditto World Capitals, where both Israel and Palestine claim Jerusalem?
* Log stats about user's performance (and .gitignore them)
  * Ask more frequently about the questions the user isn't very good at (like on Duolingo!)
* Consolidate other_answers into the answers column

# Other misc notes

* World capitals/countries are a hairy area, and I am not in the business of politics. For now, my definition of a "country" is "anything listed on the Wikipedia article 'List of sovereign states and dependent territories in $CONTINENT', under either the 'Near universally recognised' or 'Substantial, but limited, recognition' list". My definition of a "capital" is "Any city listed for each country (as previously defined) on the Wikipedia article 'List of national capitals', except for Abidjan, which just seems to be there for historical reasons".
