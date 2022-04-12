from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# class UserRegisterView(generic.CreateView):
    # form_class = UserCreationForm
    # template_name = 'registration/register.html'
    # success_url = reverse_lazy('login')


# def registerView(request):
#     if request.method == "POST":
#        form = UserCreationForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('members:login_url')
#     else:
#         form = UserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})


# def password_change_done(reequest):
  