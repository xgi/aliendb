import datetime
from django.conf import settings
from django.core.cache import cache
from django.http import Http404
from .helpers import *
from .models import *

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
        id: (HTTP parameter) the submission id

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
    score_tallies = [[timestamp_to_ms(s.timestamp), s.score] for s in submission_scores]
    comment_tallies = [[timestamp_to_ms(c.timestamp), c.num_comments] for c in submission_num_comments]

    ## upvote_ratio
    upvote_ratios = [[timestamp_to_ms(s.timestamp), s.upvote_ratio] for s in submission_upvote_ratios]

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

    # cache for 10 minutes
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
        id: (HTTP parameter) the name of the subreddit

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

    today = datetime.date.today()
    start_date = today - datetime.timedelta(weeks=4)

    subreddit_scores = SubredditScore.objects.filter(timestamp__gt=start_date, subreddit=subreddit).order_by('timestamp')
    subreddit_num_comments = SubredditNumComments.objects.filter(timestamp__gt=start_date, subreddit=subreddit).order_by('timestamp')

    ## activity
    score_tallies_raw = [[timestamp_to_ms(s.timestamp), s.score] for s in subreddit_scores]
    comment_tallies_raw = [[timestamp_to_ms(c.timestamp), c.num_comments] for c in subreddit_num_comments]

    # throw out tallies within the same day
    score_tallies = []
    comment_tallies = []
    time_to_beat = 0
    for i in range(len(score_tallies_raw)):
        if score_tallies_raw[i][0] >= time_to_beat:
            score_tallies.append(score_tallies_raw[i])
            comment_tallies.append(comment_tallies_raw[i])
            time_to_beat = score_tallies_raw[i][0] + 86400000

    # calculate differentials
    score_differentials = []
    comment_differentials = []
    for i in range(1, len(score_tallies)):
        score_differentials.append([score_tallies[i][0], score_tallies[i][1] - score_tallies[i-1][1]])
        comment_differentials.append([comment_tallies[i][0], comment_tallies[i][1] - comment_tallies[i-1][1]])

    data = {
        'activity': {
            'scores': score_tallies,
            'comments': comment_tallies,
            'score_differentials': score_differentials,
            'comment_differentials': comment_differentials
        }
    }

    # cache for 10 minutes
    cache.set("subreddit_data_%s" % id, data, 600)

    return data

def cumulative(request) -> dict:
    """Retrieves data needed to generate graphs for the main page.

    Retrieves data for the following categories, accessible by name from the
    base of the returned dict (i.e. data['category']):
        total; average; front

    After retrieving the data, it is temporarily added to the cache. This
    function checks whether the data is available in the cache, and will use it
    if available to save resources.

    Args:
        request: a standard HttpRequest
        timerange: (HTTP parameter) the time range to retrieve data from, can
            be: day; week; fortnight; month; year

    Returns:
        dict: data needed to generate graphs for the main page.
    """
    timerange = request.GET.get('timerange', '')
    if timerange not in ['day', 'week', 'fortnight', 'month', 'year']:
        # should probably be 400
        raise Http404("Invalid timerange parameter")

    # try to get full data variable from cache
    data = cache.get("cumulative_data_%s" % timerange)
    if data is not None and settings.DEBUG is False:
        return data

    # get datetime object for earliest possible date based on range
    today = datetime.date.today()
    if timerange == 'day':
        start_date = today - datetime.timedelta(days=1)
    if timerange == 'week':
        start_date = today - datetime.timedelta(weeks=1)
    elif timerange == 'fortnight':
        start_date = today - datetime.timedelta(weeks=2)
    elif timerange == 'month':
        start_date = today - datetime.timedelta(weeks=4)
    elif timerange == 'year':
        start_date = today - datetime.timedelta(weeks=52)

    total_scores = TotalScore.objects.filter(timestamp__gt=start_date).order_by('timestamp')
    total_num_comments = TotalNumComments.objects.filter(timestamp__gt=start_date).order_by('timestamp')
    average_scores = AverageScore.objects.filter(timestamp__gt=start_date).order_by('timestamp')
    average_num_comments = AverageNumComments.objects.filter(timestamp__gt=start_date).order_by('timestamp')

    ## total
    total_score_tallies = [[timestamp_to_ms(s.timestamp), s.score] for s in total_scores]
    total_comment_tallies = [[timestamp_to_ms(c.timestamp), c.num_comments] for c in total_num_comments]

    ## average
    average_score_tallies = [[timestamp_to_ms(s.timestamp), s.score] for s in average_scores]
    average_comment_tallies = [[timestamp_to_ms(c.timestamp), c.num_comments] for c in average_num_comments]

    ## front
    front_score_tallies = [[tally[0], tally[1] * 100] for tally in average_score_tallies]
    front_comment_tallies = [[tally[0], tally[1] * 100] for tally in average_comment_tallies]

    data = {
        'total': {
            'scores': total_score_tallies,
            'comments': total_comment_tallies
        },
        'average': {
            'scores': average_score_tallies,
            'comments': average_comment_tallies
        },
        'front': {
            'scores': front_score_tallies,
            'comments': front_comment_tallies
        }
    }

    # cache for 1 hour
    cache.set("cumulative_data_%s" % timerange, data, 3600)

    return data
