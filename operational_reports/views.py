import datetime
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from esr21_subject.models import EligibilityConfirmation, InformedConsent, ScreeningEligibility
from django.db.models import Q


# Create your views here.
def operational_report_page(request):
    statistics = []
    users = User.objects.all()

    if request.method == 'POST':
        # pprint(request.POST)
        start_date = None
        end_date = None
        if request.POST['start_date'] and request.POST['end_date']:
            start_date = datetime.date.fromisoformat(request.POST['start_date'])
            end_date = datetime.date.fromisoformat(request.POST['end_date'])

        selected_user = request.POST['selected_user']
        if not selected_user == 'all':
            user = User.objects.get(username=selected_user)
            screened = EligibilityConfirmation.objects.filter(user_created=selected_user).count()
            consented = InformedConsent.objects.filter(user_created=selected_user).count()
            eligible = ScreeningEligibility.objects.filter(Q(user_created=selected_user) & Q(is_eligible=True)).count()
            conversion = 0
            if consented:
                conversion = (eligible / consented) * 100

            statistics.append({
                'username': user.username,
                'firstname': user.first_name,
                'lastname': user.last_name,
                'figures': [screened, consented, eligible, round(conversion, 1)]
            })
        elif not selected_user == 'all' and start_date and end_date:
            user = User.objects.get(username=selected_user)
            screened = EligibilityConfirmation.objects.filter(user_created=selected_user,
                                                              created__range=[start_date, end_date]).count()
            consented = InformedConsent.objects.filter(user_created=selected_user,
                                                       created__range=[start_date, end_date]).count()
            eligible = ScreeningEligibility.objects.filter(
                Q(user_created=selected_user.username) & Q(user_created=selected_user) & Q(is_eligible=True), ).count()
            conversion = 0
            if consented:
                conversion = (eligible / consented) * 100

            statistics.append({
                'username': user.username,
                'firstname': user.first_name,
                'lastname': user.last_name,
                'figures': [screened, consented, eligible, round(conversion, 1)]
            })

        if user == all and start_date and end_date:
            for user in users:
                screened = EligibilityConfirmation.objects.filter(user_created=user.username,
                                                                  created__range=[start_date, end_date]).count()
                consented = InformedConsent.objects.filter(user_created=user.username,
                                                           created__range=[start_date, end_date]).count()
                eligible = ScreeningEligibility.objects.filter(
                    Q(user_created=user.username) & Q(user_created=user.name) & Q(is_eligible=True), ).count()
                conversion = 0
                if consented:
                    conversion = (eligible / consented) * 100

                statistics.append({
                    'username': user.username,
                    'firstname': user.first_name,
                    'lastname': user.last_name,
                    'figures': [screened, consented, eligible, round(conversion, 1)]
                })

        context = {
            'statistics': statistics,
            'users': users
        }

        return render(request, 'operational_reports/operational.html', context)

    for user in users:
        # username = user.username
        screened = EligibilityConfirmation.objects.filter(user_created=user.username).count()
        consented = InformedConsent.objects.filter(user_created=user.username).count()
        eligible = ScreeningEligibility.objects.filter(Q(user_created=user.username) & Q(is_eligible=True)).count()
        conversion = 0
        if consented:
            conversion = (eligible / consented) * 100

        statistics.append({
            'username': user.username,
            'firstname': user.first_name,
            'lastname': user.last_name,
            'figures': [screened, consented, eligible, round(conversion, 1)]
        })

    context = {
        'statistics': statistics,
        'users': users
    }
    return render(request, 'operational_reports/operational.html', context)
