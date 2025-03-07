from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models.query import QuerySet
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .serializer import UserRegistrationSerializer, LoginSerializer, UserDataSerializer, ResetPasswordSerializer, BookSerializer, BorrowSerializer, ReserveSerializer, FineSerializer, PaymentSerializer
from .models import Book, User, Borrow, Reserve, Fine, Payment
from paystackapi.paystack import Paystack
from datetime import datetime
from django.utils import timezone
import uuid



@api_view(['GET'])
def api_root(request):
    return Response({
        "message": "Welcome to the Library Management System API.",
        "books": "/api/books/",
        "users": "/api/users/"
    })

class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                
                response_data = {
                    "status": status.HTTP_201_CREATED,
                    "message": "User registered successfully",
                    "data": {
                        "token": token,
                        "user": {
                            "email": user.email,
                            "name": user.first_name,
                            "accountType": user.account_type,
                            "country": user.country,
                            "state": user.state,
                            "address": user.address,
                            "phoneNumber": user.phone_number
                        }
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LoginView(APIView):
    permission_classes = [AllowAny]  
    authentication_classes = []      
    
    http_method_names = ['post'] 
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'status': 400,
                    'message': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.validated_data['user']
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            user_data = UserDataSerializer(user).data

            return Response({
                'status': 200,
                'message': 'Login successful',
                'data': {
                    'token': access_token,
                    'user': user_data
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 500,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ResetpasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'status': 400,
                'message': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data.get("user")  
        
        if user is None:
            return Response({
                'status': 400,
                'message': 'User not found or invalid token/email.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = serializer.validated_data["password"]
        user.set_password(new_password)
        user.save()

        return Response({
            "status": 200,
            "message": "User password reset successfully",
            "data": {
                "email": user.email,
                "id": user.id,
                "name": user.get_full_name()
            }
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                "status": 200,
                "message": "User logged out successfully",
                "data": {
                    "user_id": request.user.id,
                    "logout_time": datetime.datetime.now()
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": 400,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
class BookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.account_type != 'admin':
            return Response (
                {
                    "status": 403,
                    "message": "Only admins can add books."
                }, status=status.HTTP_403_FORBIDDEN
            )
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()

            return Response({
                "status": 200,
                "message": "",
                "data": BookSerializer(book).data
            }, status=status.HTTP_200_OK
            )
        return Response ({
            "status": 400,
            "message": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id=None):
        try:
            if id is not None:
                book = Book.objects.filter(id=id).first()
                if book:
                    return Response(
                        {
                            "status": 200,
                            "message": "Retrieved a single book successfully.",
                            "data": BookSerializer(book).data
                        },
                        status=status.HTTP_200_OK
                    )
            

            page = int(request.query_params.get('page', 0))
            size = int(request.query_params.get('size', 10))
            
            books = Book.objects.all().order_by('id')
            
            paginator = Paginator(books, size)
            
            current_page = paginator.get_page(page + 1)
            
            serialized_books = BookSerializer(current_page, many=True).data
            
            return Response({
                "status": 200,
                "message": "",
                "data": {
                    "books": serialized_books,
                    "pagination": {
                        "totalPages": paginator.num_pages,
                        "totalItems": paginator.count,
                        "currentPage": page,
                        "pageSize": size
                    }
                }
            }, status=status.HTTP_200_OK)
            
        except ValueError:
            return Response({
                "status": 400,
                "message": "Invalid pagination parameters",
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Book.DoesNotExist:
            return Response({
                "status": 404,
                "message": "Book not found",
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            return Response({
                "status": 500,
                "message": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateView(APIView):
    def post(self, request, id):
        book = Book.objects.filter(id=id).first()
        
        if not book:
            return Response({
                "status": 404,
                "message": "Book not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
        try:
            book.delete()
            return Response({
                "status": 200,
                "message": "Book deleted successfully"
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": 400,
                "message": str(e)
            }, status=status.HTTP_BAD_REQUEST)
        
    def put(self, request, id):
        if request.user.account_type != 'admin':
            return Response (
                {
                    "status": 403,
                    "message": "Only admins can add books."
                }, status=status.HTTP_403_FORBIDDEN
            )
        book = Book.objects.filter(id=id).first()
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response ({
                "status": 200,
                "messages": serializer.data
            }, status=status.HTTP_200_OK)
        return Response ({
            "status": 400,
            "messages": serializer.error
        })


    

class DeleteView(APIView):
    def post(self, request, id):
        book = Book.objects.filter(id=id).first()
        
        if not book:
            return Response({
                "status": 404,
                "message": "Book not found"
            }, status=status.HTTP_NOT_FOUND)
            
        try:
            book.delete()
            return Response({
                "status": 200,
                "message": "Book deleted successfully"
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": 400,
                "message": str(e)
            }, status=status.HTTP_BAD_REQUEST)


    

class ReturnBookView(APIView):
    def post(self, request):
        book_id = request.data.get('bookId')
        book = Book.objects.filter(id=book_id).first()
        if not book:
            return Response ({
                "status": 403,
                "message": "book not avalaible"
            })
        
        book.availability = True
        book.save()

        serializer = BookSerializer(book)
        
        return Response ({
            "status": 201,
            "message": "Book returned successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)



class BorrowView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        book_id = request.data.get('bookId')
        if not book_id:
            return Response({
                "status": 400,
                "message": "bookId is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
        print(f"Attempting to borrow book {book_id} for user {request.user.id}")
        
        book = Book.objects.filter(id=book_id).first()
        if not book:
            return Response({
                "status": 404,
                "message": "Book not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
        if not book.availability:
            return Response({
                "status": 403,
                "message": "Book not available"
            }, status=status.HTTP_403_FORBIDDEN)
        
        
        try:
            borrow = Borrow.objects.create(
                book=book,
                borrowedBy=request.user,
                dateBorrow=timezone.now(),
                dateReturn=None  
            )
            print(f"Borrow created with ID: {borrow.id}")
            
            
            book.availability = False
            book.save()
            
            
            serializer = BorrowSerializer(borrow)
            
            return Response({
                "status": 201,
                "message": "Book borrowed successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"Error creating borrow: {str(e)}")
            return Response({
                "status": 500,
                "message": "Error creating borrow"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RenewBorrowView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        book_id = request.data.get('bookId')
        if not book_id:
            return Response({
                "status": 400,
                "message": "bookId is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        
        print(f"Attempting to renew book {book_id} for user {request.user.id}")
        
       
        try:
            borrow = Borrow.objects.filter(
                book_id=book_id,
                borrowedBy=request.user,
                dateReturn__isnull=True
            ).first()
            
            if not borrow:
                
                all_borrows = Borrow.objects.filter(
                    book_id=book_id,
                    borrowedBy=request.user
                )
                print(f"Found {all_borrows.count()} borrows for this book and user:")
                for b in all_borrows:
                    print(f"Borrow ID: {b.id}, Return Date: {b.dateReturn}")
                
                return Response({
                    "status": 404,
                    "message": "No active borrow found for this book"
                }, status=status.HTTP_404_NOT_FOUND)
            
           
            borrow.book.availability = False
            borrow.book.save()
            
           
            serializer = BorrowSerializer(borrow)
            
            return Response({
                "status": 200,
                "message": "Book renewed successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"Error renewing borrow: {str(e)}")
            return Response({
                "status": 500,
                "message": f"Error renewing borrow: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ReserveView(APIView):
    def post(self, request):
        book_id = request.data.get('bookId')
        if not book_id:
            return Response({
                "status": 400,
                "message": "bookID required"
            }, status=status.HTTP_400_BAD_REQUEST) 
        
        book = Book.objects.filter(id=book_id).first()
        if not book or not book.availability:
            return Response({
                "status": 403,
                "message": "Book not available"
            }, status=status.HTTP_403_FORBIDDEN)
        
        if not book.availability:
            return Response ({
                "status": 400,
                "message": "Book is currently borrowed"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        reserve_exist = Reserve.objects.filter(
            reservedBy = request.user,
            book = book,
            isActive = True
        ).first()
        if reserve_exist:
            return Response ({
                "status": 400,
                "message": "You have already reserved this book"
            }, status=status.HTTP_400_BAD_REQUEST)
        reserve = Reserve.objects.create(
            book = book,
            reservedBy = request.user,
            isActive = True
        )
        book.availability = False
        book.save()
        serializer = ReserveSerializer(reserve)

        return Response({
                "status": 201,
                "message": "Book reserved successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
    

class CancelReservationView(APIView):
    def delete(self, request, id=None):
        
        book = Book.objects.filter(id=id).first()
        print(book)
        if not book:
            return Response({
                "status": 403,
                "message": "Book not available"
            }, status=status.HTTP_403_FORBIDDEN)
        
        
        reservation = Reserve.objects.get(
            id = id,
            reservedBy = request.user,
            book = book,
            isActive = True
        )
        reservation.isActive = False
        reservation.save()
        
        book.availability = True
        book.save()
        serializer = BookSerializer(book)

        return Response({
                "status": 201,
                "message": "Book reserved Cancelled",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)



class HistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            page = int(request.query_params.get('page', 0))
            size = int(request.query_params.get('size', 10))
            
           
            borrows = Borrow.objects.filter(
                borrowedBy=request.user
            ).order_by('-dateBorrow')
            
           
            paginator = Paginator(borrows, size)
            page_obj = paginator.get_page(page + 1)  
            
            
            serializer = BorrowSerializer(page_obj, many=True)
            
            return Response({
                "status": 200,
                "message": "Retrieved all borrowed books history successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
            
        except ValueError:
            return Response({
                "status": 400,
                "message": "Invalid page or size parameter"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "status": 500,
                "message": "Error retrieving borrow history"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class FineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = int(request.query_params.get("page"))
        size = int(request.query_params.get("size"))

        fines = Fine.objects.filter(
            user = request.user
        )

        sort = request.query_params.get("sort", "transactionDate")
        order = request.query_params.get("order",  "desc")
        sort_by = f'-{sort}' if order == "desc" else sort

        query_set = fines.order_by(sort_by)


        paginator = Paginator(query_set, size)
        page_obj = paginator.get_page(page + 1)

        fineSerializer = FineSerializer(page_obj, many=True)

        return Response ({
            "status": 200,
            "message": "Retrieved all fines successfully",
            "date": fineSerializer.data
        }, status=status.HTTP_200_OK)




class PaymentProcessView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        amount = request.data.get('amount')
        book_id = request.data.get('bookId')
        user = request.user

        reference = f"pay_{uuid.uuid4().hex[:16]}"


        payment = Payment.objects.create(
            user = user,
            bookId = book_id,
            amount =amount,
            reference = reference,
            status="pending"
        )
       

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        amount_kobo = int(amount * 100)

        payload= {
            'email': request.user.email,
            'amount': amount_kobo,
            'reference': reference,
            'callback_url': f"{request.build_absolute_uri('/').rstrip('/')}/api/payments/verify/{reference}/",
            'metadata': {
                'book_id': book_id,
                'user_id': request.user.id
            }
        }
        try:
            response = request.post('https://api.paystack.co/transaction/initialize', headers=headers, json=payload)

            if response.status_code == 200:
                response_data = response.json()

                return Response ({
                    'status': 200,
                    'message': 'Payment initiated successfully',
                    'data': {
                        'amount': f'${amount}',
                        'bookId': book_id,
                        'user': request.user.id,
                        'transactionDate': payment.transaction_date,
                        'reference': reference,
                        'authorization_url': response_data['data']['authorization_url']
                    }
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "status": 400,
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)




    