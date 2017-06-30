from django.shortcuts import render, redirect
from .models import User, Poke

# Create your views here.
def index(request):
    print "Inside the index method."

    return render(request,'pybelt_app/main.html')

def result(request):
    print "Inside the result method."

    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        pokes = len(user.poked.all())

        users = User.objects.exclude(id=user.id)

        current_user = User.objects.get(id=user_id)
        context = {
            'current_user': user,
            'users': users,
            'pokes': pokes,
        }

        return render(request, 'pybelt_app/pokes.html', context)
    return redirect('/')

def poke(request, id):
    print "Inside the poke method"

    if request.method =="POST":
        current_user = User.objects.get(id = request.session['user_id'])

        user = User.objects.get(id=id)
        poke = Poke.objects.create(poker=current_user, pokee=user)


        return redirect('/result')
    return redirect('/result')

def logout(request):
    request.session.pop('user_id')
    return redirect('/')

def create(request):
    print "Inside the create method."

    if request.method == "POST":
        form_data = request.POST

        check = User.objects.validate(form_data)
        if check:
            print check
            return redirect('/')
        #valid user data
        user = User.objects.create(
            name = form_data['name'],
            alias = form_data['alias'],
            email = form_data['email'],
            password = form_data['password']
        )

        request.session['user_id'] = user.id

        return redirect('/result')
    return redirect('/')

def login(request):
    print "Inside the login method."

    if request.method == "POST":
        form_data = request.POST

        check = User.objects.login(form_data)

        if type(check) == type(User()):
            request.session['user_id'] = check.id
            return redirect('/result')
        print check
    return redirect('/')
