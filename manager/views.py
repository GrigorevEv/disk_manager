from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory 
from django.shortcuts import render

from .forms import DiskForm, UserRegistrationForm
from .models import Disk
from .services import DiskManager


@login_required
def disk_manager(request):
    DiskFormSet = modelformset_factory(Disk, form=DiskForm, extra=0)
    formset = DiskFormSet(request.POST or None)
    if formset.is_valid():
        instances = formset.save(commit=False)
        for instance in instances:
            manager = DiskManager(instance)
            manager.mounts_or_umounts_disk()
            manager.formats_disk()
            instance.save()
    return render(request, 'manager/disks.html', {'formset': formset})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})

