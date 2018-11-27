from django.db import models


class TotalScore(models.Model):
    score = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class TotalNumComments(models.Model):
    num_comments = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class AverageScore(models.Model):
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class AverageNumComments(models.Model):
    num_comments = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Subreddit(models.Model):
    name = models.CharField(primary_key=True, unique=True, max_length=21)
    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=500, blank=True)
    score = models.IntegerField(default=0)
    num_comments = models.IntegerField(default=0)
    tracked_submissions = models.IntegerField(default=0)
    tracked_comments = models.IntegerField(default=0)
    average_upvote_ratio = models.FloatField(default=0)
    average_is_op = models.FloatField(default=0)
    average_is_mod = models.FloatField(default=0)
    average_is_admin = models.FloatField(default=0)
    average_is_special = models.FloatField(default=0)
    average_gilded = models.FloatField(default=0)
    average_submission_polarity = models.FloatField(default=0)
    average_comments_polarity = models.FloatField(default=0)
    average_submission_subjectivity = models.FloatField(default=0)
    average_comments_subjectivity = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Submission(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=7)
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=20)
    rank = models.IntegerField()
    rank_previous = models.IntegerField()
    rank_peak = models.IntegerField()
    score = models.IntegerField()
    num_comments = models.IntegerField()
    polarity = models.FloatField()
    subjectivity = models.FloatField()
    domain = models.CharField(max_length=64)
    link_flair_text = models.CharField(max_length=64)
    upvote_ratio = models.FloatField()
    stickied = models.BooleanField()
    over_18 = models.BooleanField()
    spoiler = models.BooleanField()
    locked = models.BooleanField()

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)


class SubredditScore(models.Model):
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class SubredditNumComments(models.Model):
    subreddit = models.ForeignKey(Subreddit, on_delete=models.CASCADE)
    num_comments = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=7)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)

    score = models.IntegerField()
    is_root = models.BooleanField()
    is_op = models.NullBooleanField()
    is_mod = models.NullBooleanField()
    is_admin = models.NullBooleanField()
    is_special = models.NullBooleanField()
    gilded = models.IntegerField()
    characters = models.IntegerField()
    words = models.IntegerField()
    sentences = models.IntegerField()
    polarity = models.FloatField()
    subjectivity = models.FloatField()

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)


class SubmissionScore(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class SubmissionNumComments(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    num_comments = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class SubmissionUpvoteRatio(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    upvote_ratio = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
