import config
import praw

import submission_scraper as ss
import semantic_analysis as sa

def main():

    #Bot login
    reddit_bot = login()

    #Get user input for which subreddits to analyze
    subreddit_names = list(str(input("Enter the names of the subreddits (separated by commas) that you would like to analyze: ")).split(","))


    print("Analyzing submission titles...\n")

    #Values can be changed to collect more/less data
    num_submissions = 1500

    #Scrape submission titles from chosen subreddits
    subreddit_objects = ss.scrape(reddit_bot, subreddit_names, num_submissions)

    for obj in subreddit_objects:
        print("Subreddit name: ", obj.name, "\n")
        print("Number of submissions: ", obj.num_submissions, "\n")
        #print("Submissions: ", obj.submission_list, "\n")
        print("Number of submissions read: ", obj.num_submissions_read, "\n \n")

    #Bundle together all submission titles from all subreddits
    submissions = ss.bundle_submissions(subreddit_objects)

    #Tag each comment based off of which subreddit it came from
    subreddit_tags, numeric_tags = ss.get_tags(subreddit_objects)

    #Learn comment vocabulary
    #num_strings, text, subreddit_tags, numeric_tags
    sa.run_lsa(len(submissions), submissions, subreddit_tags, numeric_tags)


def login():

    print("Logging in... \n")

    reddit_bot = praw.Reddit(username = config.username,
                        password = config.password,
                        client_id = config.client_id,
                        client_secret = config.client_secret,
                        user_agent = config.user_agent)

    return reddit_bot


if __name__ == '__main__':
    main()