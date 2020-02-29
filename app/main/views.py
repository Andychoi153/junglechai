import time
from django.shortcuts import render
from django.http import HttpResponseRedirect
# from queues import matches
from redis_utils import r
from .forms import ProfileForm
from .utils import producer, tear_matrix


def index(request):
    # POST 요청이면 폼 데이터를 처리한다
    if request.method == 'POST':

        # 폼 인스턴스를 생성하고 요청에 의한 데이타로 채운다 (binding):
        # 롤 티어, 국가
        # 응답 받으면 채워 넣고 response

        profile = ProfileForm(request.POST)
        if profile.is_valid():
            match_flag = 0
            profile.lol_id = profile.cleaned_data['lol_id']
            profile.tear = profile.cleaned_data['tear']
            tear = int(profile.tear)
            lol_id = profile.lol_id

            data = {lol_id: {
                        'tear': tear,
                        'tear_matrix': tear_matrix[tear],
                        'time': 0}
                    }

            producer.send('match', value=data)
            start = time.time()

            while True:
                values = r.hgetall(profile.lol_id)
                if values:
                    match_flag = 1
                    r.delete(profile.lol_id)
                    break
                else:
                    if time.time() - start > 300:
                        data = {lol_id: {
                                    'tear': tear,
                                    'tear_matrix': tear_matrix[tear],
                                    'time': 0,
                                    'delete': 1}
                                }
                        producer.send('match', value=data)
                        break
                time.sleep(0.1)

            if match_flag == 1:
                room, duo = list(values.items())[0]
                room = room.decode('utf-8')
                duo = duo.decode('utf-8')

                return HttpResponseRedirect(f'/chat/{room}?profile_id={lol_id}&duo_profile_id={duo}&tear={tear}')
            else:
                context = {
                    'form': profile,
                }

                return render(request, 'main/not_found.html', context)

    else:
        profile = ProfileForm()

    context = {
        'form': profile,
    }

    return render(request, 'main/index.html', context)


def not_found(request):
    # 백 엔드 로직은 index 랑 거의 일치
    # POST 요청이면 폼 데이터를 처리한다
    if request.method == 'POST':

        # 폼 인스턴스를 생성하고 요청에 의한 데이타로 채운다 (binding):
        # 롤 티어, 국가
        # 응답 받으면 채워 넣고 response

        profile = ProfileForm(request.POST)
        if profile.is_valid():
            match_flag = 0
            profile.lol_id = profile.cleaned_data['lol_id']
            profile.tear = profile.cleaned_data['tear']
            tear = int(profile.tear)
            lol_id = profile.lol_id

            data = {lol_id: {
                        'tear': tear,
                        'tear_matrix': tear_matrix[tear],
                        'time': 0}
                    }

            producer.send('match', value=data)
            start = time.time()

            while True:
                values = r.hgetall(profile.lol_id)
                if values:
                    match_flag = 1
                    r.delete(profile.lol_id)
                    break
                else:
                    if time.time() - start > 300:
                        data = {lol_id: {
                                    'tear': tear,
                                    'tear_matrix': tear_matrix[tear],
                                    'time': 0,
                                    'delete': 1}
                                }
                        producer.send('match', value=data)
                        break
                time.sleep(0.1)

            if match_flag == 1:
                room, duo = list(values.items())[0]
                room = room.decode('utf-8')
                duo = duo.decode('utf-8')
                return HttpResponseRedirect(f'/chat/{room}?profile_id={lol_id}&duo_profile_id={duo}&tear={tear}')
            else:
                context = {
                    'form': profile,
                }

                return render(request, 'main/not_found.html', context)

    else:
        profile = ProfileForm()

    context = {
        'form': profile,
    }

    return render(request, 'main/not_found.html', context)
