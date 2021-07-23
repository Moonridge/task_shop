import datetime

def get_current_time_to_context(request):
    current_datetime = datetime.datetime.now()
    return {
        'current_datetime': current_datetime
    }
