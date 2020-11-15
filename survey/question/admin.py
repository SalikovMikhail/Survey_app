from django.contrib import admin
from .models import Answer, Question, Survey, User, UserSurvey, UserResponses

admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(User)
admin.site.register(UserSurvey)
admin.site.register(UserResponses)
