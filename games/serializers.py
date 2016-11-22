from rest_framework import serializers
from games.models import Game, Report, Evaluation

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'info', 'game_url', 'game_img_url')

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ('id','game', 'eval_type', 'result')

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id','game', 'total_answers')
