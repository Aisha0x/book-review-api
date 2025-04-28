from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .models import Book, Review
from .serializers import RegisterSerializer, BookSerializer, ReviewSerializer
from django.contrib.auth.models import User

# تسجيل مستخدم جديد
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# تغيير كلمة المرور
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    user = request.user
    new_password = request.data.get('new_password')
    if new_password:
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password updated successfully'})
    else:
        return Response({'error': 'New password is required.'}, status=status.HTTP_400_BAD_REQUEST)

# قائمة الكتب وإنشاء كتاب (Admins فقط يضيفون)
class BookGenericAPIView(generics.GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

# تفاصيل كتاب (عرض - تعديل - حذف) (Admins فقط للتعديل والحذف)
class BookDetailGenericAPIView(generics.GenericAPIView,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)

# مراجعات كتاب معين (عرض - إضافة)
class ReviewGenericAPIView(generics.GenericAPIView,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Review.objects.filter(book_id=book_id)

    def get(self, request, book_id):
        return self.list(request)

    def post(self, request, book_id):
        return self.create(request)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, book_id=self.kwargs['book_id'])

# تفاصيل مراجعة (تعديل - حذف - فقط المالك)
class ReviewDetailGenericAPIView(generics.GenericAPIView,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        review = self.get_object()
        if review.user != request.user:
            return Response({'error': 'You can only edit your own reviews.'}, status=status.HTTP_403_FORBIDDEN)
        return self.update(request, pk)

    def delete(self, request, pk):
        review = self.get_object()
        if review.user != request.user:
            return Response({'error': 'You can only delete your own reviews.'}, status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, pk)
