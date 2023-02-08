from rest_framework import serializers
from stack.models import Questions,Answers

# class QuestionSerializer(serializers.ModelSerializer):
#     id=serializers.CharField(read_only=True)
#     created_date=serializers.CharField(read_only=True)
#     is_active=serializers.BooleanField(read_only=True)
#     user=serializers.CharField(read_only=True)

#     class Meta:
#         model=Questions
#         fields="__all__"



class AnswerSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    question=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)
    # up_vote=serializers.CharField(read_only=True)
    up_vote_count=serializers.CharField(read_only=True)

    class Meta:
        model=Answers
        # fields="__all__"
        exclude=("up_vote",)

    def create(self, validated_data):
        question=self.context.get("question")
        user=self.context.get("user")
        return Answers.objects.create(user=user,question=question,**validated_data)

class QuestionSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    created_date=serializers.CharField(read_only=True)
    is_active=serializers.BooleanField(read_only=True)
    user=serializers.CharField(read_only=True)
    fetch_answers=AnswerSerializer(read_only=True,many=True)

    class Meta:
        model=Questions
        fields="__all__"
