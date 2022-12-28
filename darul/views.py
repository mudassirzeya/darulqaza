import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
# from django.apps import apps
from .models import CaseType, TimeLine, UserProfile, Court, Judge, Case
from .forms import CaseForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.db import connection
# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("user", password, username)
        user = authenticate(request, username=username, password=password)
        print("us", user)
        if user is not None:
            login(request, user)
            staffProfile = UserProfile.objects.get(user=user)
            usertype = staffProfile.user_type
            if usertype == 'admin':
                return redirect('admin_page')
            elif usertype == 'law':
                return redirect('/')
        else:
            messages.info(request, 'Username or Password is in correct')
    context = {}
    return render(request, 'login.html', context)


@login_required(login_url='user_login')
def add_admin(request):
    admin_user = UserProfile.objects.filter(user_type='admin')
    if request.method == "POST":
        phone = request.POST.get("phone")
        passcode = request.POST.get("passcode")
        name = request.POST.get("name")
        username = request.POST.get("email")
        try:
            already_user = User.objects.get(username=username)
        except Exception:
            already_user = None
            print('user', already_user)
        if already_user is None:
            new_user = User.objects.create_user(
                username=username, password=passcode, first_name=name)
            UserProfile.objects.create(
                user=new_user,
                phone=phone,
                email=username,
                password=passcode,
                user_type='admin',
            )
            return redirect('admin_team')
        else:
            messages.info(
                request, 'This Email Id is already exist in our DataBase')
            return redirect('admin_team')
    context = {'admin_user': admin_user}
    return render(request, "admin_team.html", context)


@login_required(login_url='user_login')
def add_judge(request):
    all_judge = UserProfile.objects.filter(user_type='law')
    all_court = Court.objects.all()
    json_allCourt = serializers.serialize('json', Court.objects.all())

    if request.method == "POST":
        phone = request.POST.get("phone")
        passcode = request.POST.get("passcode")
        name = request.POST.get("name")
        username = request.POST.get("email")
        courts = request.POST.getlist("court")
        print('judge data', courts)
        try:
            already_user = User.objects.get(username=username)
        except Exception:
            already_user = None
            print('user', already_user)
        if already_user is None:
            new_user = User.objects.create_user(
                username=username, password=passcode, first_name=name)
            judge = UserProfile.objects.create(
                user=new_user,
                phone=phone,
                email=username,
                password=passcode,
                user_type='law',
            )
            judge_obj = Judge.objects.create(
                user=judge)
            for court in courts:
                # each_court = Court.objects.get(id=int(court))
                judge_obj.court.add(court)
            return redirect('judges_list')
        else:
            messages.info(
                request, 'This email Id is already exist in our DataBase')
            return redirect('judges_list')
    context = {'judges': all_judge, 'courts': all_court,
               'json_allCourt': json_allCourt}
    return render(request, "judge_list.html", context)


def recieve_judge_id(request):
    if request.method == "POST":
        data = json.loads(request.body)
        judge_id = data["data_obj"]
        # print("data", judge_id)
        judgeProfile = UserProfile.objects.get(id=int(judge_id))
        profile_json = serializers.serialize('json', [judgeProfile])
        judge = Judge.objects.filter(user=judgeProfile)
        # print('con', contact)
        judge_json = serializers.serialize('json', judge)
        print('judge', judge_json)
        return JsonResponse({"msg": "success",
                             "name": judgeProfile.user.first_name,
                             "profile_data": json.loads(profile_json),
                             "judge": json.loads(judge_json)})
    return render(request, "judge_list.html")


def edit_judge(request):
    if request.method == "POST":
        court_id = request.POST.getlist("edit_court")
        user_id = request.POST.get("edit_id")
        user_data = UserProfile.objects.get(id=int(user_id))
        judge_data = Judge.objects.get(user=user_data)
        judge_data.court.clear()
        for court in court_id:
            # each_court = Court.objects.get(id=int(court))
            judge_data.court.add(court)
        return redirect('judges_list')
    context = {}
    return render(request, 'judge_list.html', context)


def edit_court_name(request):
    if request.method == "POST":
        data = json.loads(request.body)
        court_id = data["data_obj"]
        print('court', court_id)
        court = Court.objects.get(id=int(court_id))
        return JsonResponse({"msg": "success", "court_name": court.court_name})
    context = {}
    return render(request, 'court_list.html', context)


