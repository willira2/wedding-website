# Create your views here.
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Question, Choice, Invitation, Party

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions """
		return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

class RsvpView(generic.ListView):
	model = Invitation
	template_name = 'polls/rsvp.html'
	context_object_name = 'guest'

	def get_queryset(self):
		partyObj = Party.objects.get(invitation__first_name__icontains='ann')
		return Invitation.objects.filter(party__id=partyObj.id)

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#redisplay the question voting form
		return render(request, 'polls/detail.html', {
			'question':question,
			'error_message': "You didn't select a choice",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()

		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def get_invitees(self, request, *args, **kwargs):
	query = request.GET.get('q', None)
	if query:			
		partyObj = Party.objects.get(invitation__first_name__icontains=query)
		invObj = Invitation.objects.filter(party__id=partyObj.id).values("pk","name")
		invitees = Product.objects.filter(name__icontains=query).values("pk","name")
		invitees = list(invitees)
		return JsonResponse(invitees, safe=False)
	else:
		return JsonResponse(data={'success': False,'errors': 'No matching names found'})




