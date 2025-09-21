from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from .models import Todo
from .serializers import TodoSerializer, TodoCreateUpdateSerializer

class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Todo.objects.filter(user=self.request.user)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        # Filter by completion status
        completed = self.request.query_params.get('completed', None)
        if completed is not None:
            if completed.lower() == 'true':
                queryset = queryset.filter(completed=True)
            elif completed.lower() == 'false':
                queryset = queryset.filter(completed=False)
        
        # Filter by priority
        priority = self.request.query_params.get('priority', None)
        if priority:
            queryset = queryset.filter(priority=priority)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk, user=request.user)
        todo.completed = not todo.completed
        todo.save()
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
    except Todo.DoesNotExist:
        return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def todo_stats(request):
    todos = Todo.objects.filter(user=request.user)
    total = todos.count()
    completed = todos.filter(completed=True).count()
    pending = total - completed
    
    return Response({
        'total': total,
        'completed': completed,
        'pending': pending,
        'completion_rate': round((completed / total * 100) if total > 0 else 0, 1)
    })
