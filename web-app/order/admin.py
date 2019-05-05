from django.contrib import admin
from .models import orders,wareHouse,truck,upsack,upsseq,worldack,worldseq,topack,placed
# Register your models here.
admin.site.register(orders)
admin.site.register(wareHouse)
admin.site.register(truck)
admin.site.register(upsack)
admin.site.register(upsseq)
admin.site.register(worldack)
admin.site.register(worldseq)
admin.site.register(topack)
admin.site.register(placed)