from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db import connections, IntegrityError
from .models import Problem, UserSolvedProblems, Category

# Create your views here.


def index(request):
    return redirect('problems_by_category', 'all')


def get_queryset(database_alias, solution):  # function for evaluating queries
    with connections[f'{database_alias}'].cursor() as cursor:
        try:
            cursor.execute(f'{solution}')
            queryset = []
            for row in cursor:
                queryset.append(row)
            return queryset  # if query works as expected then return result
        except Exception as e:
            s = e.__str__()
            error_code = int(s[1:5])
            if error_code == 1064:  # if there is error in syntax then return a message
                return s[6:-1]
            elif error_code == 1142:  # if there is SQL injection return a message
                return "Only retriev queries allowed!"
            

def test_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    problem = get_object_or_404(Problem, id=pk)
    context = {
            'problem': problem,
        }
    if request.method == "POST":
        context['checked'] = True
        context['is_correct'] = False
        correct_queryset = get_queryset('tables_for_query', problem.solution)
        test_queryset = get_queryset('tables_for_query', request.POST.get('code'))
        if not isinstance(test_queryset, str) and test_queryset:
            if len(correct_queryset) == len(test_queryset):
                context['is_correct'] = True
                for i in range(0, len(correct_queryset)):
                    if correct_queryset[i] != test_queryset[i]:
                        context['is_correct'] = False
                        break
        else:
            context['error_message'] = test_queryset
        if context['is_correct']:
            try:
                UserSolvedProblems.objects.create(user=request.user, problem=problem)
            except IntegrityError:
                pass
    return render(request, 'submit.html', context)


def problems_by_category_view(request, category):
    try:
        category_obj = Category.objects.get(category_name=category)  # get category provided in url
        problem_list = category_obj.problems.order_by('-pub_date')  # get all problems related to the category
        category_name = category.title()
    except Category.DoesNotExist:
        problem_list = Problem.objects.order_by('-pub_date')  # if requested category does not exist return all problems
        category_name = "All"

    paginator = Paginator(problem_list, 10)  # Show 10 contacts per page.
    page_number = request.GET.get('page')
    queryset = paginator.get_page(page_number)

    context = {
        'problems': queryset,
        'category_name': category_name,
    }
    return render(request, 'main.html', context)


def solved_problems_by_current_user_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    problem_list = []
    try:
        user_problems = UserSolvedProblems.objects.order_by('-date').filter(user=request.user)
        for user_problem in user_problems:
            problem_list.append(user_problem.problem)
        paginator = Paginator(problem_list, 10)  # Show 10 contacts per page.
        page_number = request.GET.get('page')
        queryset = paginator.get_page(page_number)
    except UserSolvedProblems.DoesNotExist:
        pass
    context = {
        "problems": queryset,
    }
    return render(request, 'main.html', context)
