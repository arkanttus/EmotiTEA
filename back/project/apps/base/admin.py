from django.contrib import admin
from .models import *
from .forms import TrainedModelForm


class TrainedModelAdmin(admin.ModelAdmin):
    form = TrainedModelForm
    
    def save_model(self, request, obj, form, change):
        print('AEE')
        if obj.active:
            print('ACTIVE')
            models_actives = TrainedModel.objects.filter(active=True)

            print(models_actives)

            if models_actives.count():
                for model in models_actives:
                    print(model.__dict__)
                    model.active = False
                    print(model.__dict__)
                TrainedModel.objects.bulk_update(models_actives, ['active'])

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
