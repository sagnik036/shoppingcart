from django.views import View


class CartInfo(View):
    @staticmethod
    def list_data(instance):
        result = {}
        products = instance.products.all()
        if instance:
            result["id"] = instance.id
            result["username"] = instance.user.username
            result["products"] = [str(i) for i in products]
            result['created_at'] = instance.created_at
            result['edited_at'] = instance.edited_at
        return result
