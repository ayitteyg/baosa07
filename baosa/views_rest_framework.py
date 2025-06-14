from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # Try to get related Member
        try:
            member = user.member_profile  # via related_name='member_profile'
            member_id = member.id
            member_name = member.name
        except:
            member_id = None  # If no member profile exists

        return Response({
            'token': token.key,
            'mid': member_id,  # Return Member.id here instead of User.id
             'usid': user.id,
            'username': user.username,
            'member_name':member_name,
            'isExecutive': user.is_executive,
        })
