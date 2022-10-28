from django.views import View


class ProductsInfo(View):
    @staticmethod
    def list_data(instance,request):
        result = {}
        host = request.get_host()
        if instance:
            result["id"] = instance.id
            result["name"] = instance.name
            result["short_describtion"]  = instance.short_describtion
            result["describtion"]  = instance.describtion
            result["price"]  = instance.price
            result["discount"]  = instance.discount
            result['created_on'] = instance.created_on
            result["final_price"] = instance.final_price
            result["product listed by "] = instance.seller.company_name
            result["image"]= host +'/media/'+ str(instance.image)
        return result
