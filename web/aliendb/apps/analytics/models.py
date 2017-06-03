from django.db import models

class Submission(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=7)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=20)
    rank = models.IntegerField()
    rank_previous = models.IntegerField()
    rank_peak = models.IntegerField()
    karma_peak = models.IntegerField()
    comments_peak = models.IntegerField()
    subreddit = models.CharField(max_length=21)
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

# models with many-to-one relationship with Submission
class Comment(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=7)
    submission = models.ForeignKey(Submission)

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
    submission = models.ForeignKey(Submission)
    score = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class SubmissionNumComments(models.Model):
    submission = models.ForeignKey(Submission)
    num_comments = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class SubmissionUpvoteRatio(models.Model):
    submission = models.ForeignKey(Submission)
    upvote_ratio = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
