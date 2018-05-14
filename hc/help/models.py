from django.db import models

class Faqs(models.Model):
    # question_id = models.AutoField(primary_key=True)
    question = models.TextField()
    answer = models.TextField()
    date_created = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True)

    def __str__(self):
        return '%s, %s, %d'%(self.question, self.answer, self.id)

