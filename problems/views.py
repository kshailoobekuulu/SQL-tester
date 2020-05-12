from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db import connections
from .models import Problem

# Create your views here.
def get_queryset(database_alias, solution):
    with connections[f'{database_alias}'].cursor() as cursor:
        try:
            cursor.execute(f'{solution}')
            queryset = []
            for row in cursor:
                queryset.append(row)
            return queryset
        except Exception as e:
            s = e.__str__()
            error_code = int(s[1:5])
            if error_code == 1064:
                return (s[6:-1])
            elif error_code == 1142:
                return "Only retriev queries allowed!"
            

def test_view(request, pk):
    problem = get_object_or_404(Problem, id=pk)
    context = {
            'problem': problem,
        }
    if request.method == "POST":
        context['checked'] = True
        correct_queryset = get_queryset('tables_for_query', problem.solution)
        print(request.POST.get('code'))
        test_queryset = get_queryset('tables_for_query', request.POST.get('code'))
        if not isinstance(test_queryset, str) and test_queryset:
            if len(correct_queryset) == len(test_queryset):
                context['is_correct'] = True
                for i in range(0,len(correct_queryset)):
                    print(test_queryset[i])
                    if correct_queryset[i] != test_queryset[i]:
                        context['is_correct'] = False
                        break
            else:
                context['is_correct'] = False
        else:
            context['error_message'] = test_queryset
    return render(request, 'submit.html', context)

def problems_list_view(request):
    queryset = Problem.objects.all()
    context = {
        'problems': queryset,
    }
    return render(request, 'main.html', context)