from django.db import models

# Create your models here.

class VocabularyDict(models.Model):
    VocabularyEN = models.CharField(max_length = 50)    
    VocabularyCH = models.CharField(max_length = 255)
    Category = models.CharField(max_length = 50)

class VocabularyRelatedInfo(models.Model):
    VocabularyEN = models.CharField(max_length = 50)
    ExampleSentences = models.TextField()
    ExampleSentencesCH = models.TextField()
    Synonym = models.CharField(max_length=50)
    SynonymCH = models.CharField(max_length = 255) 

class UserRigisterInfo(models.Model):
    NickName = models.CharField(max_length = 50,primary_key=True)
    Phone = models.CharField(max_length = 11)
    Email = models.EmailField(max_length = 50)
    Password = models.CharField(max_length = 20) 
    
  
class VocabularyNotes(models.Model):
    NickName = models.ForeignKey(UserRigisterInfo)
    VocabularyEN = models.CharField(max_length = 50)
    NoteContent = models.TextField()
    IsShared = models.CharField(max_length = 1)
    CreateTime = models.DateTimeField()

class ReciteWordsRecords(models.Model):
    NickName = models.ForeignKey(UserRigisterInfo)
    RecordingDate = models.DateTimeField()
    IndexOfCET4 = models.IntegerField()
    IndexOfCET6 = models.IntegerField()
    IndexOfGRE = models.IntegerField()
    IndexOfTOEFL = models.IntegerField()
    

class ReciteWordsInitSettings(models.Model):
    NickName = models.ForeignKey(UserRigisterInfo)
    SettingDate = models.DateTimeField()
    CountOfEveryDay = models.IntegerField()
    VocabularyCategory = models.CharField(max_length = 50)
