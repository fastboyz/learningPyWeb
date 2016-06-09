from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.db.models import F

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
#       redisplay the question with an error message notifying the user that he did not choose an answer
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        #selected_choice.votes += 1
        ########################################################################################################################
        # If 2 people are saving their votes at the same time, the version upward might cause problems because it is the python
        # BACKEND that is in charge of adding that field, and since we are working in a multithreaded inviroment, the results
        # might notbe what we intend it to be. To fix that, we can use the F() function when adding they vote value, that
        # will overwrite the python code and ask the database to update its values directly
        ########################################################################################################################
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Note: always return an HttpResponseRedirect after a susccesful post, to prevent data from
        # being posted twice if the user press on the back button
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
