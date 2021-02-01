from django.shortcuts import render, redirect
from django.http import JsonResponse
from .controllers.jobs import Jobs
from .models import ConvertJob, Preset
import os

# Create your views here.

def index(request):
    all_jobs = ConvertJob.objects.all().order_by('-id')
    for job in all_jobs:
        if job.status == "running":
            if not Jobs().check_if_actually_running(job.id):
                job.status = "failed"
                job.error_text = "Killed and/or crashed."
                job.save()
    data = {
        'jobs': all_jobs
    }
    return render(request, 'index.html', data)

def new_job(request):
    if request.method == "GET":
        data = {
            'presets': Preset.objects.all()
        }
        return render(request, 'new_job.html', data)
    elif request.method == "POST":
        source = os.path.normpath('Media/' + request.POST['source']) if "source" in request.POST else ""
        working_directory = os.path.dirname(source)
        destination = os.path.normpath(os.path.join(working_directory, request.POST['destination'])) if "destination" in request.POST else ""
        preset_id = request.POST['preset']
        custom_arguments = request.POST['custom_arguments'] if "custom_arguments" in request.POST else ""
        if "overwrite_destination" in request.POST and request.POST['overwrite_destination'].lower() == 'on':
            custom_arguments = "-y " + custom_arguments
        
        Jobs().start_new_job(source, destination, preset_id, custom_arguments)
        return redirect('/')

def view_job(request, id):
    pass_job = ConvertJob.objects.get(id=id)
    return render(request, 'view_job.html', {'job': pass_job})

def job_status(request):
    json_data = []
    for job in ConvertJob.objects.all():
        json_data.append({
            'id': job.id,
            'source': job.source,
            'destination': job.destination,
            'preset': job.preset.name,
            'custom_arguments': job.custom_arguments,
            'error_text': job.error_text,
            'status': job.status,
            'percentage': job.percentage,
            'time_left': job.time_left,
            'speed': job.speed
        })
    return JsonResponse({
        'jobs': json_data
        })

def job_status_specific(request, id):
    json_data = {}
    for job in ConvertJob.objects.all():
        if job.id == id:
            json_data['id'] = job.id
            json_data['source'] = job.source
            json_data['destination'] = job.destination
            json_data['preset'] = job.preset.name
            json_data['custom_arguments'] =job.custom_arguments
            json_data['error_text']= job.error_text
            json_data['status'] = job.status
            json_data['percentage'] = job.percentage
            json_data['time_left'] = job.time_left
            json_data['speed'] = job.speed
    return JsonResponse(json_data)

def job_log(request, id):
    job = ConvertJob.objects.get(id=id)
    if job:
        log = ""
        with open(job.log_location(), 'r') as log_handle:
            log = log_handle.read()
        return JsonResponse({
            "log": log
        })
    
def rerun_job(request, id):
    Jobs().rerun_job(id)
    return redirect('/')

def cancel_job(request, id):
    Jobs().cancel_job(id)
    return redirect('/')

def media_files(request):
    return_dict = {'files': [], 'directories': []}
    path_argument = request.GET['path'] if 'path' in request.GET else ""
    full_path = 'Media/' + path_argument
    if "../" not in full_path:
        if os.path.exists(full_path):
            for path in os.listdir(full_path):
                if os.path.isfile(full_path + '/' + path):
                    return_dict['files'].append(path)
                else:
                    return_dict['directories'].append(path + "/")
            return_dict['files'].sort()
            return_dict['directories'].sort()
        else:
            return JsonResponse({'error': F"Path '{full_path}' does not exist"})
    else:
        return JsonResponse({'error': "'../' not allowed in path!"})
    return JsonResponse(return_dict)