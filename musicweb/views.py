from django.shortcuts import render,redirect,render_to_response
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from pymongo import MongoClient
# Create your views here.
import re



# user_list=[
#     {'user':'yingmo','password':"123"},
#     {'user':'xuchang','password':'456'}
# ]

user_list=[
    {'user':'yingmo','password':"123"},
    {'user':'xuchang','password':'456'}
]

def details(request):
    q=request.GET.get('name')
    client = MongoClient('localhost', 27017)
    db = client['inf551']
    coll = db['music']

    r = {}
    # r.setdefault('title','%s'%username)
    # regx = re.compile("%s" % q, re.IGNORECASE)
    r.setdefault('title', q)
    dat=list(coll.find(r))
    print(dat)
    return render(request,'details.html',{'dat':dat[0]})
def funs(request):
    # if request.method=='POST':
    #     username=request.POST.get('username')
    # else:
    #     username = request.GET.get('input')
    #
    #

    if request.method=='POST':
        q=request.POST.get('search')

        if not q:
            q="(all)"

        return HttpResponseRedirect('result?search=%s&artist=None&album=None&genre=None&date=None' % q)

    # if q:
    #     return HttpResponseRedirect('result?search=%s'%q)
    #
    # # password=request.POST.get('password',None)
    # # temp={'user':username,'password':password}
    #
    # # user_list.append(temp)

    client = MongoClient('localhost', 27017)
    db = client['inf551']



    check = request.GET.get('album')
    if check!='None':
        al_checklist=(check.split('-')[1:])
    else:
        al_checklist = []

    coll=db['album']
    album=list(coll.find({}))
    album_name=[]
    for x in album:
        if x['album'] in al_checklist:
            is_check='True'
        else:
            is_check='False'
        album_name.append({"album":x['album'],"num":len(x["index"]),"check":is_check})
    album_name = sorted(album_name, key=lambda x: x['album'])


    check=request.GET.get('artist')
    if check!='None':
        ar_checklist=(check.split('-')[1:])
        ar_checklist=list(map(lambda x:x.replace('*','&'),ar_checklist))

    else:
        ar_checklist = []

    coll=db['artist']
    artist=list(coll.find({}))
    artist_name=[]
    for x in artist:
        if x['artist'] in ar_checklist:
            is_check='True'
        else:
            is_check='False'
        artist_name.append({"artist":x['artist'],"num":len(x["index"]),"check":is_check})
    artist_name = sorted(artist_name, key=lambda x: x['artist'])

    check = request.GET.get('date')
    if check != 'None':
        date_checklist = (check.split('-')[1:])
    else:
        date_checklist = []

    coll = db['date']
    date = list(coll.find({}))
    date_name = []
    for x in date:
        if x['date'] in date_checklist:
            is_check='True'
        else:
            is_check='False'
        date_name.append({"date": x['date'], "num": len(x["index"]),"check":is_check})
    date_name= sorted(date_name, key=lambda x:x['date'])

    check = request.GET.get('genre')
    if check != 'None':
        genre_checklist = (check.split('-')[1:])
        genre_checklist = list(map(lambda x: x.replace('*', '&'), genre_checklist))
    else:
        genre_checklist = []
    coll = db['genre']
    genre = list(coll.find({}))
    genre_name = []
    for x in genre:
        if x['genre'] in genre_checklist:
            is_check='True'
        else:
            is_check='False'
        genre_name.append({"genre": x['genre'], "num": len(x["index"]),"check":is_check})
    genre_name = sorted(genre_name, key=lambda x: x['genre'])

    username = request.GET.get('search')

    # coll = db['music']
    # if username != '(all)':
    #     r = {}
    #     # r.setdefault('title','%s'%username)
    #     regx = re.compile("%s" % username, re.IGNORECASE)
    #     r.setdefault('title', regx)
    #
    #     # print(r)
    #     res = list(coll.find(r))
    # else:
    #     res = list(coll.find({}))
    res=get_result(username,al_checklist,ar_checklist,genre_checklist,date_checklist)

    return render(request,"result.html",{'dat':res,'album':album_name,'artist':artist_name,'date':date_name,'genre':genre_name})

def get_result(keyword,album_l=None,artist_l=None,genre_l=None,date_l=None):
    or_list=[]
    client = MongoClient('localhost', 27017)
    db = client['inf551']
    coll = db['music']
    if keyword!='(all)':
        regx = re.compile("%s" % keyword, re.IGNORECASE)
        or_list.append({'title':regx})
    if len(album_l)>0:
        ls=[]
        for x in album_l:
            ls.append({'album':x})
        or_list.append({'$or':ls})
    if len(artist_l)>0:
        ls = []
        for x in artist_l:
            ls.append({'artist':x})
        or_list.append({'$or': ls})
    if len(genre_l)>0:
        ls = []
        for x in genre_l:
            ls.append({'genre':x})
        or_list.append({'$or': ls})
    if len(date_l)>0:
        ls=[]
        for x in date_l:
            ls.append({'date':x})
        or_list.append({'$or': ls})
    if len(or_list)==0:
        res=list(coll.find({}))
    else:
        res=list(coll.find({"$and":or_list}))
    return res
def xuchang(request):
    # res={''}
    # if request.method=='POST':
    #     return render_to_response('index12.html')

    q = request.GET.get('search')
    # if q:
    #     search={'content':q}
    #     request.session['msg']=search
    if q:
        return HttpResponseRedirect('result?search=%s&artist=None&album=None&genre=None&date=None'%q)
    # else:
    #     return HttpResponseRedirect('result?search=%s&artist=None&album=None&genre=None&date=None' % "(all)")

    return render(request, "index.html")

