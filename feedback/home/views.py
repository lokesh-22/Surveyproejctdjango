from django.shortcuts import render,redirect
from .models import *
# Create your views here.

def index(request):
    feedbacks = Customerfeedback.objects.all()
    return render(request, 'surveys.html', {'feedbacks': feedbacks})

def customer_feedback(request, id):
    feedback = Customerfeedback.objects.get(id = id)
    if request.method == 'POST':
        for question in feedback.question.all():
            response = customerResponse(feedback = feedback, question = question)
            response.save()
            if question.question_type == 'Text' or question.question_type == 'BigText':
                response.response_text = request.POST.get(f"response_{question.id}")
            else:
                selected_option = request.POST.getlist(f"question_{question.id}")
                response.selected_option.set(selected_option)
            response.save()
            
        return redirect('/thankyou/')
    return render(request, 'survey.html', {'questions': feedback.question.all()})

def thankyou(request):
    return render(request, 'thank_you.html')

