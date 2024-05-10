from django.shortcuts import render, redirect
from pathlib import Path
from django.http import HttpResponse, JsonResponse
from nextServer.forms import UploadFileForm
from nextServer.utilities import parse_csv
from nextServer.models import Person
from django.contrib import messages
import os
import environ

def hello_world(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)

def hello(request):
    return HttpResponse("Welcome")

def map_csv_to_model(data):
    return {
        'person_name_cn': data.get('Person_Name_CN'),
        'person_name_en': data.get('Person_Name_EN'),
        'url': data.get('URL'),
        'physical_geography': bool(int(data.get('Physical Geography', 0))),
        'human_geography': bool(int(data.get('Human Geography', 0))),
        'urban_planning': bool(int(data.get('Urban Planning', 0))),
        'gis': bool(int(data.get('GIS', 0))),
        'rs': bool(int(data.get('RS', 0))),
        'gnss': bool(int(data.get('GNSS', 0))),
        'research_interests': data.get('Research Interests'),
        'university': data.get('University'),
        'transportation': bool(int(data.get('Transportation', 0))),
        # Add more fields as necessary
    }

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR.joinpath('.env'))

CORRECT_PASSWORD = env('DB_UPDATE_KEY')

def file_upload(request):
    if request.method == 'POST':
        password = request.POST.get('password', '')
        form = UploadFileForm(request.POST, request.FILES)
        if 'file' in request.FILES:
            if password == CORRECT_PASSWORD:
                if form.is_valid():
                    file = request.FILES['file']
                    file_path = handle_uploaded_file(file)
                    modifications = parse_csv(file_path)

                    # Store modifications in the session for confirmation
                    request.session['modifications'] = modifications
                    return render(request, 'upload.html', {'form': form, 'modifications': modifications, 'confirm': True, 'password': password})
                else:
                    messages.error(request, "Invalid form data!")
                    return render(request, 'upload.html', {'form': form, 'confirm': False})
            else:
                messages.error(request, "Incorrect password!")
                return render(request, 'upload.html', {'form': form, 'confirm': False})

        elif 'confirm' in request.POST:
            if password == CORRECT_PASSWORD:
                modifications = request.session.get('modifications', [])
                # Update the database logic
                for data in modifications:
                    defaults = map_csv_to_model(data)
                    Person.objects.update_or_create(
                        people_id=data['Id'],
                        defaults=defaults
                    )
                del request.session['modifications']  # Clear session data
                return JsonResponse({'status': 'success', 'updated_records': len(modifications), 'details': modifications})

            else:
                messages.error(request, "Incorrect password!")
                return render(request, 'upload.html', {'form': form, 'confirm': True, 'modifications': request.session.get('modifications', [])})

        elif 'cancel' in request.POST:
            # Clear modifications from the session and redirect to the upload page
            if 'modifications' in request.session:
                del request.session['modifications']
            return redirect('file_upload')

    else:
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form, 'confirm': False})

def handle_uploaded_file(f):
    # Create directory if it does not exist
    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)  # This creates the directory

    file_path = os.path.join(upload_dir, f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path
