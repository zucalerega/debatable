from django.http import HttpResponse, Http404
from .forms import ProfileForm, RawProfileForm
from django.shortcuts import render, get_object_or_404
from .models import Profile

# Create your views here.
def profile_detail_view(request):
	obj = Profile.objects.get(id=1)
	context = {"obj": obj}
	return render(request, "profiles/profile_detail.html", context)

def dynamic_lookup_view(request, id):
	print(id)
	obj = get_object_or_404(Profile, id=id)
	context = {
		"object": obj
	}
	return render(request, "profiles/profile_detail.html", context)

def profile_list_view(request):
	queryset = Profile.objects.all()
	context = {
		"object_list": queryset
	}
	return render(request, "profiles/profile_list.html", context)
# def profile_create_view(request):
# 	form = RawProfileForm()
# 	if request.method == "POST":
# 		form = RawProfileForm(request.POST)
# 		if form.is_valid():
# 			#now data is good
# 			print(form.cleaned_data)
# 			Profile.objects.create(**form.cleaned_data)
# 			form = RawProfileForm()
# 		else:
# 			print(form.errors)
# 	context = {'form': form}
# 	return render(request, "profiles/profile_create.html", context)

# def profile_create_view(request):
# 	print(request.GET)
# 	print(request.POST)

# 	context = {

# 	}
# 	return render(request, "profiles/profile_create.html", context)

def profile_create_view(request, id):
	print(request.user)

	form = ProfileForm(request.POST or None, instance=obj)
	if form.is_valid():
		form.save()
		form = ProfileForm()


	context = {
	'form': form
	}
	return render(request, "profiles/profile_create.html", context)
