from datetime import datetime, timedelta
import time

from django.conf import settings
from django.core.cache import cache
from django.db.models import Q, Count
from django.http import JsonResponse, Http404, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import *
from . import reports


def home(request) -> HttpResponse:
    """View for the index/landing page.

    After rendering the HttpResponse, it is temporarily added to the cache.
    This function checks whether the response is available in the cache,
    and will use it if available to save resources.

    Args:
        request: a standard HttpRequest

    Returns:
        HttpResponse: a standard HttpResponse from templates/home.html
    """
    # try to get response from cache
    response = cache.get("home_response")
    if response is not None and settings.DEBUG is False:
        return response

    submissions = Submission.objects.filter(rank__gt=0).order_by('rank')

    cumulative_stats = {
        'submissions': Submission.objects.all().count(),
        'score': TotalScore.objects.latest('timestamp').score if TotalScore.objects.count() > 0 else 0,
        'comments': TotalNumComments.objects.latest('timestamp').num_comments if TotalNumComments.objects.count() > 0 else 0,
        'subreddits': Subreddit.objects.all().count()
    }

    # calculate rank deltas
    for submission in submissions:
        rank_delta = 0
        if submission.rank_previous != -1 and submission.rank != -1:
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

    response = render(request, 'home.html', {
        'page_category': 'posts',
        'submissions': submissions,
        'cumulative_stats': cumulative_stats
    })
    cache.set("home_response", response, 1200)
    return response


def subreddits(request) -> HttpResponse:
    """View for the subreddits listing page.

    After rendering the HttpResponse, it is temporarily added to the cache.
    This function checks whether the response is available in the cache,
    and will use it if available to save resources.

    Args:
        request: a standard HttpRequest

    Returns:
        HttpResponse: a standard HttpResponse from templates/subreddits.html
    """
    # try to get response from cache
    response = cache.get("subreddits_response")
    if response is not None and settings.DEBUG is False:
        return response

    subreddits = Subreddit.objects.order_by('-tracked_submissions')[:50]
    agreeable_subreddits = Subreddit.objects \
        .exclude(tracked_submissions__lt=30) \
        .order_by('-average_upvote_ratio')[:5]
    controversial_subreddits = Subreddit.objects \
        .exclude(tracked_submissions__lt=30) \
        .order_by('average_upvote_ratio')[:5]

    response = render(request, 'subreddits.html', {
        'page_category': 'subreddits',
        'subreddits': subreddits,
        'agreeable_subreddits': agreeable_subreddits,
        'controversial_subreddits': controversial_subreddits

    })
    cache.set("subreddits_response", response, 1200)
    return response


def about(request) -> HttpResponse:
    """View for the about page.

    Args:
        request: a standard HttpRequest

    Returns:
        HttpResponse: a standard HttpResponse from templates/about.html
    """
    return render(request, 'about.html', {
        'page_category': 'about'
    })


def api(request) -> JsonResponse:
    """View for accessing the public API.

    Args:
        request: a standard HttpRequest;
        name: (HTTP parameter) type of data to retrieve;
        id: (HTTP parameter) identifier for the data, if applicable

    Returns:
        JsonResponse: a JSON formatted data set
    """
    name = request.GET.get('name', '')

    if name == 'submission':
        data = reports.submission(request)
    elif name == 'subreddit':
        data = reports.subreddit(request)
    elif name == 'cumulative':
        data = reports.cumulative(request)

    return JsonResponse(data)


def submission(request, id) -> HttpResponse:
    """View for an individual submission's page.

    After rendering the HttpResponse, it is temporarily added to the cache.
    This function checks whether the response is available in the cache,
    and will use it if available to save resources.

    Args:
        request: a standard HttpRequest;
        id: the submission's id

    Returns:
        HttpResponse: a standard HttpResponse from templates/submission.html
    """
    try:
        submission = Submission.objects.get(id=id)
    except Submission.DoesNotExist:
        raise Http404("Submission was not found")

    # try to get response from cache
    response = cache.get("submission_response_%s" % id)
    if response is not None and settings.DEBUG is False:
        return response

    submission_scores = SubmissionScore.objects.filter(
        submission=submission).order_by('timestamp')

    # lifetime and rise time
    lifetime_delta = submission_scores[len(
        submission_scores) - 1].timestamp - submission_scores[0].timestamp
    lifetime = time.strftime('%H:%M:%S', time.gmtime(lifetime_delta.seconds))

    rise_time_delta = submission_scores[0].timestamp - submission.created_at
    rise_time = time.strftime('%H:%M:%S', time.gmtime(rise_time_delta.seconds))

    response = render(request, 'submission.html', {
        'page_category': 'posts',
        'submission': submission,
        'lifetime': lifetime,
        'rise_time': rise_time,
    })
    cache.set("submission_response_%s" % id, response, 1200)
    return response


