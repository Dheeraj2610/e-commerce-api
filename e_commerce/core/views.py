
from rest_framework import generics,filters,status
from rest_framework.response import Response
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Category,Product,CartItem, registration, User,Contact
from .serializers import ProductCreateSerializer,Categoryserializer,ProductSerializer, ProductDetailSerializer,CartItemSerializer,ProductDiscountSerializer, userSerializer, CartItemListSerializer, OrderSerializer, EmailSerializer,ContactSerializer,ObtainTokenPairSerializer
from datetime import date
from rest_framework.filters import BaseFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView

import smtplib
from email.mime.text import MIMEText

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse


class ObtainTokenPairView(TokenObtainPairView):
    serializer_class = ObtainTokenPairSerializer


# Create your views here.


class userCreate(generics.CreateAPIView):  # create user
    queryset = registration.objects.all()
    serializer_class = userSerializer

class CreateCategoryView(generics.CreateAPIView):
    permission_classes = [IsAdminUser,IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = Categoryserializer

class CategoryList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = Categoryserializer

class CreateProductView(generics.CreateAPIView):
    # permission_classes = [IsAdminUser,IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer

class ProductDetailAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class =  ProductDetailSerializer


class ProductOfferList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]  #offer and discount
    serializer_class = ProductDiscountSerializer

    def get_queryset(self):
        today = date.today()
        return Product.objects.filter(offer_start_date__lte=today, offer_end_date__gte=today)
    


class AddToCartView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    
   


class CartItemList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemListSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return CartItem.objects.filter(user=user_id)

class productFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category = request.query_params.get('category', None)
    
        if category:
            queryset = queryset.filter(category=category)       
        
        return queryset
    
class productFilterView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    filter_backends = [productFilterBackend]
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset() 
        min_price = self.request.query_params.get('min')
        max_price = self.request.query_params.get('max')
        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
        return queryset.order_by('price')

class EmailView(generics.CreateAPIView):

    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

            # Get user and cart item
        user_id = serializer.validated_data['user_id']
        product_id = serializer.validated_data['product_id']
        user = get_object_or_404(User, id=user_id)
        cart_item = get_object_or_404(CartItem, user=user, product_id=product_id)

            # Get user's email address
        email_to = user.email

        product = cart_item.product

            # Other email details (sender, subject, body)
        email_from = "e-commerce@example.com"
        subject = "Your order has been placed"
        body = f"Thank you for placing an order for product {product.name}."

            # Compose email message
        message = MIMEText(body)
        message['from'] = email_from
        message['to'] = email_to
        message['subject'] = subject

            # Connect to SMTP server and send email
        smtp_server = "smtp.mailtrap.io"
        smtp_port = 465
        smtp_user = "5c447154dc3077"
        smtp_pass = "a26bfa753ab075"
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(email_from, email_to, message.as_string())
        server.quit()
        return Response({'message': 'Email sent successfully'})

class ContactCreate(generics.CreateAPIView):
    permission_classes = [IsAdminUser,IsAuthenticated]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class AdminContactList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()

class ProductDelete(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser,IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
   
class  UpdateProductView(generics.RetrieveUpdateAPIView):
    
    lookup_field = 'pk'  # details of particular employee
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class LogoutAPIView(APIView):
    def post(self, request):
        response = JsonResponse({'message': 'Logout successful'})
        response.delete_cookie('jwt')
        return response