from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import re


class Subreddit:

    def __init__(self, name, num_submissions, submission_list, num_submissions_read):
        self.name = name
        self.num_submissions = num_submissions
        self.submission_list = submission_list
        self.num_submissions_read = num_submissions_read


def scrape(reddit_bot, subreddit_names, num_submissions):

    #Set stop words to english
    stop_words = set(stopwords.words('english'))

    submission_list = []
    filtered_submission = []
    filtered_submission_list = []

    subreddit_list = []

    read = 0
    counter = 0

    for subreddit_name in subreddit_names:

        #Get subreddit object
        subreddit = get_subreddit(reddit_bot, subreddit_name)

        print("Gathering top %d submissions from %s..." % (num_submissions, subreddit_name))

        #Gather top level comments from x number of submissions inside of subreddit
        for submission in subreddit.top(limit = num_submissions):

            counter += 1
            
            #print("Submission title: %s (contains %d comments) \n" % (submission.title, len(submission.comments)))

            #Add submission title to list of submissions
            submission_list.append(submission.title)

            #Clean the submission title and tokenize
            submission_tokens = word_tokenize(str(clean(submission.title)))

            #Skip empty submissions
            if(len(submission_tokens) == 0):
                continue

            else:
                read += 1
                #Remove stopwords from tokenized comment
                for word in submission_tokens:
                    if word not in stop_words:
                        filtered_submission.append(word)

                filtered_submission_list.append(' '.join(filtered_submission))

                #print("Filtered comment: %s \n" % str(' '.join(filtered_submission)))

                filtered_submission = []

        print("Successfully parsed %d submissions out of %d --- %.2f \n" % (read, counter, 100*(read/counter)))

        counter = 0
        read = 0

        #Construct list of subreddit objects
        subreddit_list.append(Subreddit(subreddit_name, num_submissions, filtered_submission_list,  len(filtered_submission_list)))

        filtered_submission_list = []

    return subreddit_list

def clean(submission):

    #Remove parentheses
    re_p = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", submission)

    #Remove links
    re_l = re.sub(r"http\S+|([\(\[]).*?([\)\]])", "", re_p)

    #Remove special characters
    re_s = re.sub(r"[^A-Za-z \—]+", " ", re_l)

    #Remove excess white space
    filtered_submission = " ".join(re_s.split())

    return filtered_submission

def get_subreddit(reddit_bot, subreddit_name):
    subreddit_obj = reddit_bot.subreddit(subreddit_name)
    return subreddit_obj


def get_tags(subreddit_objects):

    subreddit_tag_list = []
    numeric_tag_list = []

    print("Gathering submission tags... \n")

    for i in range(len(subreddit_objects)):
        length = len(subreddit_objects[i].submission_list)
        while length > 0:
            subreddit_tag_list.append(subreddit_objects[i].name)
            numeric_tag_list.append(i)
            length -= 1

    print("Successfully tagged: %d submissions \n" % len(subreddit_tag_list))

    return subreddit_tag_list, numeric_tag_list


def bundle_submissions(subreddit_objects):

    bundled_submission_list = []
    
    print("Bundling up submissions... \n")

    for i in range(len(subreddit_objects)):
        for submission in subreddit_objects[i].submission_list:
            bundled_submission_list.append(submission)

    print("Successfully bundled: %d submissions \n" % len(bundled_submission_list))

    return bundled_submission_list