from rest_framework import serializers
from .models import registration,Category,Product,Order,CartItem, User,Contact
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class ObtainTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = registration
        fields = ('User_Name','Email','Password')
    
    def create(self, validated_data):
        username = validated_data.get('User_Name')
        email = validated_data.get('Email')
        password = validated_data.get('Password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username, email, password)

        validated_data['user'] = user
        user_reg = registration.objects.create(**validated_data)
        return user_reg


class Categoryserializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductCreateSerializer(serializers.ModelSerializer):
    lookup_field = 'pk'
    class Meta:
        model = Product
        fields = '__all__'

class ProductUpdateSerializer(serializers.ModelSerializer):
    lookup_field = 'pk'

    class Meta:
        model = Product
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name','category_name']

    def get_category_name(self, obj):
        return obj.category.name
    
class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','name','description','price','category_name']

    def get_category_name(self, obj):
        return obj.category.name
    

class CartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['user', 'product']

    
class CartItemListSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id','user_name','product_name','product','user']

    def get_product_name(self, obj):
        return obj.product.name

    def get_user_name(self, obj):
        return obj.user.username

class ProductDiscountSerializer(serializers.ModelSerializer):#discount and offer
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'discount', 'offer_start_date', 'offer_end_date','discount_percentage']

    def get_discount_percentage(self, obj):
        if obj.discount:
            Discount = obj.price - obj.discount
            percentage = round((Discount / obj.price) * 100)
            return f'{percentage}%'
        return None
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'total_price']



class EmailSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'phone', 'address')
