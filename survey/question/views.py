from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Survey, User, UserSurvey, UserResponses, Question, Answer
from .serializers import SurveySerializers, DetailSurveySerializers, AnswerUserSerializers
from datetime import datetime


class SurveyView(ListAPIView):
    """Отдает список активных опросов"""
    date_now = datetime.today()
    queryset = Survey.objects.filter(date_end__gt=date_now)
    serializer_class = SurveySerializers


class DetailSurveyView(RetrieveAPIView):
    """Отдает опрос по id"""
    queryset = Survey.objects.all()
    serializer_class = DetailSurveySerializers


class StartSurveyView(APIView):
    """Старт опроса"""

    def get(self, request, pk):

        user = request.data.get('user_id')
        survey = Survey.objects.get(pk=pk)
        question_count = Question.objects.filter(survey=pk).count()

        user_survey = UserSurvey(id_survey=get_object_or_404(Survey, id=survey.id),
                                 id_user=get_object_or_404(User, id=user.id),
                                 total_responses=question_count)
        user_survey.save()
        serializer = DetailSurveySerializers(survey)
        return Response({"survey": serializer.data, "user_id": user.id})


class StartSurveyAnonymView(APIView):
    """Старт анонимного опроса"""

    def get(self, request, pk):

        user = User.objects.create()
        survey = Survey.objects.get(pk=pk)
        question_count = Question.objects.filter(survey=pk).count()

        user_survey = UserSurvey(id_survey=get_object_or_404(Survey, id=survey.id),
                                 id_user=get_object_or_404(User, id=user.id),
                                 total_responses=question_count)
        user_survey.save()
        serializer = DetailSurveySerializers(survey)
        return Response({"survey": serializer.data, "user_id": user.id})


class AnswerFromUser(APIView):
    """Получает ответ на вопрос"""

    def post(self, request, pk):

        user_id = request.data.get('user_id')
        response_bool = UserResponses.objects.filter(id_question=pk, id_user=user_id).exists()

        if response_bool == True:
            # проверяет, отвечал пользователь раньше на это вопрос
            return Response({"message": "на этот вопрос Вы уже отвечали"})
        else:
            type_answer = request.data.get('type_answer')
            survey_id = request.data.get('survey_id')
            user_survey = UserSurvey.objects.filter(id_survey=survey_id,
                                                    id_user=user_id)
            total_responses = UserSurvey.objects.filter(id_survey=survey_id,
                                                        id_user=user_id).values_list('total_responses', flat=True)[0]
            current_count_response = UserSurvey.objects.filter(id_survey=survey_id,
                                                               id_user=user_id).values_list('current_count_responses',
                                                                                            flat=True)[0]

            if type_answer == 'One':
                user_answer = request.data.get('answer_id')
                # Создаем ответ пользователя и добавляем туда id опроса, юзера, вопроса и ответа
                user_responses = UserResponses.objects.create()
                user_responses.save()
                user_responses.id_question.add(get_object_or_404(Question, id=pk))
                user_responses.id_user.add(get_object_or_404(User, id=user_id))
                user_responses.id_answer.add(get_object_or_404(Answer, id=user_answer))
                user_responses.id_survey.add(get_object_or_404(Survey, id=survey_id))

                user_responses.save()

                current_count_response += 1
                user_survey.update(current_count_responses=current_count_response)

                if current_count_response == total_responses:
                    return Response({"message": "Ваш ответ записан. Вы ответили на все вопросы. Большое спасибо за участие!"})
                return Response({"message": "Ваш ответ записан"})

            if type_answer == 'Text':
                user_text = request.data.get('text')
                # Создаем ответ пользователя и добавляем туда id опроса, юзера, вопроса и ответа текстом
                user_responses = UserResponses.objects.create()
                user_responses.save()
                user_responses.id_question.add(get_object_or_404(Question, id=pk))
                user_responses.id_user.add(get_object_or_404(User, id=user_id))
                user_responses.id_survey.add(get_object_or_404(Survey, id=survey_id))
                user_responses.text=user_text

                user_responses.save()

                current_count_response += 1
                user_survey.update(current_count_responses=current_count_response)

                if current_count_response == total_responses:
                    return Response({"message": "Ваш ответ записан. Вы ответили на все вопросы. Большое спасибо за участие!"})
                return Response({"message": "Ваш ответ записан"})

            if type_answer == 'Many':
                user_answers = request.data.get('answer_id')
                # Создаем ответ пользователя и добавляем туда id опроса, юзера, вопроса и ответа
                user_responses = UserResponses.objects.create()
                user_responses.save()
                user_responses.id_question.add(get_object_or_404(Question, id=pk))
                user_responses.id_user.add(get_object_or_404(User, id=user_id))
                user_responses.id_survey.add(get_object_or_404(Survey, id=survey_id))

                for answer in user_answers:
                    user_responses.id_answer.add(answer)

                user_responses.save()

                current_count_response += 1
                user_survey.update(current_count_responses=current_count_response)

                if current_count_response == total_responses:
                    return Response({"message": "Ваш ответ записан. Вы ответили на все вопросы. Большое спасибо за участие!"})
                return Response({"message": "Ваш ответ записан"})

            return Response({"message": "тип ответа указан неверный"})


class AnswerUserView(APIView):
    """Отдает ответы ползователя на вопросы опроса"""
    def post(self, request):
        user_id = request.data.get('user_id')
        survey_id = request.data.get('survey_id')

        survey = Survey.objects.get(pk=survey_id)
        answer_user = UserResponses.objects.filter(id_survey=survey_id, id_user=user_id)
        serializer_survey = DetailSurveySerializers(survey)
        serializer_answer = AnswerUserSerializers(answer_user, many=True)
        return Response({"Answer user": serializer_answer.data, "survey": serializer_survey.data})
