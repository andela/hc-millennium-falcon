from django.contrib.auth.decorators import login_required
import requests
from django.shortcuts import get_object_or_404, redirect, render
from hc.help.forms import FaqForm
from django.contrib import messages
from hc.help.models import Faqs
from django.utils import timezone
from datetime import timedelta

def faq(request):
    qns = Faqs.objects.all()
    ctx = {"qns":qns, "page":"help"}

    if "post_question" in request.POST:
        form = FaqForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            answer = form.cleaned_data['answer']
            question = Faqs(question=question, answer=answer)
            question.date_created = timezone.now()
            question.date_modified = timezone.now()
            question.save()
    return render(request, "help/faq.html", ctx)

def videos(request):
    return render(request, "help/videos.html", {"page":"help"})