@login_required(login_url='user_login')
def add_court(request):
    all_court = Court.objects.all()
    court_list = []
    for court in all_court:
        temp = {}
        all_cases = Case.objects.filter(court=court)
        temp["court"] = court.court_name
        temp['court_id'] = court.id
        temp['total_case'] = all_cases.count()
        temp['judge'] = []
        court_list.append(temp)
        judge = Judge.objects.filter(court=court)
        for each_judge in judge:
            temp['judge'].append(
                each_judge.user.user.first_name + ' - ' + each_judge.user.phone)
    print('court list', court_list)
    if request.method == "POST":
        if 'add_court_name' in request.POST:
            name = request.POST.get("name")
            Court.objects.create(
                court_name=name
            )
        if 'edit_court_name' in request.POST:
            court_id = request.POST.get("court_id")
            court_name = request.POST.get("edited_name")
            court = Court.objects.get(id=int(court_id))
            court.court_name = court_name
            court.save()
        return redirect('court_list')
    context = {'courts': court_list}
    return render(request, "court_list.html", context)


@login_required(login_url='user_login')
def add_case_type(request):
    all_casetype = CaseType.objects.all()
    if request.method == "POST":
        case_type = request.POST.get("name")
        CaseType.objects.create(
            case_type=case_type
        )
        return redirect('case_types')
    context = {'casetype': all_casetype}
    return render(request, "case_type.html", context)


def logout_user(request):
    logout(request)
    return redirect('user_login')


@login_required(login_url='user_login')
def admin_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    usertype = staffProfile.user_type
    if usertype == 'law':
        return redirect('/')
    all_court = Court.objects.all()
    total_court = all_court.count()
    userprofile = UserProfile.objects.filter(user_type='law')
    total_lawyer = userprofile.count()
    context = {'total_court': total_court,
               'total_lawyer': total_lawyer}
    return render(request, "admin_home.html", context)


@login_required(login_url='user_login')
def lawyer_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    usertype = staffProfile.user_type
    if usertype == 'admin':
        return redirect('admin_page')
    judge_Profile = Judge.objects.get(user=staffProfile)
    judge_cases = Case.objects.filter(judge=judge_Profile).order_by('id')
    all_cases = judge_cases
    searched_text = request.GET.get('text')
    casetype_id = request.GET.get('select_casetype')
    try:
        casetype = CaseType.objects.get(id=int(casetype_id))
    except:
        casetype = None
    casestatus = request.GET.get('select_status')
    selectcourt_id = request.GET.get('select_court')
    try:
        selectcourt = Court.objects.get(id=int(selectcourt_id))
    except:
        selectcourt = None

    if 'text' in request.GET or 'select_casetype' in request.GET or 'select_status' in request.GET or 'select_court' in request.GET:
        print('text', request.GET.get('select_status'))

        if casetype:
            all_cases = all_cases.filter(case_type=casetype)
        if casestatus:
            all_cases = all_cases.filter(status=casestatus)
        if selectcourt:
            all_cases = all_cases.filter(court=selectcourt)
        if searched_text:
            split_text = searched_text.split()
            for text in split_text:
                all_cases = all_cases.filter(
                    Q(accused__contains=text) |
                    Q(plaintiff__contains=text) |
                    Q(aditional_text__contains=text) |
                    Q(case_num__contains=text)
                )

    case_type = CaseType.objects.all()
    # print('status', list(Case.CASESTATUS))
    case_status = Case.CASESTATUS
    court_list = judge_Profile.court.all()
    pages = Paginator(all_cases, 10)
    page_num = request.GET.get('page', 1)
    try:
        page = pages.page(page_num)
    except EmptyPage:
        page = pages.page(1)
    context = {'judge_cases': page,
               'case_type': case_type,
               'case_statuss': 'case_status',
               'court_list': court_list,
               'case_status': list(case_status),
               'searched_text': searched_text,
               'casetype': casetype, 'casestatus': casestatus,
               'selectcourt': selectcourt}
    return render(request, "lawyer_home.html", context)


