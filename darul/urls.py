from unicodedata import name
from django.urls import path
from.views import login_page, admin_page, lawyer_page, logout_user, add_admin, add_judge, add_court, add_case_type, add_new_case, recieve_judge_id, edit_case, edit_judge, add_timeline_notes, overview_page, cases_overview_page

urlpatterns = [
    path('user_login/', login_page, name='user_login'),
    path('user_logout/', logout_user, name='user_logout'),
    path('admin_page/', admin_page, name='admin_page'),
    path('admin_team/', add_admin, name='admin_team'),
    path('judges_list/', add_judge, name='judges_list'),
    path('edit_judge/', edit_judge, name='edit_judge'),
    path('court_list/', add_court, name='court_list'),
    path('case_types/', add_case_type, name='case_types'),
    path('', lawyer_page, name='lawyer_page'),
    path('new_case/', add_new_case, name='new_case'),
    path('recieve_judge_id/', recieve_judge_id, name='recieve_judge_id'),
    path('edit_case/<str:pk>/', edit_case, name='edit_case'),
    path('add_notes/', add_timeline_notes, name='add_notes'),
    path('overview_page/', overview_page, name='overview_page'),
    path('cases_overview_page/', cases_overview_page, name='cases_overview_page'),
    # path('bulk_casetype_upload', bulk_casetype_upload,
    #      name='bulk_casetype_upload'),
]
