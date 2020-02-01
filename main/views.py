import datetime
import time
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from queues import queues, matches
from django.urls import reverse

from .forms import ProfileForm


def index(request):
    # POST 요청이면 폼 데이터를 처리한다
    if request.method == 'POST':

        # 폼 인스턴스를 생성하고 요청에 의한 데이타로 채운다 (binding):
        # 롤 티어, 국가
        # 응답 받으면 채워 넣고 response

        profile = ProfileForm(request.POST)
        if profile.is_valid():
            match_flag = 0
            profile.profile_id = profile.cleaned_data['profile_id']
            profile.tear = profile.cleaned_data['tear']
            tear = profile.tear
            profile_id = profile.profile_id
            queues[(int(tear)-1)].put(profile.profile_id)
            start = time.time()
            while True:
                values = matches.get(profile.profile_id)
                if values:
                    matches.update({profile.profile_id: None})
                    match_flag = 1
                    break
                if time.time() - start > 180:
                    profile_id = queues[(int(tear) - 1)].get()
                    if profile_id != profile.profile_id:
                        queues[(int(tear) - 1)].put(profile.profile_id)
                    break

            if match_flag == 1:
                return HttpResponseRedirect(f'/chat/{values}?profile_id={profile_id}')
            else:
                context = {
                    'form': profile,
                }

                return render(request, 'main/index.html', context)

    else:
        profile = ProfileForm()

    context = {
        'form': profile,
    }

    return render(request, 'main/index.html', context)
