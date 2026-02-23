from django.shortcuts import render, redirect
from pathlib import Path
from django.http import HttpResponse, JsonResponse
from nextServer.forms import UploadFileForm
from nextServer.utilities import parse_csv
from nextServer.models import Person, University
from django.contrib import messages
import os
import environ

def hello_world(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)

def hello(request):
    return HttpResponse("Welcome")

def map_csv_to_person(data):
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


def map_csv_to_university(data):
    return {
        'university_name_cn': data.get('University_Name_CN'),
        'university_name_en': data.get('University_Name_EN'),
        'university_name_local': data.get('University_Name_Local'),
        'city': data.get('City'),
        'url': data.get('URL'),
        'university_abbr': data.get('University_Abbr'),
        'university_other_name': data.get('University_Other_Name'),
        'description_cn': data.get('Description_CN'),
        'description_en': data.get('Description_EN'),
        'unit_cn': data.get('Unit_CN'),
        'unit_en': data.get('Unit_EN'),
        'lon': float(data.get('Lon', 0)),  # Assuming latitude and longitude are present and valid floats
        'lat': float(data.get('Lat', 0)),
        'physical_geography': data.get('Physical_Geography') == '1',
        'human_geography': data.get('Human_Geography') == '1',
        'urban_planning': data.get('Urban_Planning') == '1',
        'gis': data.get('GIS') == '1',
        'rs': data.get('RS') == '1',
        'gnss': data.get('GNSS') == '1',
        'transportation': data.get('Transportation') == '1',
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
        data_type = request.POST.get('data_type', 'person')  # Assuming you have a way to distinguish the data type

        if 'file' in request.FILES:
            if password == CORRECT_PASSWORD:
                if form.is_valid():
                    file = request.FILES['file']
                    file_path = handle_uploaded_file(file)
                    modifications = parse_csv(file_path)

                    # Store modifications in the session for confirmation
                    request.session['modifications'] = modifications
                    request.session['data_type'] = data_type
                    return render(request, 'upload.html', {
                        'form': form, 
                        'modifications': modifications, 
                        'confirm': True, 
                        'password': password,
                        'data_type': data_type
                    })
                else:
                    messages.error(request, "Invalid form data!")
            else:
                messages.error(request, "Incorrect password!")

        elif 'confirm' in request.POST:
            if password == CORRECT_PASSWORD:
                modifications = request.session.get('modifications', [])
                data_type = request.session.get('data_type', 'person')
                
                if data_type == 'person':
                    model = Person
                    map_function = map_csv_to_person
                    id_field = 'people_id'
                else:
                    model = University
                    map_function = map_csv_to_university
                    id_field = 'universities_id'

                # Update the database logic
                for data in modifications:
                    defaults = map_function(data)
                    if data_type == 'university':  # Check if the data type is 'university'
                        obj, created = University.objects.update_or_create(
                            university_name_en=data['University_Name_EN'],  # assuming university_name_en is the indexed field
                            defaults=defaults
                        )
                        if created:
                            print(f"Created new {data_type}: {data['University_Name_EN']}")
                        else:
                            print(f"Updated existing {data_type}: {data['University_Name_EN']}")
                    else:
                        # Continue with the existing logic for persons or any other data types
                        obj, created = model.objects.update_or_create(
                            defaults=defaults,
                            **{id_field: data['Id']}
                        )
                        if created:
                            print(f"Created new {data_type}: {data['Person_Name_EN']}")
                        else:
                            print(f"Updated existing {data_type}: {data['Person_Name_EN']}")

                del request.session['modifications']  # Clear session data
                del request.session['data_type']
                return JsonResponse({'status': 'success', 'updated_records': len(modifications)})
            else:
                messages.error(request, "Incorrect password!")
                return render(request, 'upload.html', {
                    'form': form, 
                    'confirm': True, 
                    'modifications': request.session.get('modifications', []),
                    'data_type': request.session.get('data_type', 'person')
                })

        elif 'cancel' in request.POST:
            # Clear modifications from the session and redirect to the upload page
            if 'modifications' in request.session:
                del request.session['modifications']
                del request.session['data_type']
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
