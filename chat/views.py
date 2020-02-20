# chat/views.py

from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    profile_id = request.GET.get('profile_id')
    duo_profile_id = request.GET.get('duo_profile_id')
    # TODO: 전적 검색 창 조합

    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'profile_id_json': mark_safe(json.dumps(profile_id)),
        'duo_profile_id' : mark_safe(duo_profile_id)
    })
