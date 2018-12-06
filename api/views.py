from django.shortcuts import render
import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from api.models import Contact, ContactSerializer
from api.models import Books, Profile, Inventory, Trades
from api.models import BooksSerializer, ProfileSerializer, InventorySerializer, TradesSerializer, TradeProfileSerializer
# from api.models import WishlistSerializer, InterestedBooks
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login

# class ContactsView(APIView):
#     def get(self, request, contact_id=None):

#         if contact_id is not None:
#             contact = Contact.objects.get(id=contact_id)
#             serializer = ContactSerializer(contact, many=False)
#             return Response(serializer.data)
#         else:
#             contacts = Contact.objects.all()
#             serializer = ContactSerializer(contacts, many=True)
#             return Response(serializer.data)
        
#     def post(self, request):
            
#         serializer = ContactSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        
#     def delete(self, request, contact_id):
        
#         contact = Contact.objects.get(id=contact_id)
#         contact.delete()
        
#         return Response(status=status.HTTP_204_NO_CONTENT)

class BooksView(APIView):
    def get(self, request, book_id=None):
        if book_id is not None:
            book = Books.objects.get(id=book_id)
            serializer = BooksSerializer(book, many=False)
            return Response(serializer.data)
        else:
            book = Books.objects.all()
            serializer = BooksSerializer(book, many=True)
            return Response(serializer.data)
            
class LoginView(APIView):
    def get(self, request):
        user = request.GET['user']
        
        if user is not None:
            try:
                profile = Profile.objects.get(user=user)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProfileSerializer(profile, many=False)
            return Response(serializer.data)
        
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    def get(self, request, profile_id=None):
        if profile_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                profile = Profile.objects.get(id=profile_id)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = ProfileSerializer(profile, many=False)
            return Response(serializer.data)
        
            

    def put(self, request, profile_id=None):
        if profile_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                profile = Profile.objects.get(id=profile_id)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            profile.address = request.data.get("address")
            profile.birthday = request.data.get("birthday")
            profile.favorite_genre = request.data.get("favorite_genre")
            profile.address = request.data.get("address")
            profile.save()
            return Response(status=status.HTTP_200_OK)

    def patch(self, request, profile_id=None):
        if profile_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                profile = Profile.objects.get(id=profile_id)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, profile_id=None):
        if profile_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                profile = Profile.objects.get(id=profile_id)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            profile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        
class LibraryView(APIView):
    def get(self, request, profile_id=None):
        if profile_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                library = Inventory.objects.filter(profile=profile_id)
            except Inventory.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            serializer = InventorySerializer(library, many=True)
            return Response(serializer.data)
            
    def delete(self, request, profile_id=None):
        if profile_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                inventory = Inventory.objects.get(id=profile_id)
            except Inventory.DoesNotExist:
                return Response(Status=status.HTTP_404_NOT_FOUND)
            
            inventory.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
    def post(self, request):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PageView(APIView):   
    def get(self, request, book_id=None):
        if book_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                owners = Profile.objects.filter(library__exact=book_id)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
        if owners is not None:
            serializer = TradeProfileSerializer(owners, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
class WishersView(APIView):
    def get(self, request, book_id=None):
        if book_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                wishers = Profile.objects.filter(wishlist__exact=book_id)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
        if wishers is not None:
            serializer = ProfileSerializer(owners, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
   
            
    
# class WishlistView(APIVIew):
#     serializer_class = ProfileSerializer
    
    
    #partial=true
        
# class WishlistView(APIView):
#     serializer_class = WishlistSerializer
    
#     def get(self, request, profile_id):
#         wishlist = InterestedBooks.objects.filter(profile=profile_id)
#         serializer = WishlistSerializer(wishlist, many=True)
#         return Response(serializer.data)
        
        
class TradesView(APIView):
    serializer_class = TradesSerializer
    
    def get(self, request, given_id):
        user_books = Trades.objects.filter(trader__profile=given_id)
        trades = TradesSerializer(user_books, many=True)
        return Response(trades.data)
        
    def put(self, request, given_id):
        trade = Trades.objects.get(id=given_id)
        serializer = TradesSerializer(trade, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        serializer = TradesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class RequestsView(APIView):
    def get(self, request, given_id):
        user_books = Trades.objects.filter(receiver__profile=given_id)
        trades = TradesSerializer(user_books, many=True)
        return Response(trades.data)
        
    def put(self, request, profile_id):
        trade = Trades.objects.get(id=profile_id)
        trade.is_accepted = request.data.get("is_accepted")
        trade.save()
        
        serializer = TradesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
            
    
    def delete(self, request, profile_id):
        trade = Trades.objects.get(id=profile_id)
        trade.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
        