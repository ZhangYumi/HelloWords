from django.conf.urls import url,include
from . import views

urlpatterns=[
        url(r'^$',views.index,name='index'),
        url(r'^index/$',views.index,name='index'),
        url(r'^(?P<Category>\CET4|CET6|GRE|TOEFL)/$', views.getVocabularyByCategory, name = 'getVocabularyByCategory'),
        url(r'^login/$',views.login,name = 'login'),
        url(r'^rigister/$',views.rigister,name = 'rigister'),
        url(r'^vocabularysettings/$',views.vocabularysettings,name = 'vocabularysettings'),
        url(r'^detailVocabulary/$',views.detailVocabulary,name = 'detailVocabulary'),
        url(r'^addNote/$',views.addNote,name='addNote'),
        url(r'^getVocabularyByCategoryAndRecords/$',views.getVocabularyByCategoryAndRecords,name='getVocabularyByCategoryAndRecords'),
        url(r'^getMyNote/$',views.getMyNote,name='getMyNote'),
        url(r'^getSharedNote/$',views.getSharedNote,name='getSharedNote'),
        url(r'^updateReciteRecords/$',views.updateReciteRecords,name='updateReciteRecords'),
        ]
        
