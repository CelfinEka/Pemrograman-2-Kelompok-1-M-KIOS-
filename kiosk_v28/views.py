import json
from pathlib import Path
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_http_methods
from .models import V28Snapshot

def _safe_json(obj):
    return json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')

def home(request):
    snap=V28Snapshot.objects.filter(singleton=1).first()
    bootstrap={'data':snap.data if snap else {},'revision':snap.revision if snap else 0,'csrf':get_token(request)}
    content=(Path(__file__).resolve().parent/'v28_served.html').read_text('utf-8')
    # Never interpolate user input as HTML. Only JSON encoded and escaping.
    content=content.replace('__BOOTSTRAP__',_safe_json(bootstrap),1)
    return HttpResponse(content,content_type='text/html; charset=utf-8')

@require_http_methods(['GET','POST'])
def state_api(request):
    if request.method=='GET':
        snap=V28Snapshot.objects.filter(singleton=1).first()
        return JsonResponse({'data':snap.data if snap else {},'revision':snap.revision if snap else 0})
    if len(request.body)>6_000_000:
        return JsonResponse({'error':'Payload terlalu besar'},status=413)
    try:
        payload=json.loads(request.body.decode('utf-8'))
        data=payload['data']
        if not isinstance(data,dict) or any(not isinstance(data.get(k),list) for k in ('tickets','promos','transactions','users')):
            raise ValueError('Format snapshot tidak valid')
        if len(data['transactions'])>100_000 or len(data['tickets'])>5_000:
            raise ValueError('Batas data terlampaui')
    except (ValueError,KeyError,UnicodeDecodeError,TypeError) as exc:
        return JsonResponse({'error':'Data tidak valid'},status=400)
    with transaction.atomic():
        snap,_=V28Snapshot.objects.select_for_update().get_or_create(singleton=1,defaults={'data':{}})
        snap.data=data
        snap.revision+=1
        snap.save(update_fields=['data','revision','updated_at'])
    return JsonResponse({'ok':True,'revision':snap.revision})

def health(request):
    try:
        from django.db import connection
        with connection.cursor() as c:c.execute('SELECT 1')
    except Exception:
        return JsonResponse({'ok':False},status=503)
    return JsonResponse({'ok':True,'version':'V28 exact UI'})
