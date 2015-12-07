from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from .models import Snippet
from .serializers import SnippetSerializer


class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    List all snippets , or create a new snippet
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        """
        handles GET requests
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        handles POST requests
        """
        return self.create(request, *args, **kwargs)


class SnippetDetail(APIView):
    """
    Retrieve , update or delete a code snippet
    :param request:
    :param pk:
    :return:
    """

    def get_object(self, pk):

        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
