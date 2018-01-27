import datetime
from django.conf import settings
from django.core.cache import cache
from django.http import Http404
from .models import *

epoch = datetime.datetime.utcfromtimestamp(0)

def submission(request) -> dict:
    """Retrieves data needed to generate graphs for a submission's page.

    Retrieves data for the following categories, accessible by name from the
    base of the returned dict (i.e. data['category']):
        activity; upvote_ratio; special_users; gilded; polarity; subjectivity

    After retrieving the data, it is temporarily added to the cache. This
    function checks whether the data is available in the cache, and will use it
    if available to save resources.

    Args:
        request: a standard HttpRequest;
        id: (HTTP parameter): the submission id

    Returns:
        dict: data needed to generate graphs for the submission page.
    """
    id = request.GET.get('id', '')

    try:
        submission = Submission.objects.get(id=id)
    except Submission.DoesNotExist:
        raise Http404("Submission was not found")

    # try to get full data variable from cache
    data = cache.get("submission_data_%s" % id)
    if data is not None and settings.DEBUG is False:
        return data

    subreddit = submission.subreddit
    comments = Comment.objects.filter(submission=submission)
    submission_scores = SubmissionScore.objects.filter(submission=submission).order_by('timestamp')
    submission_num_comments = SubmissionNumComments.objects.filter(submission=submission).order_by('timestamp')
    submission_upvote_ratios = SubmissionUpvoteRatio.objects.filter(submission=submission).order_by('timestamp')

    ## activity
    score_tallies = [[int((s.timestamp - epoch).total_seconds()) * 1000.0, s.score] for s in submission_scores]
    comment_tallies = [[int((c.timestamp - epoch).total_seconds()) * 1000.0, c.num_comments] for c in submission_num_comments]

    ## upvote_ratio
    upvote_ratios = [[int((s.timestamp - epoch).total_seconds()) * 1000.0, s.upvote_ratio] for s in submission_upvote_ratios]

    ## special_users
    special_users_submission = [
        [c.is_op for c in comments].count(True),
        [c.is_mod for c in comments].count(True),
        [c.is_admin for c in comments].count(True),
        [c.is_special for c in comments].count(True)
    ]
    special_users_subreddit = [
        float("{0:.2f}".format(subreddit.average_is_op)),
        float("{0:.2f}".format(subreddit.average_is_mod)),
        float("{0:.2f}".format(subreddit.average_is_admin)),
        float("{0:.2f}".format(subreddit.average_is_special)),
    ]

    ## gilded
    gilded_submission = sum(c.gilded for c in comments)

    ## polarity
    polarity_submission = [
        float("{0:.4f}".format(submission.polarity)),
        float("{0:.4f}".format(sum(c.polarity for c in comments) / len(comments)))
    ]
    polarity_subreddit = [
        float("{0:.4f}".format(subreddit.average_submission_polarity)),
        float("{0:.4f}".format(subreddit.average_comments_polarity))
    ]

    ## subjectivity
    subjectivity_submission = [
        float("{0:.4f}".format(submission.subjectivity)),
        float("{0:.4f}".format(sum(c.subjectivity for c in comments) / len(comments)))
    ]
    subjectivity_subreddit = [
        float("{0:.4f}".format(subreddit.average_submission_subjectivity)),
        float("{0:.4f}".format(subreddit.average_comments_subjectivity))
    ]

    data = {
        'activity': {
            'scores': score_tallies,
            'comments': comment_tallies
        },
        'upvote_ratio': {
            'upvote_ratios': upvote_ratios,
            'average_upvote_ratio': float("{0:.2f}".format(subreddit.average_upvote_ratio))
        },
        'special_users': {
            'submission': special_users_submission,
            'subreddit': special_users_subreddit
        },
        'gilded': {
            'data': [
                gilded_submission,
                float("{0:.2f}".format(subreddit.average_gilded))
            ]
        },
        'polarity': {
            'submission': polarity_submission,
            'subreddit': polarity_subreddit
        },
        'subjectivity': {
            'submission': subjectivity_submission,
            'subreddit': subjectivity_subreddit
        }
    }

    cache.set("submission_data_%s" % id, data, 600)

    return data

def subreddit(request) -> dict:
    """Retrieves data needed to generate graphs for a subreddit's page.

    Retrieves data for the following categories, accessible by name from the
    base of the returned dict (i.e. data['category']):
        activity

    After retrieving the data, it is temporarily added to the cache. This
    function checks whether the data is available in the cache, and will use it
    if available to save resources.

    Args:
        request: a standard HttpRequest;
        id: (HTTP parameter): the name of the subreddit

    Returns:
        dict: data needed to generate graphs for the submission page.
    """
    id = request.GET.get('id', '')

    try:
        subreddit = Subreddit.objects.get(name=id)
    except Subreddit.DoesNotExist:
        raise Http404("Submission was not found")

    # try to get full data variable from cache
    data = cache.get("subreddit_data_%s" % id)
    if data is not None and settings.DEBUG is False:
        return data

    subreddit_scores = SubredditScore.objects.filter(subreddit=subreddit).order_by('timestamp')
    subreddit_num_comments = SubredditNumComments.objects.filter(subreddit=subreddit).order_by('timestamp')

    ## activity
    score_tallies = [[int((s.timestamp - epoch).total_seconds()) * 1000.0, s.score] for s in subreddit_scores]
    comment_tallies = [[int((c.timestamp - epoch).total_seconds()) * 1000.0, c.num_comments] for c in subreddit_num_comments]

    data = {
        'activity': {
            'scores': score_tallies,
            'comments': comment_tallies
        }
    }

    cache.set("subreddit_data_%s" % id, data, 600)

    return data
