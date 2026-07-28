from knox.auth import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.db import connection

# 允许作为 tag 过滤列名的白名单：new_Universities 与 new_people 两表同时存在的布尔标签列。
# 列名不能通过驱动参数化，白名单是唯一防线。
ALLOWED_TAGS = frozenset({
    'Physical_Geography',
    'Human_Geography',
    'Urban_Planning',
    'GIS',
    'RS',
    'GNSS',
    'Transportation',
})


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes((TokenAuthentication,))
def get_school_list(request):
    """
    e.g.
    http://127.0.0.1:8000/api/schools
    http://127.0.0.1:8000/api/schools?tag=Urban_Planning
    http://127.0.0.1:8000/api/schools?tag=Urban_Planning,Transportation
    http://127.0.0.1:8000/api/schools?continent=Asia
    """
    where_clauses = []
    params = []

    # tag：按逗号切分后仅保留白名单命中项；全部非法时用恒假条件占位，避免 SQL 语法错误。
    if 'tag' in request.GET:
        valid_tags = [
            tag for tag in (item.strip() for item in request.GET['tag'].split(','))
            if tag in ALLOWED_TAGS
        ]
        if valid_tags:
            tag_conditions = [
                '(u.' + tag + '=1 AND p.' + tag + '=1)' for tag in valid_tags
            ]
            where_clauses.append('(' + ' OR '.join(tag_conditions) + ')')
        else:
            where_clauses.append('(0)')

    # continent：走参数化占位符，驱动负责转义/绑定。
    if 'continent' in request.GET:
        where_clauses.append('co.Continent_EN = %s')
        params.append(request.GET['continent'])

    # 构造最终的 WHERE 子句
    where_sql = ''
    if where_clauses:
        where_sql = 'WHERE ' + ' AND '.join(where_clauses)

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.University_Name_CN, u.University_Name_EN, u.University_Name_Local,
            u.City, u.URL, u.University_Abbr, u.University_Other_Name,
            u.Description_CN, u.Description_EN, u.Unit_CN, u.Unit_EN, u.Lon, u.Lat,
            u.Universities_id, c.City_Name_CN, c.City_Name_EN, c.Country, c.Lat, c.Lon,
            c.City_Name_Other, c.City_id, c.Country_EN, co.Country_Name_CN, co.Country_Name_EN,
            co.Continent, co.Country_id, co.Continent_EN, p.Person_Name_CN, p.Person_Name_EN, p.URL,
            p.Physical_Geography, p.Human_Geography, p.Urban_Planning, p.GIS, p.RS, p.GNSS, p.Transportation, p.Research_Interests, p.people_id, p.Research_Interests_CN
            FROM new_Universities u
            LEFT JOIN new_city c ON u.City = c.City_Name_EN
            LEFT JOIN new_country co ON c.Country = co.Country_Name_CN
            LEFT JOIN new_people p ON u.University_Name_EN = p.University
        """ + where_sql, params)
        rows = cursor.fetchall()

    # 优化：使用列表推导式减少内存占用
    data = [{
        'U_Name_CN': row[0],
        'U_Name_EN': row[1],
        'U_Name_Local': row[2],
        'U_City': row[3],
        'U_URL': row[4],
        'U_Abbr': row[5],
        'U_Other_Name': row[6],
        'Description_CN': row[7],
        'Description_EN': row[8],
        'Unit_CN': row[9],
        'Unit_EN': row[10],
        'U_Lon': row[11],
        'U_Lat': row[12],
        'U_id': row[13],
        'C_Name_CN': row[14],
        'C_Name_EN': row[15],
        'Country': row[16],
        'C_Lat': row[17],
        'C_Lon': row[18],
        'C_Name_Other': row[19],
        'C_id': row[20],
        'C_Country_EN': row[21],
        'Co_Name_CN': row[22],
        'Co_Name_EN': row[23],
        'Co_Continent_EN': row[26],
        'P_Name_CN': row[27],
        'P_Name_EN': row[28],
        'P_URL': row[29],
        'P_Physical_Geography': row[30],
        'P_Human_Geography': row[31],
        'P_Urban_Planning': row[32],
        'P_GIS': row[33],
        'P_RS': row[34],
        'P_GNSS': row[35],
        'P_Transportation': row[36],
        'P_Research_Interests': row[37],
        'P_people_id': row[38],
        'P_Research_Interests_CN': row[39]
    } for row in rows]

    return Response(data)
