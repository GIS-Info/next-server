import json
import logging

from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger('django')
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.db import connection

@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def get_school_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.University_Name_CN, u.University_Name_EN, u.University_Name_Local, 
            u.City, u.URL, u.University_Abbr, u.University_Other_Name, 
            u.Description_CN, u.Description_EN, u.Unit_CN, u.Unit_EN, u.Lon, u.Lat, 
            u.Universities_id, c.City_Name_CN, c.City_Name_EN, c.Country, c.Lat, c.Lon,
            c.City_Name_Other, c.City_id, c.Country_EN, co.Country_Name_CN, co.Country_Name_EN, 
            co.Continent, co.Country_id, co.Continent_EN, p.Person_Name_CN, p.Person_Name_EN, p.URL, 
            p.Physical_Geography, p.Human_Geography, p.Urban_Planning, p.GIS, p.RS, p.GNSS, p.Research_Interests, p.people_id
            FROM new_Universities u 
            LEFT JOIN new_city c ON u.City = c.City_Name_EN
            LEFT JOIN new_country co ON c.Country = co.Country_Name_CN
            LEFT JOIN new_people p ON u.University_Name_EN = p.University
        """)
        rows = cursor.fetchall()

    data = []
    for row in rows:
        data.append({
            'University_Name_CN': row[0],
            'University_Name_EN': row[1],
            'University_Name_Local': row[2],
            'University_City': row[3],
            'University_URL': row[4],
            'University_Abbr': row[5],
            'University_Other_Name': row[6],
            'Description_CN': row[7],
            'Description_EN': row[8],
            'Unit_CN': row[9],
            'Unit_EN': row[10],
            'University_Lon': row[11],
            'University_Lat': row[12],
            'Universities_id': row[13],
            'City_Name_CN': row[14],
            'City_Name_EN': row[15],
            'Country': row[16],
            'City_Lat': row[17],
            'City_Lon': row[18],
            'City_Name_Other': row[19],
            'City_id': row[20],
            'City_Country_EN': row[21],
            'Country_Name_CN': row[22],
            'Country_Name_EN': row[23],
            'Country_Continent': row[24],
            'Country_id': row[25],
            'Country_Continent_EN': row[26],
            'Person_Name_CN': row[27],
            'Person_Name_EN': row[28],
            'Person_URL': row[29],
            'Person_Physical_Geography': row[30],
            'Person_Human_Geography': row[31],
            'Person_Urban_Planning': row[32],
            'Person_GIS': row[33],
            'Person_RS': row[34],
            'Person_GNSS': row[35],
            'Person_Research_Interests': row[35],
            'Person_people_id': row[36]
        })

    return Response(data)