def subreddit(request, subreddit) -> HttpResponse:
    """View for an individual subreddit's page.

    After rendering the HttpResponse, it is temporarily added to the cache.
    This function checks whether the response is available in the cache,
    and will use it if available to save resources.

    Args:
        request: a standard HttpRequest;
        subreddit: the name of the subreddit

    Returns:
        HttpResponse: a standard HttpResponse from templates/subreddit.html
    """
    try:
        subreddit = Subreddit.objects.get(name__iexact=subreddit)
    except Subreddit.DoesNotExist:
        raise Http404("Subreddit was not found")

    # try to get response from cache
    response = cache.get("subreddit_response_%s" % subreddit.name)
    if response is not None and settings.DEBUG is False:
        return response

    submissions = Submission.objects.filter(subreddit=subreddit)
    top_submissions = submissions.order_by('-score')[:50]
    recent_submissions = submissions.order_by('-created_at')[:10]
    agreeable_submissions = submissions.order_by('-upvote_ratio')[:5]
    controversial_submissions = submissions.order_by('upvote_ratio')[:5]

    if len(submissions) == 0:
        raise Http404("Subreddit has no recorded submissions")

    response = render(request, 'subreddit.html', {
        'page_category': 'subreddits',
        'subreddit': subreddit,
        'top_submissions': top_submissions,
        'recent_submissions': recent_submissions,
        'agreeable_submissions': agreeable_submissions,
        'controversial_submissions': controversial_submissions
    })
    cache.set("subreddit_response_%s" % subreddit.name, response, 1200)
    return response


def search(request) -> HttpResponse:
    """View for the search page.

    Primitively provides search functionality by retrieving a list of
    submissions which wholly contain the given query. Additionally retrieves
    a list of subreddits based on the subreddit of top results.

    Args:
        request: a standard HttpRequest;
        query: (HTTP parameter) the search query;
        order_by: (HTTP parameter) how to sort the resulting submissions;
        time: (HTTP parameter) time frame which submissions must be within;
        from_subreddits: (HTTP parameter) comma separated list of subreddits

    Returns:
        HttpResponse: a standard HttpResponse from templates/search.html
    """
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', '')
    time = request.GET.get('time', '')
    from_subreddits = request.GET.get('from_subreddits', '')

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
            submissions = Submission.objects.filter(title__search=query)

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
            if from_subreddits is not None and from_subreddits is not '':
                subreddit_objs = ['']
                for from_subreddit in from_subreddits.split(','):
                    try:
                        subreddit_objs.append(Subreddit.objects.get(
                            name__iexact=from_subreddit))
                    except Subreddit.DoesNotExist:
                        continue

                # create query which ORs subreddit matches
                query_objs = Q()
                for subreddit in subreddit_objs:
                    query_objs.add(Q(subreddit=subreddit), Q.OR)

                submissions = submissions.filter(query_objs)

            # get relevant subreddits
            relevant_subreddits = []
            for term in query.split(' '):
                try:
                    subreddit = Subreddit.objects.get(name__iexact=term)
                    relevant_subreddits.append(subreddit.name)
                except Subreddit.DoesNotExist:
                    continue
            for submission in submissions:
                if submission.subreddit.name not in relevant_subreddits:
                    relevant_subreddits.append(submission.subreddit.name)

        return render(request, 'search.html', {
            'submissions': submissions,
            'query': query,
            'order_by': order_by,
            'time': time,
            'from_subreddits': from_subreddits,
            'relevant_subreddits': relevant_subreddits[:8]
        })
