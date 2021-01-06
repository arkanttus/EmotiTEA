from django.contrib import admin
from .models import *
from .forms import TrainedModelForm


class TrainedModelAdmin(admin.ModelAdmin):
    form = TrainedModelForm
    
    def save_model(self, request, obj, form, change):
        obj.save()

        files = request.FILES.getlist('weights')

        files_instance = [ WeightTrainedModel(weight=file, trained_model=obj) for file in files]
        WeightTrainedModel.objects.bulk_create(files_instance)

admin.site.register(Institution)
admin.site.register(Student)
admin.site.register(Affiliation)
admin.site.register(PalliativeMeasure)
admin.site.register(AdditionalInformation)
admin.site.register(Photos)
admin.site.register(TrainedModel, TrainedModelAdmin)
