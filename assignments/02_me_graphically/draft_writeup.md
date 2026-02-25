# Objective

Relevant information
***

    What is your mechanism for "recording" or "mapping" yourself?
    What is your mechanism for organizing, presenting, and explaining?
    What relationships between data are you trying to explore?
    What story is it telling?

There are only three rules:

    No photographs or similar images. This is not a comic book or instagram feed.
    Appropriate content.
    It must be a single graphic composition - one page - though of any size or shape that you want.

***

Along with the visual, include a written description of your work (in a separate document, a page or so (single-spaced)) that explains it and explains your thought process.  What were you after?  How did you go about getting there?  What struggles did you have?  What choices did you make?  Talk about your process and thinking, as well as the outcome.  These written self-reviews on our work will become a standard throughout the course.

## Actual Write up

One of the unexpected perks of joining the Online MSDS program was access to the O'Reilly, which hosted a lot the textbooks and supplemental reading for the program. I've really enjoyed these readings, having the O'Reilly App on my smartphone made it convient to read these instead of doomscroll with downtime. Sometimes while swiping on the screen I imagine turning the actual page of a would be textbook and after finishing a book, I imagine putting it on my bookshelf. 

While I couldn't get actual screentime metrics from my O'Reilly homepage I was able to find some proxy metrics of book "highlights" which included timestamp information. I wanted ot use that to build a chart of what would be my digital book shelf. I wanted to capture the natural variation of my reading along the axis of months and semesters, highlighting the different categories of books that were most read and imagining a larger and larger "cumlative" digitalbook shelf that is starting to come to life as I make my way through these materials. 

To start the process, I sketched out what I wanted on a sheet of paper, just trying to let the image flow. In order to get the metrics into a monthly view I used some basic Python aggregation to make out a Pandas dataframe, using a Claude to generate the starter code. I went and valdiated the times and then just played around with InkScape. I had some trouble getting the book shelf to be "built" over time, I originally wanted it to occur in some some of piecemeal construction or with books getting "added" but instead settled with it growing over time to show cumulative time read. 

I wanted the Data Science data to look at scientific as possible but also being less about the numbers and more about the feel of each semester and each course taken. I wanted to show how some semsters relied more on reading and some more on final projects, which spread time differently.