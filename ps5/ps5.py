# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: amkil728


import feedparser, string, time, threading, pytz
from project_util import translate_html
from mtTkinter import *
from datetime import datetime


est = pytz.timezone("EST")      # EST Timezone for datetime objects

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, link, pubdate)
        ret.append(newsStory)
    return ret


#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    """Class to store news stories."""

    def __init__(self, guid, title, link, pubdate):
        """
        Initialise a NewsStory object,

        Arguments:
        - guid (string): globally unique identifier for story
        - title (string): story's title
        - link (string): link to story's web page
        - pubdate (datetime): date of publication of story

        A NewsStory object has corresponding attributes:
            self.guid, self.title, self.link, self.pubdate
        """

        # Initialise attributes for NewsStory object
        self.guid, self.title = guid, title
        self.link, self.pubdate = link, pubdate


    def get_guid(self):
        '''Returns the story's guid.'''

        return self.guid


    def get_title(self):
        '''Returns the title of the story.'''

        return self.title


##    def get_description(self):
##        '''Return the story's description.'''
##
##        return self.description


    def get_link(self):
        '''Return the link to the webpage containing the story.'''

        return self.link


    def get_pubdate(self):
        '''Return a datetime object representing the publication date of the story.'''

        return self.pubdate



#======================
# Triggers
#======================

class Trigger(object):
    """Interface for trigger classes."""

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError



# PHRASE TRIGGERS

# Problem 2

class PhraseTrigger(Trigger):
    """
    Abstract class for phrase triggers, i.e, triggers that fire
    whenever a particular phrase is detected in some text.
    """

    def __init__(self, phrase):
        """
        You should never directly instantiate a PhraseTrigger.
        Instead, create a subclass of PhraseTrigger that
        uses the is_phrase_in method to detect the specified phrase in a
        particular field of the story.

        phrase (string): phrase to be detected in text to fire trigger

        Attributes: self.phrase
        """

        # Initialise object, converting phrase to lower case for case insensitive
        # detection
        self.phrase = phrase.lower()


    def is_phrase_in(self, text):
        """
        Returns True if the phrase is in the given text, and False otherwise.
        Only considers the phrase to be present if each word in the phrase
        appears as it is, consecutively in the text, separated only by spaces
        or punctuation, and ignores case.
        """

        # Split phrase into first word and list of remaining words
        first, *rest = self.phrase.split()

        # Remove all punctuation from text
        text_no_punctuation = ''
        for char in text:
            if char in string.punctuation:
                text_no_punctuation += ' '
            else:
                text_no_punctuation += char

        # Split text into lowercase words
        words = [word.lower() for word in text_no_punctuation.split()]

        # Keep track of position to start looking from
        start = 0

        # Repeat the following steps
        while True:
            # Try to find element in list after index start
            try:
                index = words.index(first, start)

            # If element is not found
            except ValueError:
                # End loop
                break

            # For each remaining word of phrase
            for word in rest:
                # If list does not have remaining items
                if len(words) == index + 1:
                    # Return to main loop
                    break

                # If it is next word in list
                if words[index + 1] == word:
                    # Update index to index of current word
                    index += 1

                # Otherwise
                else:
                    # Phrase has not been found, return to main loop
                    break
            # If each word was found
            else:
                # Phrase has been found
                return True

            # Update start to after current index
            start = index + 1

        # The phrase does not appear in the text
        return False



# Problem 3

class TitleTrigger(PhraseTrigger):
    """
    Class for creating title triggers, i.e., triggers that fire whenever a
    given phrase is found in the title of a story.
    """

    def __init__(self, phrase):
        """
        Initialise a TitleTrigger object.

        phrase (string): phrase to be detected in title to fire trigger

        Attributes: self.phrase
        """

        # Initialise object using constructor for superclass PhraseTrigger
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        """
        Returns True if an alert should be generated for the given
        news item, or False otherwise. An alert should be generated if the
        story's title contains the phrase specified for the trigger.

        story (NewsStory): NewsStory object representing a news item
        """

        # Check if phrase is in story's title, using is_phrase_in method
        # from PhraseTrigger
        return self.is_phrase_in(story.get_title())



# Problem 4

class DescriptionTrigger(PhraseTrigger):
    """
    Class for creating description triggers, i.e., triggers that fire
    whenever a given phrase is found in the description of a story.
    """

    def __init__(self, phrase):
        """
        Initialise a DescriptionTrigger object.

        phrase (string): phrase to be detected in description to fire trigger

        Attributes: self.phrase
        """

        # Initialise object using constructor for superclass PhraseTrigger
        PhraseTrigger.__init__(self, phrase)


    def evaluate(self, story):
        """
        Returns True if an alert should be generated for the given
        news item, or False otherwise. An alert should be generated if the
        story's description contains the phrase specified for the trigger.

        story (NewsStory): NewsStory object representing a news item
        """

        # Check if phrase is in story's description, using is_phrase_in method
        # from PhraseTrigger
        return self.is_phrase_in(story.get_description())


# TIME TRIGGERS

# Problem 5

