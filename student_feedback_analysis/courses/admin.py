from django.contrib import admin
from .models import Subject, FeedbackForm, FormQuestion, FormAnswer, Enroll
# Register your models here.
admin.site.register(Subject)
admin.site.register(Enroll)
admin.site.register(FeedbackForm)
admin.site.register(FormQuestion)
admin.site.register(FormAnswer)




# csv
# teacher, feedbackabout her, label, year, semtype, subject,formtype, score
# 3 15 5-6 ->4 feedbacks per subject by one student

# Review,formquestion