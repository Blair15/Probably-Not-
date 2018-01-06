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

## check the submission title and body to see if iijm and dae is present
## if this function returns true we're going to post a new top-level reply
def checkTitleAndBody(submission):

    subTitle = submission.title
    alphaTitle = makeAlpha(subTitle)
    bothInTitle = justMePresent(alphaTitle) and doesAnyoneElsePresent(alphaTitle)

    subBody = submission.selftext
    alphaBody = makeAlpha(subBody)
    bothInBody = justMePresent(alphaBody) and doesAnyoneElsePresent(alphaBody) 

    return bothInTitle or bothInBody 

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
        markdownReply += ">Is it just me\n\nProbably not.\n\n"
    else:
        markdownReply += ">Is it just me\n\nProbably not.\n\n"
        markdownReply += ">Does any" + oneOrBody + " else\n\nProbably.\n\n"
    return markdownReply

## this function will have to iterate through comments, checking for iijm and dae,
## and if found then post a reply to the comment with our standard response only
## if we haven't done so before
def checkComments(submission):

    submission.comments.replace_more(limit=None)

    ## this gives comments breadth-first, can't see any advantage to doing
    ## depth first
    for comment in submission.comments.list():
        commentBody = comment.body
        print(commentBody)
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
            

checkComments(submission)

print( reddit.user.me() )
