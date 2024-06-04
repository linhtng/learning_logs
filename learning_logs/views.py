from django.shortcuts import render, redirect
from .models import Topic
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Show all topics."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """Show a single topic and all its entries."""
    # Query: Use the get() method to retrieve the topic requested by the user.
    topic = Topic.objects.get(id=topic_id)
    # Query: Get all the entries associated with the topic and order them by date_added.
    # The minus sign in front of date_added sorts the results in reverse order, 
    # which will display the most recent entries first.
    entries = topic.entry_set.order_by('-date_added')
    # Store the topic and entries in the context dictionary, which we’ll pass to the template.
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

"""this function takes in the request object as its parameter.
When the user initially requests this page, their browser will send a GET request. 
Once the user has filled out and submitted the form, their browser will submit a POST request.
Depending on the request, we know whether the user is requesting a blank form 
(GET) or asking us to process a completed form (POST).
"""
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            # redirect() function takes in the name of a view and redirects the user to the page associated with that view.
            return redirect('learning_logs:topics')
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

""" The new_entry() view function is similar to new_topic(), 
but it takes an additional parameter: topic_id, which stores the
value it receives from the url. 
"""
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        """ If form is valid, we need to set the entry object's topic attribute
        before saving it to the database. When we call save(), we pass commit=False
        argument to tell Django to create a new entry object and assign it to 
        new_entry without saving it to the database yet. We then set the topic
        attribute of new_entry to the topic we pulled from the database at the beginning of the function.
        Then we call save() with no arguments to save the new entry to the database
        with the correct associated topic.
        """
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            """ The redirect() call requires two arguments: the name of the view
            we want to redirect to and the argument that view function requires
            """
            return redirect('learning_logs:topic', topic_id=topic_id)
    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)