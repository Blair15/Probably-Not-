import praw
from praw.models import MoreComments

reddit = praw.Reddit('ProbablyNotBot', 
                     user_agent='testing script by /u/ProbablyNotBot')

## get the Submission model, NOT iterable
submission = reddit.submission(id='7oc5vb')

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
    return alphaComment.find("isitjustme") != -1

## check to see if the comment contains "does any(one|body) else"
def doesAnyoneElsePresent(alphaComment):
    anyBODYelsePresent = alphaComment.find("doesanybodyelse") != -1
    anyONEelsePresent = alphaComment.find("doesanyoneelse") != -1
    return anyBODYelsePresent or anyONEelsePresent

## check the submission title and body to see if iijm and dae is present
##  if this function returns true we're going to post a new top-level reply
def checkTitleAndBody(submission):

    subTitle = submission.title
    alphaTitle = makeAlpha(subTitle)
    bothInTitle = justMePresent(alphaTitle) and doesAnyoneElsePresent(alphaTitle)

    subBody = submission.selftext
    alphaBody = makeAlpha(subBody)
    bothInBody = justMePresent(alphaBody) and doesAnyoneElsePresent(alphaBody) 

    return bothInTitle or bothInBody 

## this function will have to iterate through comments, checking for iijm and dae,
## and if found then post a reply to the comment with our standard response
def checkComments(submission):

    

    submission.comments.replace_more(limit=None)
    





    
## this will list comment breadth-first,
## can't see any advantage to doing depth- vs. breadth-
##submission.comments.replace_more(limit=None)
##for comment in submission.comments.list():



print( reddit.user.me() )
