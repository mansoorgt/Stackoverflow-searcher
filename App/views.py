from datetime import datetime, time, timedelta, timezone
from itertools import count
import json
from time import strftime

from turtle import title
from types import SimpleNamespace
from xml.etree.ElementTree import tostring
from django.http import HttpResponse
from django.shortcuts import redirect, render
from stackapi import StackAPI
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from yaml import MappingStartEvent

from App.models import searchResultDb, searchperdayDb, timeDb
# Create your views here.

def renderIndex(reqeust):

    total_searches=searchResultDb.objects.all().count()
    search_perday=searchperdayDb.objects.all().count()
    


    if timeDb.objects.all().count()>0:
        end_time=timeDb.objects.last().endtime
        currentime=datetime.now()

        first_search_time=timeDb.objects.first().startedtime

        day_time_limit=first_search_time+timedelta(hours=24)
        print(first_search_time,'----------------daytime----------',day_time_limit)

        if search_perday>99:
            if currentime.time()<day_time_limit.time():
                
                searchperdayDb.objects.all().delete()
                
                return render(reqeust,'searchpage.html',{'total_searches':search_perday,'status':'finiedja'})
            else:
                print(currentime)
                te=day_time_limit
                
                return render(reqeust,'searchpage.html',{'total_searches':search_perday,'status':te})

               
            

        print(currentime.time(),'------------',end_time.time())
        if total_searches>4 and currentime.time()<end_time.time():
        
            print('-----------limitfinshed---------------')    
            status='You need to wait 1 minute' 
            
            return render(reqeust,'searchpage.html',{'total_searches':search_perday,'status_red':status})
        else:
            searchResultDb.objects.all().delete()
            
            return render(reqeust,'searchpage.html',{'total_searches':search_perday,'status':'You can Search Now'})
    else:
        return render(reqeust,'searchpage.html',{'total_searches':search_perday,'status':'You can Search Now'})
       
    
    
def getQuestions(request):
   
    search_count=searchResultDb.objects.all().count()
    search_perday=searchperdayDb.objects.all().count()
    if search_count>4 or search_perday>99:
        
        return redirect(renderIndex)
    if search_count==0:
        started_time=datetime.now()
        timelimit=1
        print(started_time)
        end_time=started_time+timedelta(minutes=timelimit)
        m_time=timeDb(startedtime=started_time,endtime=end_time)

        m_time.save()
        print('timer_started==',started_time)

    m_search=request.GET.get('search')
    if m_search == None:
        
        m_search=searchResultDb.objects.order_by('id')[0].search
        print('changed',m_search)
    else:
        m_perdaydata=searchperdayDb(search=m_search)
        m_data=searchResultDb(search=m_search)
        m_perdaydata.save()
        m_data.save()
    print('-----------------------------------',m_search)
    site= StackAPI('stackoverflow')
        
    questions = site.fetch('search/advanced', title=m_search)
    paginator_objs=Paginator(questions['items'],10)
    page=request.GET.get('page')
    print(len(questions['items']))
    try:
        post=paginator_objs.page(page)
    except PageNotAnInteger:
        post=paginator_objs.page(1)
    except EmptyPage:
        post=paginator_objs.page(paginator_objs.num_pages)    
        
  
    return render(request,'searchpage.html',{'obj':post,'search':m_search})
    