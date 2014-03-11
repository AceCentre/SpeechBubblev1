from django import template, http
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, loader, RequestContext
from speechbubble.campaign.models import Campaign, Subscriber, SubscriberList
import forms

def view_online(request, object_id):
    campaign = get_object_or_404(Campaign, pk=object_id, online=True)
    
    if campaign.template.html is not None and campaign.template.html != u"":
        tpl = template.Template(campaign.template.html)
        content_type = 'text/html, charset=utf-8'
    else:
        tpl = template.Template(campaign.template.plain)
        content_type = 'text/plain, charset=utf-8'
        
    return http.HttpResponse(tpl.render(template.Context({})), content_type=content_type)
        
    
def subscribe(request):
    success = False
    if request.method == 'POST':
        form = forms.SubscribeForm(request.POST)
        if form.is_valid():
            subscriber = Subscriber(
                salutation=form.cleaned_data["name"],
                email=form.cleaned_data["email"]
            )
            subscriber.save()
            subscriber_list = SubscriberList.objects.get(name='SpeechBubble Newsletter')
            subscriber_list.subscribers.add(subscriber)
            return http.HttpResponseRedirect('/newsletter/subscribe/outcome/')
    else:
        form = forms.SubscribeForm()
    context = Context({
        'form': form,
    })
    return render_to_response(
        'campaign/subscribe.html', 
        context, 
        context_instance=RequestContext(request)
    )


def subscribe_outcome(request):
    return render_to_response('campaign/subscribe_outcome.html')

    
def unsubscribe(request):
    if request.method == 'POST':
        form = form.UnSubscribeForm(request.POST)
        if form.is_valid():
            return http.HttpResponseRedirect('/newsletter/unsubscribe/outcome/')
    else:
        initial = {}
        if request.GET.get('email'):
            initial['email'] = request.GET.get('email')
        form = forms.UnSubscribeForm(initial=initial)
    context = Context({
        'form': form,
    })
    return render_to_response(
        'campaign/unsubscribe.html', 
        context, 
        context_instance=RequestContext(request)
    )


def unsubscribe_outcome(request):
    return render_to_response('campaign/unsubscribe_outcome.html')
