from .models import *
import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def bulk(request):
    data = {}
    data.update(activity(request))
    data.update(upvote_ratio(request))
    data.update(special_users(request))
    data.update(gilded(request))
    data.update(polarity(request))
    data.update(subjectivity(request))
    return data

def activity(request):
    id = request.GET.get('id', '')

    submission = Submission.objects.get(id=id)
    submission_scores = SubmissionScore.objects.filter(submission=submission).order_by('timestamp')
    submission_num_comments = SubmissionNumComments.objects.filter(submission=submission).order_by('timestamp')

    scores = [[int((s.timestamp - epoch).total_seconds()) * 1000.0, s.score] for s in submission_scores]
    comments = [[int((c.timestamp - epoch).total_seconds()) * 1000.0, c.num_comments] for c in submission_num_comments]

    data = {
        'activity': {
            'scores': scores,
            'comments': comments
        }
    }

    return data

def upvote_ratio(request):
    id = request.GET.get('id', '')

    submission = Submission.objects.get(id=id)
    subreddit_submissions = Submission.objects.filter(subreddit=submission.subreddit)
    submission_upvote_ratios = SubmissionUpvoteRatio.objects.filter(submission=submission).order_by('timestamp')

    upvote_ratios = [[int((s.timestamp - epoch).total_seconds()) * 1000.0, s.upvote_ratio] for s in submission_upvote_ratios]

    # get average ratio for subreddit
    total_upvote_ratio = 0
    for submission in subreddit_submissions:
        total_upvote_ratio += submission.upvote_ratio
    average_upvote_ratio = total_upvote_ratio / len(subreddit_submissions)
    average_upvote_ratio = float("{0:.2f}".format(average_upvote_ratio))


    data = {
        'upvote_ratio': {
            'upvote_ratios': upvote_ratios,
            'average_upvote_ratio': average_upvote_ratio
        }
    }

    return data

def special_users(request):
    id = request.GET.get('id', '')

    submission = Submission.objects.get(id=id)
    comments = Comment.objects.filter(submission=submission)
    subreddit_submissions = Submission.objects.filter(subreddit=submission.subreddit)

    data_submission = [
        [c.is_op for c in comments].count(True),
        [c.is_mod for c in comments].count(True),
        [c.is_admin for c in comments].count(True),
        [c.is_special for c in comments].count(True)
    ]
    data_subreddit = [
        [c.is_op for c in comments].count(True) / len(subreddit_submissions),
        [c.is_mod for c in comments].count(True) / len(subreddit_submissions),
        [c.is_admin for c in comments].count(True) / len(subreddit_submissions),
        [c.is_special for c in comments].count(True) / len(subreddit_submissions)
    ]

    data = {
        'special_users': {
            'submission': data_submission,
            'subreddit': data_subreddit
        }
    }

    return data

def gilded(request):
    id = request.GET.get('id', '')

    submission = Submission.objects.get(id=id)
    comments = Comment.objects.filter(submission=submission)
    subreddit_submissions = Submission.objects.filter(subreddit=submission.subreddit)
    subreddit_comments = [c for queryset in [Comment.objects.filter(submission_id=s.id) for s in subreddit_submissions] for c in queryset]

    data = {
        'gilded': {
            'data': [
                sum(c.gilded for c in comments),
                sum(c.gilded for c in subreddit_comments) / len(subreddit_submissions)
            ]
        }
    }

    return data

def polarity(request):
    id = request.GET.get('id', '')

    submission = Submission.objects.get(id=id)
    comments = Comment.objects.filter(submission=submission)
    subreddit_submissions = Submission.objects.filter(subreddit=submission.subreddit)
    subreddit_comments = [c for queryset in [Comment.objects.filter(submission_id=s.id) for s in subreddit_submissions] for c in queryset]

    data_submission = [
        submission.polarity,
        sum(c.polarity for c in comments) / len(comments)
    ]
    data_subreddit = [
        sum(s.polarity for s in subreddit_submissions) / len(subreddit_submissions),
        sum(c.polarity for c in subreddit_comments) / len(subreddit_comments)
    ]

    data = {
        'polarity': {
            'submission': data_submission,
            'subreddit': data_subreddit
        }
    }

    return data

def subjectivity(request):
    id = request.GET.get('id', '')

    submission = Submission.objects.get(id=id)
    comments = Comment.objects.filter(submission=submission)
    subreddit_submissions = Submission.objects.filter(subreddit=submission.subreddit)
    subreddit_comments = [c for queryset in [Comment.objects.filter(submission_id=s.id) for s in subreddit_submissions] for c in queryset]

    data_submission = [
        submission.subjectivity,
        sum(c.subjectivity for c in comments) / len(comments)
    ]
    data_subreddit = [
        sum(s.subjectivity for s in subreddit_submissions) / len(subreddit_submissions),
        sum(c.subjectivity for c in subreddit_comments) / len(subreddit_comments)
    ]

    data = {
        'subjectivity': {
            'submission': data_submission,
            'subreddit': data_subreddit
        }
    }

    return data
