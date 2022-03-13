from rest_framework import generics

from english.api.serializer import WordsSerializer
from english.models import Words


class WordRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WordsSerializer
    queryset = Words.objects.all()


class WordListCreateView(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = WordsSerializer
    queryset = Words.objects.filter(repeat_in_progress=False).order_by("?")[0:20]
