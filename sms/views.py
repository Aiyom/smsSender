from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from parsingOsonSms.parse import logining
from .models import Students, SaveMessage


def index(request):
    time = request.GET.get('time', None)
    date = request.GET.get('date', None)
    kurs = request.GET.get('kurs', None)
    group = request.GET.get('group', None)
    people = Students.objects.filter(dayOfDate=date, timeOfKurs=time, kurs=kurs, group=group)
    return render(request, "pages/students.html", {"people": people})


def listKurs(request):
    return render(request, "pages/list_kurs.html")


def sendSms(request):
    if request.is_ajax():
        if request.POST:
            pk = request.POST['pk']
            number = request.POST['number']
            student = Students.objects.filter(pk=pk)
            studentParentsTel = student[0].telParents
            studentname = student[0].sirname + ' ' + student[0].name + '. '
            if int(number) == 1:
                logining(studentParentsTel, studentname + 'Ба дарс хозир шуд.', params=None)
                saveMsgToServer(Students.objects.get(pk=pk), 'Ба дарс хозир шуд.')
                print('omad')
            else:
                logining(studentParentsTel, studentname + 'Ба дарс хозир НАшуд.', params=None)
                saveMsgToServer(Students.objects.get(pk=pk), 'Ба дарс хозир НАшуд.')
                print('nest')
            return HttpResponse()
        else:
            print("error get ")
    else:
        print("error ajax")


def saveMsgToServer(user, msg):
    msg = SaveMessage.objects.create(id_name=user, data=timezone.now(), typeOfMessage=msg)
    msg.save()