@login_required(login_url='user_login')
def add_new_case(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    usertype = staffProfile.user_type
    judge_qs = Judge.objects.get(user=staffProfile)
    court_list = judge_qs.court.all()
    if usertype == 'admin':
        return redirect('admin_page')
    casetype = CaseType.objects.all()
    courts = Court.objects.all()
    form = CaseForm()
    form.fields['court'].queryset = court_list
    if request.method == "POST":
        form = CaseForm(request.POST)
        if form.is_valid():
            new_case = form.save(commit=False)
            new_case.judge = judge_qs
            new_case.status = 'اندراج معاملہ'
            new_case.save()
            TimeLine.objects.create(
                user=staffProfile,
                case=new_case,
                aditional_text='اندراج معاملہ'
            )
            return redirect('/')
        messages.info(request, 'Something went wrong, please try again')
    context = {'casetype': casetype, 'courts': courts, 'form': form}
    return render(request, "new_case.html", context)


@login_required(login_url='user_login')
def edit_case(request, pk):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    usertype = staffProfile.user_type
    if usertype == 'admin':
        return redirect('admin_page')

    judge_qs = Judge.objects.get(user=staffProfile)
    court_list = judge_qs.court.all()
    case_data = Case.objects.get(id=pk)
    # print('case', case_data.status)
    form = CaseForm(request.POST or None, instance=case_data)
    # form = CaseForm(instance=case_data)
    form.fields['court'].queryset = court_list
    timelines = TimeLine.objects.filter(
        user=staffProfile, case=case_data).order_by('-added_date')
    if request.method == "POST":
        # print("data: ", case_data.status)
        prev_status = case_data.status
        if form.is_valid():
            # print('status', form.cleaned_data.get('status'))
            if form.cleaned_data.get('status') != prev_status:
                TimeLine.objects.create(
                    user=staffProfile,
                    case=case_data,
                    aditional_text='Status Changed to' +
                    ' ' + form.cleaned_data.get('status')
                )
            form.save()
            return redirect('/')

        messages.info(request, 'Something went wrong, please try again')
    # form.fields['case_type'].queryset = CaseType.objects.all()
    context = {'form': form, 'case_data': case_data,
               'timelines': timelines}
    return render(request, "edit_case.html", context)


@login_required(login_url='user_login')
def add_timeline_notes(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    judge_qs = Judge.objects.get(user=staffProfile)
    # timelines = TimeLine.objects.filter(user=judge_qs)
    usertype = staffProfile.user_type
    if usertype == 'admin':
        return redirect('admin_page')
    if request.method == "POST":
        notes = request.POST.get('message')
        case_id = request.POST.get('caseId')
        case = Case.objects.get(id=int(case_id))
        TimeLine.objects.create(
            user=staffProfile,
            case=case,
            aditional_text=notes
        )
        return redirect('edit_case', pk=case_id)

    # form.fields['case_type'].queryset = CaseType.objects.all()
    context = {}
    return render(request, "edit_case.html", context)


@login_required(login_url='user_login')
def overview_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    usertype = staffProfile.user_type
    if usertype == 'admin':
        return redirect('admin_page')
    judge_profile = Judge.objects.get(user=staffProfile)
    status_1 = Case.objects.filter(status='اندراج معاملہ', judge=judge_profile)
    status_2 = Case.objects.filter(
        status='اطلاع اول بنام فریق دوم مع مثنی  درخواست فریق اول', judge=judge_profile)
    status_3 = Case.objects.filter(
        status='فریق دوم  کو اطلاع موصول ہوئی', judge=judge_profile)
    status_4 = Case.objects.filter(
        status='فریق دوم کو اطلاع موصول نہیں ہوئی', judge=judge_profile)
    status_5 = Case.objects.filter(
        status='ادخال بیان تحریری من جانب فریق ثانی', judge=judge_profile)
    status_6 = Case.objects.filter(
        status='اطلاع بنام فریق اول برائے طلبی پتہ فریق دوم و  متعلقین ومعززین فریق دوم', judge=judge_profile)
    status_7 = Case.objects.filter(
        status='اطلاع ثانی بنام فریق دوم / متعلقین  و معززین فریق دوم مع مثنی درخواست', judge=judge_profile)
    status_8 = Case.objects.filter(
        status='تاریخ سماعت اول', judge=judge_profile)
    status_9 = Case.objects.filter(
        status='حاضری فریقین مع گواہان  و اندراج بیانات', judge=judge_profile)
    status_10 = Case.objects.filter(
        status='حاضری فریق اول فقط مع گواہان واندراج بیانات', judge=judge_profile)
    status_11 = Case.objects.filter(
        status='حاضری فریق دوم فقط مع گواہا ن و اندراج بیانات', judge=judge_profile)
    status_12 = Case.objects.filter(
        status='ا طلاع ثالث بنام فریق دوم', judge=judge_profile)
    status_13 = Case.objects.filter(
        status='اشتہار مفقود الخبر ی در اخبار نقیب', judge=judge_profile)
    status_14 = Case.objects.filter(
        status='تاریخ سماعت دوم', judge=judge_profile)
    status_15 = Case.objects.filter(
        status='حاضری فریقین مع گواہان  و اندراج بیانات', judge=judge_profile)
    status_16 = Case.objects.filter(
        status='حاضری فریق اول فقط مع گواہان واندراج بیانات', judge=judge_profile)
    status_17 = Case.objects.filter(
        status='حاضری فریق دوم فقط مع گواہا ن و اندراج بیانات', judge=judge_profile)
    status_18 = Case.objects.filter(
        status='تاریخ سماعت سوم', judge=judge_profile)
    status_19 = Case.objects.filter(
        status='حاضری فریقین مع گواہان  و اندراج بیانات', judge=judge_profile)
    status_20 = Case.objects.filter(
        status='حاضری فریق اول فقط مع گواہان واندراج بیانات', judge=judge_profile)
    status_21 = Case.objects.filter(
        status='حاضری فریق دوم فقط مع گواہا ن و اندراج بیانات', judge=judge_profile)
    status_22 = Case.objects.filter(status='تصفیہ', judge=judge_profile)
    status_23 = Case.objects.filter(
        status='خارج بلا تجویز', judge=judge_profile)
    status_24 = Case.objects.filter(
        status='مصالحت بذریعہ  خلع/ طلاق/ رخصتی', judge=judge_profile)
    status_25 = Case.objects.filter(status='آخری حکم', judge=judge_profile)
    status_26 = Case.objects.filter(
        status='ارسال مثل مرکزی دار القضاء', judge=judge_profile)

    context = {'status_1': status_1.count(), 'status_2': status_2.count(),
               'status_3': status_3.count(), 'status_4': status_4.count(),
               'status_5': status_5.count(), 'status_6': status_6.count(),
               'status_7': status_7.count(), 'status_8': status_8.count(),
               'status_9': status_9.count(), 'status_10': status_10.count(),
               'status_11': status_11.count(), 'status_12': status_12.count(),
               'status_13': status_13.count(), 'status_14': status_14.count(),
               'status_15': status_15.count(), 'status_16': status_16.count(),
               'status_17': status_17.count(), 'status_18': status_18.count(),
               'status_19': status_19.count(), 'status_20': status_20.count(),
               'status_21': status_21.count(), 'status_22': status_22.count(),
               'status_23': status_23.count(), 'status_24': status_24.count(),
               'status_25': status_25.count(), 'status_26': status_26.count(),

               }
    return render(request, "overview.html", context)


@login_required(login_url='user_login')
def cases_overview_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    all_judges = Judge.objects.all()
    all_courts = Court.objects.all()
    case_status = Case.CASESTATUS
    cases = Case.objects.all().order_by('case_type', 'status')
    all_cases = cases
    case_type = CaseType.objects.all()
    searched_judge = request.GET.get('select_judge')
    searched_court = request.GET.get('select_court')
    try:
        judge_obj = Judge.objects.get(id=int(searched_judge))
    except:
        judge_obj = None

    try:
        court_obj = Court.objects.get(id=int(searched_court))
    except:
        court_obj = None

    if 'select_judge' in request.GET or 'select_court' in request.GET:
        if judge_obj:
            all_cases = all_cases.filter(judge=judge_obj)
        if court_obj:
            all_cases = all_cases.filter(court=court_obj)
    final_data = []

    total_status_count = [0]*(len(case_status) + 1)

    for types in case_type:
        case_type_obj = {}
        type_cases = all_cases.filter(case_type=types)
        case_type_obj["case_type"] = types.case_type
        # if type_cases.count() > 0:
        status_count_list = []
        total_count = 0

        count = 1
        for key, val in case_status:
            status_cases_count = type_cases.filter(status=key).count()
            total_count += status_cases_count
            status_obj = {
                "status_count": status_cases_count
            }
            # status_obj['status_name'] = val
            status_count_list.append(status_obj)
            total_status_count[count] = total_status_count[count] + \
                status_cases_count
            count += 1

        case_type_obj["status"] = status_count_list
        case_type_obj['total'] = total_count

        final_data.append(case_type_obj)

        total_status_count[0] = total_status_count[0] + total_count
    context = {'cases': all_cases, 'case_status': list(
        case_status), 'final_data': final_data,
        'total_status_case': total_status_count,
        'all_judges': all_judges, 'all_courts': all_courts,
        'searched_judge': searched_judge, 'searched_court': searched_court
    }
    return render(request, 'cases_dashboard.html', context)


# @login_required(login_url='user_login')
# def overview_page(request):
#     user = request.user
#     staffProfile = UserProfile.objects.get(user=user)
#     judge_profile = Judge.objects.get(user=staffProfile)
#     usertype = staffProfile.user_type
#     if usertype == 'admin':
#         return redirect('admin_page')
#     status_1 = Case.objects.filter(status='اندراج معاملہ')
#     status_2 = Case.objects.filter(
#         status='اطلاع اول بنام فریق دوم مع مثنی  درخواست فریق اول')
#     status_3 = Case.objects.filter(status='فریق دوم  کو اطلاع موصول ہوئی')
#     status_4 = Case.objects.filter(status='فریق دوم کو اطلاع موصول نہیں ہوئی')
#     status_5 = Case.objects.filter(
#         status='ادخال بیان تحریری من جانب فریق ثانی')
#     status_6 = Case.objects.filter(
#         status='اطلاع بنام فریق اول برائے طلبی پتہ فریق دوم و  متعلقین ومعززین فریق دوم')
#     status_7 = Case.objects.filter(
#         status='اطلاع ثانی بنام فریق دوم / متعلقین  و معززین فریق دوم مع مثنی درخواست')
#     status_8 = Case.objects.filter(status='تاریخ سماعت اول')
#     status_9 = Case.objects.filter(
#         status='حاضری فریقین مع گواہان  و اندراج بیانات')
#     status_10 = Case.objects.filter(
#         status='حاضری فریق اول فقط مع گواہان واندراج بیانات')
#     status_11 = Case.objects.filter(
#         status='حاضری فریق دوم فقط مع گواہا ن و اندراج بیانات')
#     status_12 = Case.objects.filter(status='ا طلاع ثالث بنام فریق دوم')
#     status_13 = Case.objects.filter(
#         status='اشتہار مفقود الخبر ی در اخبار نقیب')
#     status_14 = Case.objects.filter(status='تاریخ سماعت دوم')
#     status_15 = Case.objects.filter(
#         status='حاضری فریقین مع گواہان  و اندراج بیانات')
#     status_16 = Case.objects.filter(
#         status='حاضری فریق اول فقط مع گواہان واندراج بیانات')
#     status_17 = Case.objects.filter(
#         status='حاضری فریق دوم فقط مع گواہا ن و اندراج بیانات')
#     status_18 = Case.objects.filter(status='تاریخ سماعت سوم')
#     status_19 = Case.objects.filter(
#         status='حاضری فریقین مع گواہان  و اندراج بیانات')
#     status_20 = Case.objects.filter(
#         status='حاضری فریق اول فقط مع گواہان واندراج بیانات')
#     status_21 = Case.objects.filter(
#         status='حاضری فریق دوم فقط مع گواہا ن و اندراج بیانات')
#     status_22 = Case.objects.filter(status='تصفیہ')
#     status_23 = Case.objects.filter(status='خارج بلا تجویز')
#     status_24 = Case.objects.filter(status='مصالحت بذریعہ  خلع/ طلاق/ رخصتی')
#     status_25 = Case.objects.filter(status='آخری حکم')
#     status_26 = Case.objects.filter(status='ارسال مثل مرکزی دار القضاء')

#     context = {'status_1': status_1.count(), 'status_2': status_2.count(),
#                'status_3': status_3.count(), 'status_4': status_4.count(),
#                'status_5': status_5.count(), 'status_6': status_6.count(),
#                'status_7': status_7.count(), 'status_8': status_8.count(),
#                'status_9': status_9.count(), 'status_10': status_10.count(),
#                'status_11': status_11.count(), 'status_12': status_12.count(),
#                'status_13': status_13.count(), 'status_14': status_14.count(),
#                'status_15': status_15.count(), 'status_16': status_16.count(),
#                'status_17': status_17.count(), 'status_18': status_18.count(),
#                'status_19': status_19.count(), 'status_20': status_20.count(),
#                'status_21': status_21.count(), 'status_22': status_22.count(),
#                'status_23': status_23.count(), 'status_24': status_24.count(),
#                'status_25': status_25.count(), 'status_26': status_26.count(),

#                }
#     return render(request, "overview.html", context)


# def bulk_casetype_upload(request):
#     data = ["مطالبہ فسخ نکاح بوجہ مفقودالخبری وترک کالمعلقہ", "شوہر کا غائب غیر مفقود الخبری کی بنیاد پرفسخ نکاح کا مطالبہ", "مطالبہ فسخ نکاح بوجہ شوہر کا ادائیگی نفقہ سے عاجز ہونا", "شوہر کا استطاعت کے باوجود نفقہ نہ دینے کی وجہ سے فسخ نکاح کا مطالبہ", "مطالبہ فسخ نکاح بوجہ شوہر کا بیوی کو اس کے حقوق واجبہ( وظیفہ زوجیت سکنی ،کسوہ ) ادا نہ کرنے یا ان حقوق کی ادائیگی پر قادر نہ ہونے یا بیمار ہونے پر مناسب علاج نہ کرانے کی وجہ سے فسخ نکاح", "مطالبہ فسخ نکاح بوجہ شوہر کا مجبوب ہونا", "مطالبہ فسخ نکاح بوجہ شوہر کا عنین ہونا", "مطالبہ فسخ نکاح بوجہ شوہر کا مجنون ہونا", "مطالبہ فسخ نکاح بوجہ شوہر کا مجز وم مبروص ہونا یا کسی ایسے مرض میں مبتلا ہونا جس کے باعث بغیر ضرر کے عورت کا اس کے ساتھ رہنا ناممکن ہو، مثلا ایڈز وغیرہ", "مطالبہ فسخ نکاح بوجہ نکاح کا غیر کفو میں ہونا یا غبن فاحش کے ساتھ ہونا", "مطالبہ فسخ نکاح بوجہ نا بالغ کا خیار بلوغ کے حق کو اختیار کرنا", "مطالبہ فسخ نکاح بوجہ عورت کا حرمت مصاہرت سے دو چار ہونا", "مطالبہ فسخ نکاح بوجہ نکاح کے بعد رضاعت کا علم ہو جانا", "مطالبہ فسخ نکاح بوجہ بیوی کو سخت زدوکوب کرنا", "مطالبہ فسخ نکاح بوجہ شقاق و نفرت مابین زن و شو", "مطالبہ فسخ نکاح بوجہ خطر ۂ جان و عفت و عصمت", "مطالبہ انصاف بوجہ عدول حکمی فیصلہ دارالقضاء", "مطالبہ رخصتی زوجہ",
#             "مطالبہ خلع بذریعہ دارالقضاء،مطالبہ نان ونفقہ و بحالی حقوق از دواجی", "حصول حکم بابت حق ولایت ( حق سر پرستی )", "حصول حکم بابت حق حضانت", "حصول اجازت نکاح اولا دصغار", "مطالبہ اصلاح بین المسلمین", "مطالبہ کر ایہ دوکان مسجد وغیرہ", "مطالبہ اشیاء مجہوزہ", "مطالبہ زرمہر وعدت خرچ", "مطالبہ حقیت", "تجویز ثانی اپیل", "مطالبہ تحقیق طلاق", "مطالبہ تحقیق نکاح", "تفویض طلاق", "مطالبہ واپسی ولد", "مطالبہ حل تنازعہ مدرسہ", "حصول اجازت برائے مسلم مسافر خانہ باراضی موقوفہ", "حصول اجازت اراضی مدرسہ برائے تعمیر مسجد", "برائے حصول اجازت اراضی قبرستان ، براۓ تعمیر مسجد", "حصول اجازت نقل اشیاء مسجد براۓ تعمیر", "حصول اجازت اراضی مدرسہ براۓ تو سیع مسجد", "مطالبہ انصاف بابت بحالی ملازمت", "مطالبہ انصاف بابت تنازعہ مار پیٹ", "مطالبہ انصاف بابت امامت و انتظام مسجد وقبرستان", "حصول اجازت بابت تبادلہ اراضی موقوفہ", "اپیل بخلاف فیصلہ قاضی شریعت و مقامی پنچایت", "مطالبہ حصول سند نکاح", "مطالبہ حصول سند اولاد", "مطالبہ حصول سند وارثین", "مطالبہ حصول سند وفات", "مطالبہ حصول سند صحیح العقیده", "مطالبہ حصول ہبہ نامہ", "مطالبہ حصول وصیت نامہ", "اقرار تبدیلی مذہب", "واپسی کا غذات گاڑی از فریق دوم", "مطالبہ تقسیم وراثت", "مطالبہ تقسیم وراثت از مفقود الخبری", "مطالبہ مصالحت بوجہ نزاع بابت مسجد و قبرستان"]

#     for case_type in data:
#         CaseType.objects.create(
#             case_type=case_type
#         )

#     return redirect('case_types')
