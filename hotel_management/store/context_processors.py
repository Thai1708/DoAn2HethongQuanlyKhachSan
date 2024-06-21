from .models import RoomType


def room_types(request):
    return {
        'room_types': RoomType.objects.all()
    }