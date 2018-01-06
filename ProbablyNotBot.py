import praw
from praw.models import MoreComments


def main():

    ## Take a string and process such that only alpha characters remain
    def makeAlpha(comment):
        lowerComment = comment.lower()
        alphaComment = ""
        for character in lowerComment:
            if character.isalpha():
                alphaComment += character 
        return alphaComment

    ## return true if "is it just me" is found within the comment
    def justMePresent(alphaComment):
        iijmIndex = alphaComment.find("isitjustme")
        iijmPresent = (iijmIndex != -1) 
        return  (iijmPresent, iijmIndex)

    ## check to see if the comment contains "does any(one|body) else"
    def doesAnyoneElsePresent(alphaComment):
        anyBODYelsePresent = alphaComment.find("doesanybodyelse")
        anyONEelsePresent = alphaComment.find("doesanyoneelse") 
        if anyBODYelsePresent != -1:
            return (True, anyBODYelsePresent, "body")
        elif anyONEelsePresent != -1:
            return (True, anyONEelsePresent, "one")
        return (False, -1, "") 

    ## return True if we've already replied to the comment passed
    def alreadyReplied(comment):
        authors = []
        for reply in comment.replies:
            authors.append(reply.author)
        probBot = reddit.user.me()
        return probBot in authors

    ## build the markdown formatted comment depending on whether dae or iijm
    ## occurs first in the comment
    def buildReply(daeIndex, iijmIndex, oneOrBody):
        markdownReply = ""
        if (daeIndex < iijmIndex):
            markdownReply += ">Does any" + oneOrBody + " else\n\nProbably.\n\n"
            markdownReply += ">is it just me\n\nProbably not.\n\n"
        else:
            markdownReply += ">Is it just me\n\nProbably not.\n\n"
            markdownReply += ">does any" + oneOrBody + " else\n\nProbably.\n\n"
        markdownReply += "^(Yes, I'm a bot. If I've gone rogue then please contact /u/Buff-Randit and shout at him!)"
        return markdownReply

    ## we want to check both the title and the body of the submission for iijm
    ## and dae, and if present check all top-level authors to make sure we've not
    ## already posted a top-level comment, if not then shit-post.
    ## return True if shit-posted 
    def checkTitleandBody(submission):
        submission.comments.replace_more(limit=None)
        subTitle = submission.title
        subBody = submission.selftext
        alphaTitle = makeAlpha(subTitle)
        alphaBody = makeAlpha(subBody)

        ## check to see if we have a BINGO in either title or body
        iijmPresentTitle, iijmIndexTitle = justMePresent(alphaTitle)
        daePresentTitle, daeIndexTitle, oneOrBodyTitle = doesAnyoneElsePresent(alphaTitle)
        iijmPresentBody, iijmIndexBody = justMePresent(alphaBody)
        daePresentBody, daeIndexBody, oneOrBodyBody = doesAnyoneElsePresent(alphaBody) 

        ## get the info needed to build a reply depending on a title
        ## or body bingo
        if (iijmPresentTitle and daePresentTitle):
            oneOrBody = oneOrBodyTitle
            daeIndex = daeIndexTitle
            iijmIndex = iijmIndexTitle
        elif (iijmPresentBody and daePresentBody):
            oneOrBody = oneOrBodyBody
            daeIndex = daeIndexBody
            iijmIndex = iijmIndexBody

        if (iijmPresentTitle and daePresentTitle) or (iijmPresentBody and daePresentBody):
            ## check to make sure we haven't already posted a top-level comment
            authors = []
            for topLevelComment in submission.comments:
                authors.append(topLevelComment.author)
            probBot = reddit.user.me()
            if probBot not in authors:
                print("***BINGO BANGO***")
                markdownReply = buildReply(daeIndex, iijmIndex, oneOrBody)
                submission.reply(markdownReply)
                print("***posted***")
                return True
        return False 

    ## this function will have to iterate through comments, checking for iijm and dae,
    ## and if found then post a reply to the comment with our standard response only
    ## if we haven't done so before. Return True if shit-post, False if not
    def checkComments(submission):
 
        submission.comments.replace_more(limit=None)

        ## this gives comments breadth-first, can't see any advantage to doing
        ## depth first
        for comment in submission.comments.list():
            commentBody = comment.body
            alphaComment = makeAlpha(commentBody)
            iijmPresent, iijmIndex = justMePresent(alphaComment) 
            daePresent, daeIndex, oneOrBody = doesAnyoneElsePresent(alphaComment)

            if iijmPresent and daePresent:
                if not alreadyReplied(comment) and (comment.author != reddit.user.me()):
                    print("***BINGO BANGO***")
                    print(comment.author)
                    print(commentBody)
                    markdownReply = buildReply(daeIndex, iijmIndex, oneOrBody)
                    comment.reply(markdownReply)
                    return True
        return False 

    ## this only checks a single comment for occurences of iijm and dae
    ## we'll use it in conjunction with comment streams
    def checkSingleComment(comment):
        ## because we're using a comment stream we have to call refresh
        ## on the comment object to get its replies
        ## it seems that refreshing occasionally throws a ClientException
        try:
            comment.refresh()
        except praw.exceptions.ClientException:
            print("SLEEPING FOR 5 SECONDS", comment.permalink())
            time.sleep(5)
            try:
                comment.refresh()
            except:
                return

        commentBody = comment.body
        alphaComment = makeAlpha(commentBody)
        iijmPresent, iijmIndex = justMePresent(alphaComment) 
        daePresent, daeIndex, oneOrBody = doesAnyoneElsePresent(alphaComment)

           
        if iijmPresent and daePresent:
            if not alreadyReplied(comment) and (comment.author != reddit.user.me()):
                print("***BINGO BANGO***")
                print(comment.author)
                print(commentBody)
                markdownReply = buildReply(daeIndex, iijmIndex, oneOrBody)
                comment.reply(markdownReply)

    reddit = praw.Reddit('ProbablyNotBot', 
                          user_agent='testing script by /u/ProbablyNotBot')

    ## These are the subreddits to monitor new posts for BINGOs
    #subredditToCheck = reddit.subreddit('ProbablyNotPractice')

    for comment in reddit.subreddit('FortNiteBR+AskReddit+Funny+2007scape+Videos+Pics+MildlyInteresting').stream.comments():
       checkSingleComment(comment)
       print(comment.fullname)
 

if __name__ == '__main__':
    main()
