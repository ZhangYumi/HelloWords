from django.shortcuts import render,render_to_response,redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template,Context
from HelloWordsApp.models import VocabularyDict,UserRigisterInfo,VocabularyRelatedInfo,VocabularyNotes,ReciteWordsRecords,ReciteWordsInitSettings
from django.core import serializers
from django.http import JsonResponse
import json
import time

# Create your views here.
def index(request):
    #Vocabulary = serializers.serialize('json',VocabularyDict.objects.filter(Category='CET4'))
    #return render(request,'index.html',{'Vocabulary':Vocabulary})
    return getVocabularyByCategory(request,'CET4')

def getVocabularyByCategory(request,Category):
    Vocabulary = serializers.serialize('json',VocabularyDict.objects.filter(Category=Category))
    return render(request,'index.html',{'Vocabulary':Vocabulary,})

def getRecordsByCategoryAndNickName(Category,NickName):
    try:
        if Category=='CET4':
            record = ReciteWordsRecords.objects.filter(NickName_id = NickName)[0].IndexOfCET4
        elif Category=='CET6':
            record = ReciteWordsRecords.objects.filter(NickName_id = NickName)[0].IndexOfCET6
        elif Category=='GRE':
            record = ReciteWordsRecords.objects.filter(NickName_id = NickName)[0].IndexOfGRE
        elif Category=='TOEFL':
            record = ReciteWordsRecords.objects.filter(NickName_id = NickName)[0].IndexOfTOEFL
        else:
            record = 0
    except:
        record = 0
    finally:
        return record


def getVocabularyByCategoryAndRecords(request):
    get = request.GET
    Category = get.get('Category')
    NickName = get.get('NickName')

    record = getRecordsByCategoryAndNickName(Category,NickName)
    if not record:
        record = 0
    try:
        count = ReciteWordsInitSettings.objects.filter(NickName_id = NickName,VocabularyCategory = Category)[0].CountOfEveryDay
    except:
        count = 0

    if not count:
        count = 50
    Vocabulary = VocabularyDict.objects.filter(Category=Category,id__gt=record)[0:count:1]  
      
    Vocabulary = serializers.serialize('json',Vocabulary).strip('[]')

    return HttpResponse(json.dumps({'Vocabulary':Vocabulary}))

def updateReciteRecords(request):
    get = request.GET
    Category = get.get('category')
    VocabularyEN = get.get('currentVocabulary')
    NickName = get.get('nickname')
    CreateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    vocabularyId = VocabularyDict.objects.filter(Category=Category,VocabularyEN=VocabularyEN)[0].id
 
    if Category=='CET4':
        defaults = {
         'IndexOfCET4' : vocabularyId,
         'RecordingDate': CreateTime,
    }
    elif Category=='CET6':
        defaults = {
         'IndexOfCET6' : vocabularyId,
         'RecordingDate': CreateTime,  
    }      
    elif Category=='GRE':
        defaults = {
         'IndexOfGRE' : vocabularyId,
         'RecordingDate': CreateTime,  
    }        
    elif Category=='TOEFL':
        defaults = {
         'IndexOfTOEFL' : vocabularyId,
         'RecordingDate': CreateTime,  
    }
    else:
        return HttpResponse(json.dumps({'status':'error'}))
    
    obj,created = ReciteWordsRecords.objects.update_or_create(
        NickName_id = NickName,defaults=defaults
    )
    if created:
        return HttpResponse(json.dumps({'status':'create'}))
    if obj:
        return HttpResponse(json.dumps({'status':'update'}))

    
    
def detailVocabulary(request):
    get = request.GET
    currentVocabulary = get.get("currentVocabulary")
    VocabularyDetail = serializers.serialize('json',VocabularyRelatedInfo.objects.filter(VocabularyEN=currentVocabulary)).strip('[]')
        
    return HttpResponse(json.dumps({'message':VocabularyDetail}))

