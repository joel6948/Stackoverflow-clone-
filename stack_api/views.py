from django.shortcuts import render

# Create your views here.
from stack.models import Questions,Answers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import authentication,permissions
from stack_api.serializers import AnswerSerializer,QuestionSerializer
from rest_framework.decorators import action
from stack_api.custompermissions import OwnerOrReadOnly
from rest_framework.generics import mixins
from rest_framework import generics
from rest_framework import serializers


class QuestionsView(viewsets.ModelViewSet):
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    http_method_names=["get","post","put"]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Questions.objects.all().exclude(user=self.request.user)

    @action(methods=["post"],detail=True)
    def add_answer(self,request,*args,**kwargs):
        question=self.get_object()
        user=request.user
        serializer=AnswerSerializer(data=request.data,context={"user":user,"question":question})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

class AnswerView(viewsets.ViewSet):
    permission_classes=[permissions.IsAuthenticated,OwnerOrReadOnly]
    # authentication_classes=[authentication.TokenAuthentication]
    
    @action(methods=["POST"],detail=True)
    def add_up_vote(self,request,*arhs,**kwargs):
        id=kwargs.get("pk")
        answer=Answers.objects.get(id=id)
        user=request.user
        answer.up_vote.add(user)
        return Response(data="you upvoted")
    

    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Answers.objects.get(id=id)
        if object.user==request.user:
            Answers.objects.filter(id=id).delete()
            return Response(data="deleted")
        else:
            raise serializers.ValidationError("you don't have permission")


class QuestionDeleteView(mixins.DestroyModelMixin,generics.GenericAPIView):

    queryset=Questions.objects.all()
    serializer_class=QuestionSerializer
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[OwnerOrReadOnly]
    
    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

    




