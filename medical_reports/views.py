from django.shortcuts import render
from esr21_subject.models import *


def adverse_event_report_page(request):
    statistics = []

    visits = SubjectVisit.objects.all()

    for visit in visits:

        adverse_event = AdverseEvent.objects.filter(subject_visit_id=visit.id).first()

        if adverse_event:
            adverse_event_records = AdverseEventRecord.objects.filter(adverse_event_id=adverse_event.id)
            # serious_adverse_event_records = SeriousAdverseEventRecord.objects.filter(serious_adverse_event_id=adverse_event.id)
            statistics.append({
                'subject_identifier': visit.subject_identifier,
                'report_date': adverse_event.created,
                'resolved': adverse_event_records.filter(status='resolved').count() or 0,
                'ongoing': adverse_event_records.filter(status='ongoing').count() or 0,
                'death': 'YES' if adverse_event_records.filter(status='death').count() else "NO",
                'grade_1': adverse_event_records.filter(ae_grade='mild').count() or 0,
                'grade_2': adverse_event_records.filter(ae_grade='moderate').count() or 0,
                'grade_3': adverse_event_records.filter(ae_grade='severe').count() or 0,
                'grade_4': adverse_event_records.filter(ae_grade='life_threatening').count() or 0,
                'grade_5': adverse_event_records.filter(ae_grade='fatal').count() or 0,
                'mild': 0,
                'moderate': 0,
                'severe': 0,

            })

        else:
            continue

    context = {
        'statistics': statistics
    }

    return render(request, 'medical_reports/advent_event.html', context)


def vaccination_report_page(request):

    visits = SubjectVisit.objects.all();
    statistics = []

    for visit in visits:

        subject_identifier = visit.subject_identifier
        contact_details = PersonalContactInfo.objects.filter(subject_identifier=subject_identifier)
        first_dose = VaccinationDetails.objects.filter(subject_visit_id=visit.id, received_dose_before='first_dose')
        second_dose = VaccinationDetails.objects.filter(subject_visit_id=visit.id, received_dose_before='second_dose')

        statistics.append({
            'subject_identifier': subject_identifier,
            'first_dose': "YES" if first_dose.exists() else "NO",
            'second_dose': "YES" if second_dose.exists() else "NO",
            'contact_details': 'contact'
        })

    context = {
        'statistics': statistics
    }

    return render(request, 'medical_reports/vaccination_report.html', context)