class TimeTrigger(Trigger):
    """
    Abstract class for triggers that fire based on the time of publication
    of a story.
    """

    def __init__(self, time):
        """
        Initialises a TimeTrigger object, with a single attribute time, which
        is a datetime object representing a particular time.
        Note that you should never instantiate TimeTrigger directly, as it is
        an abstract class.
        Instead, subclass TimeTrigger to a concrete class, and instantiate
        objects of that class.

        time (string): string representing EST date and time, in the format
                DD Mon YYYY HH:MM:SS
                e.g., 11 Oct 2021 18:35:15, 3 Feb 1997 06:12:00

        attribute: self.time, datetime object representing specified time.
        """

        # Define format for date and time
        datetime_format = '%d %b %Y %H:%M:%S'

        # Create datetime object representing given time
        time_datetime = datetime.strptime(time, datetime_format)

        # Assign time attribute to self
        self.time = time_datetime



# Problem 6

class BeforeTrigger(TimeTrigger):
    """
    Class to create triggers that fire when a story is published strictly before
    the time specified in the trigger.
    """

    def __init__(self, time):
        """
        Initialises a BeforeTrigger object.

        time: time (string): string representing EST date and time, in the format
                DD Mon YYYY HH:MM:SS

        attributes: self.time, datetime object representing specified time
        """

        # Initialise using constructor for superclass TimeTrigger
        TimeTrigger.__init__(self, time)


    def evaluate(self, story):
        """
        Returns True if an alert should be generated, which is if the story was
        published strictly before the time specified for the trigger,
        or False otherwise.
        """

        # If story publication date has specified timezone
        if story.pubdate.tzinfo:
            # Add timezone knowledge to trigger time (EST)
            time = self.time.replace(tzinfo=est)
        else:
            time = self.time

        # Compare story publication date and time for trigger
        return story.pubdate < time



class AfterTrigger(TimeTrigger):
    """
    Class to create triggers that fire when a story is published strictly after
    the time specified in the trigger.
    """

    def __init__(self, time):
        """
        Initialises a AfterTrigger object.

        time: time (string): string representing EST date and time, in the format
                DD Mon YYYY HH:MM:SS

        attributes: self.time, datetime object representing specified time
        """

        # Initialise using constructor for superclass TimeTrigger
        TimeTrigger.__init__(self, time)


    def evaluate(self, story):
        """
        Returns True if an alert should be generated, which is if the story was
        published strictly after the time specified for the trigger,
        or False otherwise.
        """

        # If story publication date has specified timezone
        if story.pubdate.tzinfo:
            # Add timezone knowledge to trigger time (EST)
            time = self.time.replace(tzinfo=est)
        else:
            time = self.time

        # Compare story publication date and time for trigger
        return story.pubdate > time

# COMPOSITE TRIGGE

# Problem 7

class NotTrigger(Trigger):
    """
    Class to create triggers that invert the output of another trigger. That is,
    given a trigger, we can define an instance of NotTrigger, which fires only
    when the other trigger does NOT fire.
    """

    def __init__(self, target):
        """
        Initialises an instance of NotTrigger.

        target (Trigger): trigger whose output is to be inverted

        attributes: self.target
        """

        self.target = target


    def evaluate(self, story):
        """
        Inverts the output of the target trigger. That is,
        returns True  if self.target.evaluate(story) is False,
            and False if self.target.evaluate(story) is True
        """

        target = self.target

        return not target.evaluate(story)



# Problem 8

class AndTrigger(Trigger):
    """
    Class to create AndTriggers. An AndTrigger takes two other triggers as
    arguments to its constructor, and fires on a news story only if BOTH
    of these triggers would fire on that story."""

    def __init__(self, trigger1, trigger2):
        """
        Initialises an instance of AndTrigger.

        trigger1, trigger2: triggers

        attributes: self.trigger1, self.trigger2"""

        # Initialise attributes
        self.trigger1, self.trigger2 = trigger1, trigger2


    def evaluate(self, story):
        """
        Returns True if an alert should be generated, which is whenever
        T1.evaluate(story) and T2.evaluate(story) are True,
        and False otherwise.
        (where T1 and T2 are self.trigger1 and self.trigger2)
        """

        # Evaluate trigger1 and trigger2
        trigger1_fires = self.trigger1.evaluate(story)
        trigger2_fires = self.trigger2.evaluate(story)

        # Return True only if both are True
        return trigger1_fires and trigger2_fires



# Problem 9

class OrTrigger(Trigger):
    """
    Class to create OrTriggers. An OrTrigger takes two other triggers as
    arguments to its constructor, and fires on a news story if EITHER (or both)
    of these triggers would fire on that story."""

    def __init__(self, trigger1, trigger2):
        """
        Initialises an instance of OrTrigger.

        trigger1, trigger2: triggers

        attributes: self.trigger1, self.trigger2"""

        # Initialise attributes
        self.trigger1, self.trigger2 = trigger1, trigger2


    def evaluate(self, story):
        """
        Returns True if an alert should be generated, which is whenever either
        T1.evaluate(story) or T2.evaluate(story) is True (or both),
        and False if both are False.
        (where T1 and T2 are self.trigger1 and self.trigger2)
        """

        # Evaluate trigger1 and trigger2
        trigger1_fires = self.trigger1.evaluate(story)
        trigger2_fires = self.trigger2.evaluate(story)

        # Return True if either is True
        return trigger1_fires or trigger2_fires


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    return stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!



SLEEPTIME = 30 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Biden")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

