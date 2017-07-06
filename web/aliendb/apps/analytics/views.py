from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.db.models import Q, Count
from .models import *
from . import reports
from redis import Redis

from datetime import datetime, timedelta
import time

redis = Redis(host='redis', port=6379)


def home(request):
    submissions = Submission.objects.filter(rank__gt=0).order_by('rank')

    # calculate rank deltas
    for submission in submissions:
        rank_delta = submission.rank_previous - submission.rank
        if rank_delta > 0:
            shape = '▲'
            color = 'green'
        elif rank_delta < 0:
            shape = '▼'
            color = 'red'
        else:
            shape = '▬'
            color = 'orange'
        submission.delta_color = color
        submission.delta_string = "%s%d" % (shape, rank_delta)

    return render(request, 'home.html', {
        'page_category': 'posts',
        'submissions': submissions,
    })

def subreddits(request):
    subreddits = Subreddit.objects.all().order_by('-tracked_submissions')[:100]

    return render(request, 'subreddits.html', {
        'page_category': 'subreddits',
        'subreddits': subreddits
    })

def about(request):
    return render(request, 'about.html', {
        'page_category': 'about'
    })

def api(request):
    name = request.GET.get('name', '')

    if name == 'submission':
        data = reports.submission(request)

    return JsonResponse(data)

def submission(request, id):
    try:
        submission = Submission.objects.get(id=id)
    except Submission.DoesNotExist:
        raise Http404("Submission was not found")

    submission_scores = SubmissionScore.objects.filter(submission=submission).order_by('timestamp')

    # lifetime and rise time
    lifetime_delta = submission_scores[len(submission_scores) - 1].timestamp - submission_scores[0].timestamp
    lifetime = time.strftime('%H:%M:%S', time.gmtime(lifetime_delta.seconds))

    rise_time_delta = submission_scores[0].timestamp - submission.created_at
    rise_time = time.strftime('%H:%M:%S', time.gmtime(rise_time_delta.seconds))

    return render(request, 'submission.html', {
        'page_category': 'posts',
        'submission': submission,
        'lifetime': lifetime,
        'rise_time': rise_time,
    })

def subreddit(request, subreddit):
    try:
        subreddit = Subreddit.objects.get(name=subreddit)
    except Subreddit.DoesNotExist:
        raise Http404("Subreddit was not found")
    submissions = Submission.objects.filter(subreddit=subreddit).order_by('-score')

    if len(submissions) == 0:
        raise Http404("Subreddit has no recorded submissions")

    return render(request, 'subreddit.html', {
        'page_category': 'subreddits',
        'subreddit': subreddit,
        'submissions': submissions,
    })

def search(request):
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', '')
    time = request.GET.get('time', '')
    subreddits = request.GET.get('subreddits', '')

    # if no query was given
    if not query:
        return render(request, 'search.html')
    else:
        # strip leading and trailing whitespace
        query = query.strip()

    # determine if query is a link to a submission
    if "//reddit.com" in query or "//www.reddit.com" in query:
        submission_id = query.split('/comments/')[1].split('/')[0]
        return redirect('/submission/%s' % submission_id)
    elif "//redd.it" in query:
        submission_id = query.split('//redd.it/')[1]
        return redirect('/submission/%s' % submission_id)
    else:
        if len(query) < 300:
            # get all matching submissions
            submissions = Submission.objects.filter(title__icontains=query)

            # order submissions
            # order_by == 'relevance' is just the default order
            if order_by == 'karma':
                submissions = submissions.order_by('-score')
            elif order_by == 'comments':
                submissions = submissions.order_by('-num_comments')

            # remove submissions not in time frame
            if time and time != 'all':
                current_time = datetime.utcnow()
                if time == 'today':
                    prev_time = current_time - timedelta(days=1)
                elif time == 'week':
                    prev_time = current_time - timedelta(weeks=1)
                elif time == 'month':
                    prev_time = current_time - timedelta(days=30)
                elif time == 'year':
                    prev_time = current_time - timedelta(days=365)
                else:
                    prev_time = current_time
                submissions = submissions.filter(created_at__gte=prev_time)

            # remove submissions not in requested subreddits
            if subreddits is not None and subreddits is not '':
                subreddit_objs = ['']
                for subreddit in subreddits.split(','):
                    try:
                        subreddit_objs.append(Subreddit.objects.get(name__iexact=subreddit))
                    except Subreddit.DoesNotExist:
                        continue

                # create query which ORs subreddit matches
                query_objs = Q()
                for subreddit in subreddit_objs:
                    query_objs.add(Q(subreddit=subreddit), Q.OR)

                submissions = submissions.filter(query_objs)

        return render(request, 'search.html', {
            'submissions': submissions,
            'query': query,
            'order_by': order_by,
            'time': time,
            'subreddits': subreddits,
        })
