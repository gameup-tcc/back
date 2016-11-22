from __future__ import unicode_literals

from django.db import models
import json
from django.core.serializers.json import DjangoJSONEncoder

class Game(models.Model):
    name = models.CharField(max_length=50)
    info = models.TextField()
    total_eval = models.IntegerField(default=0)
    game_url = models.URLField(max_length=200, null=True, blank=True)
    game_img_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class JSONField(models.TextField):
    """
    JSONField is a generic textfield that neatly serializes/unserializes
    JSON objects seamlessly.
    Django snippet #1478

    example:
        class Page(models.Model):
            data = JSONField(blank=True, null=True)


        page = Page.objects.get(pk=5)
        page.data = {'title': 'test', 'type': 3}
        page.save()
    """


    def from_db_value(self, value,  expression, connection, content):
        return self.to_python(value)

    def to_python(self, value):
        if value == "":
            return None

        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass
        return value

    def get_db_prep_value(self, value, *args, **kwargs):
        if value == "":
            return None
        if isinstance(value, dict):
            value = json.dumps(value, cls=DjangoJSONEncoder)
            print json.dumps(value, cls=DjangoJSONEncoder)
            print type(value)
        return value

class Evaluation(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    # user = models.ForeignKey('users.Person', on_delete=models.CASCADE)
    result = JSONField(blank=True, null=True)

    # Types of evaluation
    BLOMM = "BL"
    GAMIFICATION = "GA"

    EVALUATION_CHOICE = (
        (BLOMM, 'Bloom'),
        (GAMIFICATION, 'Gamification'),
    )

    eval_type = models.CharField(max_length=3, choices=EVALUATION_CHOICE, default=GAMIFICATION)


class Report(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    total_answers = models.IntegerField()
    # report_result = ?

    def __str__(self):
        return self.game.name

    class Meta:
        order_with_respect_to = 'game'

class BloomReport(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    total_answers = models.IntegerField()
    # report_result = ?

    def __str__(self):
        return self.game.name

    class Meta:
        order_with_respect_to = 'game'

class GamificationReport(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE)
    total_answers = models.IntegerField()
    # report_result = ?

    def __str__(self):
        return self.game.name

    class Meta:
        order_with_respect_to = 'game'
