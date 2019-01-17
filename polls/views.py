# Create your views here.
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse
from collections import namedtuple
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .choices import *

from .models import Invitation, Party
from .forms import PartyForm

def index(request):
	template_name = 'polls/index.html'
	return render(request,template_name)

class ResultsView(generic.DetailView):
	template_name = 'polls/results.html'

def find_code(request):
    if request.method == 'POST' or request.is_ajax():
        inv_code = request.POST.get('invite_code')

        if inv_code is not None:
            try:
                party_id = Party.objects.get(invite_code__iexact=inv_code)
            except Party.DoesNotExist:
                data = {'message': 'Unable to find that code', 'status' : 0}
                return JsonResponse(data)

            results = Invitation.objects.filter(party=party_id.id).values("pk","first_name","last_name","status")
            return render(request, 'polls/results.html', {'results': results, 'status' : 1})

        data = {'message': 'Unable to find that code'}
        return JsonResponse(data)
    else:
        return render(request, 'polls/results.html', {'message': 'how did you even get here'})

def submit_rsvp(request):
    response = {'status': 0, 'message': 'Error processing form, please try again'}
    if request.method == 'POST' or request.is_ajax():
        email_data = []
        for response in _parse_invite_params(request.POST):
            guest = Invitation.objects.get(pk=response.guest_pk)
            guest.status = response.rsvp_choice
            guest.save()
            guest_name = "%s %s" % (guest.first_name, guest.last_name)
            guest_data = {'name': guest_name, 'status': guest.status}
            email_data.append(guest_data)

        subject = 'New RSVP'
        msg_plain = render_to_string('polls/email.txt', {'data': email_data})
        msg_html = render_to_string('polls/email.html', {'data': email_data})
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['rawillia90+rsvp@gmail.com',]
        send_mail( subject, msg_plain, email_from, recipient_list, html_message=msg_html )
        response = {'status': 1}
        return render(request, 'polls/thank-you.html', response)
    return JsonResponse(response)

InviteResponse = namedtuple('InviteResponse', ['guest_pk', 'rsvp_choice'])

def _parse_invite_params(params):
    responses = {}
    for param, value in params.items():
        if param.startswith('rsvp_choice'):
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['rsvp_choice'] = YES if value == 'Yes' else NO
            responses[pk] = response

    for pk, response in responses.items():
        yield InviteResponse(pk, response['rsvp_choice'])


def search(request):
    if request.is_ajax():
        q = request.GET.get('q')
        if q is not None:
            party_ids = Party.objects.filter(invitation__first_name__icontains=q).values_list('id', flat=True)
            results = Invitation.objects.filter(party__id__in=party_ids).values("pk","first_name","last_name","status","party")
            return render(request, 'polls/results.html', {'results': results})

def rsvp(request):
    template_name = 'polls/rsvp.html'
    if request.method == 'POST':
        find_code(request.POST or None)
    else:
        form = PartyForm()

    return render(request,template_name,{'form': form})

def thank_you(request):
    template_name = 'polls/thank-you.html'
    return render(request,template_name)


@login_required
def dashboard(request):
    attending_guests = Invitation.objects.filter(status=YES).order_by('party_id').values('first_name','last_name','party__name','party__invite_code')
    not_coming_guests = Invitation.objects.filter(status=NO).order_by('party_id').values('first_name','last_name','party__name','party__invite_code')
    not_responded_guests = Invitation.objects.filter(status='').order_by('party_id').values('first_name','last_name','party__name','party__invite_code')
    attending_guests = list(attending_guests)
    not_coming_guests = list(not_coming_guests)
    not_responded_guests = list(not_responded_guests)
    return render(request, 'polls/dashboard.html', context={
        'attending_guests': attending_guests,
        'not_coming_guests': not_coming_guests,
        'not_responded_guests': not_responded_guests,
    })

def handler404(request, exception, template_name="polls/404.html"):
    response = render(request, template_name)
    response.status_code = 404
    return response



