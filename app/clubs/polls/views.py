from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from clubs.polls.models import Poll


def show_poll_view(request: HttpRequest, poll_id: int):
    """Render template to display a poll as a form."""

    poll = get_object_or_404(Poll, id=poll_id)

    return render(request, "clubs/polls/poll_form.html", context={"poll": poll})
