from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=100)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    text = models.TextField(db_index=True)
    TYPE_ANSWER = (
        ('One', 'One'),
        ('Many', 'Many'),
        ('Text', 'Text')
    )
    type_answer = models.CharField(max_length=10, choices=TYPE_ANSWER)
    survey = models.ForeignKey(Survey, blank=True, related_name='question', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}'


class Answer(models.Model):
    text = models.TextField(db_index=True)
    question = models.ForeignKey(Question, blank=True, related_name='answer', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}'


class User(models.Model):
    name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f'id: {self.id}, Имя: {self.name} Фамилия: {self.last_name}'


class UserSurvey(models.Model):
    id_survey = models.ForeignKey(Survey, blank=True, related_name='user_survey', on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, blank=True, related_name='user_survey', on_delete=models.CASCADE)
    current_count_responses = models.IntegerField(blank=True, default=0)
    total_responses = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f'Опрос: {self.id_survey}, Пользователь: {self.id_user}'


class UserResponses(models.Model):
    id_survey = models.ManyToManyField(Survey, null=True, blank=True, related_name='user_responses')
    id_question = models.ManyToManyField(Question, null=True, blank=True,  related_name='user_responses')
    id_user = models.ManyToManyField(User, null=True, blank=True,  related_name='user_responses')
    id_answer = models.ManyToManyField(Answer, null=True, blank=True, related_name='user_responses')
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Ответ {self.id_answer} или {self.text} пользователя {self.id_user} на вопрос {self.id_question}'
