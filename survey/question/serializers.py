from rest_framework import serializers
from .models import Answer, Question, Survey, User, UserResponses


class UserAnonymSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id',)


class AnswerSerializers(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id', 'text')


class QuestionSerializers(serializers.ModelSerializer):

    answer = AnswerSerializers(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type_answer', 'answer')


class SurveySerializers(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = ('id', 'date_start', 'date_end', 'description')


class DetailSurveySerializers(serializers.ModelSerializer):

    question = QuestionSerializers(many=True)

    class Meta:
        model = Survey
        fields = ('id', 'date_start', 'date_end', 'description', 'question')


class QuestionForAnswerUserSerializers(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'text')


class AnswerUserSerializers(serializers.ModelSerializer):
    id_answer = AnswerSerializers(many=True)
    id_question = QuestionForAnswerUserSerializers(many=True)

    class Meta:
        model = UserResponses
        fields = ('id', 'id_question', 'id_answer', 'text')