def addNote(request):
    get = request.GET
    VocabularyEN = get.get('addNoteVocabulary')   
    NoteContent = get.get('addNoteContent')
    IsShared = get.get('isSharedNote')
    NickName = get.get('NickName')

    CreateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    defaults = {
        'VocabularyEN' :VocabularyEN,   
        'NoteContent' : NoteContent,
        'IsShared' : IsShared,
        'NickName_id' : NickName,
        'CreateTime' : CreateTime,
    }
    
    obj,created = VocabularyNotes.objects.update_or_create(
        NickName_id = NickName,VocabularyEN=VocabularyEN,defaults=defaults
    )
    if created:
        return HttpResponse(json.dumps({'status':'create'}))
    if obj:
        return HttpResponse(json.dumps({'status':'update'}))
        
def getMyNote(request):
    get = request.GET
    NickName = get.get('NickName')
    note = VocabularyNotes.objects.filter(NickName_id = NickName)
    if note.exists():
        notestr = serializers.serialize('json',note).strip('[]')
        return HttpResponse(json.dumps({'MyNote':notestr}))     

def getSharedNote(request):
    get = request.GET
    VocabularyEN = get.get('VocabularyEN')

    note = VocabularyNotes.objects.filter(VocabularyEN = VocabularyEN,IsShared = '1')
 
    if note.exists():
        notestr = serializers.serialize('json',note).strip('[]')
        return HttpResponse(json.dumps({'SharedNote':notestr}))     


def login(request):
    print (request.method)
    if request.method == 'POST':
        post = request.POST
        email = post.get("Email")
        password = post.get("Password")
        user = UserRigisterInfo.objects.filter(Email = email)
        if user.count()>0:
            r_Password = list(user)[0].Password 
            r_NickName = list(user)[0].NickName 

            if r_Password==password:  
                return HttpResponse(json.dumps({'NickName':r_NickName}))            
            else:
                return HttpResponse(json.dumps({'NickName':''}))
        else:
            return HttpResponse(json.dumps({'NickName':''}))
    else:
        return render(request,'login.html')

def rigister(request):
    print (request.method)
    if request.method == 'POST':
        post = request.POST
        nickname = post.get("rigisterNickName")
        phone = post.get("rigisterPhone")
        email = post.get("rigisterEmail")
        password = post.get("rigisterPassword")

        r_Email = UserRigisterInfo.objects.filter(Email = email)
        r_NickName = UserRigisterInfo.objects.filter(NickName = nickname)
        r_Phone = UserRigisterInfo.objects.filter(Phone = phone)
        
        if r_Email.exists():
            return HttpResponse(json.dumps({'message':'emailexists'}))
        if r_NickName.exists():
            return HttpResponse(json.dumps({'message':'nicknameexists'}))
        if r_Phone.exists():
            return HttpResponse(json.dumps({'message':'phoneexists'}))

        user = UserRigisterInfo.objects.create(NickName=nickname,Phone=phone,Email=email,Password=password)
        if user:  
            return HttpResponse(json.dumps({'message':'successed'}))            
        else:
            return HttpResponse(json.dumps({'message':'error'}))
    else:
        return render(request,'rigister.html')


def vocabularysettings(request):
    print (request.method)
    if request.method == 'POST':
        post = request.POST
        VocabularyCategory = post.get("Category")
        CountOfEveryDay = post.get("CountOfEveryDay")
        NickName = post.get("NickName")
        SettingDate = time.strftime("%Y-%m-%d", time.localtime())
        defaults = {
                    "VocabularyCategory":VocabularyCategory,
                    "CountOfEveryDay":CountOfEveryDay,
                    "NickName_id":NickName,
                    "SettingDate":SettingDate,
                   }

        obj,created = ReciteWordsInitSettings.objects.update_or_create(
        NickName_id = NickName,VocabularyCategory=VocabularyCategory,defaults=defaults
    )
        if created:
            return HttpResponse(json.dumps({'status':'create'}))
        if obj:
            return HttpResponse(json.dumps({'status':'update'}))

    else:
        return render(request,'vocabularysettings.html')
        
    
