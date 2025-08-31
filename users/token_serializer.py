from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
        """
    Extends the default serializer to include user info in the token response.
    Expects 'email' and 'password' in the request.
    """
    
        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)
            token['email'] = user.email
            token['full_name'] = getattr(user, 'full_name', '')
            return token
        
        def validate(self, attrs):
            data = super().validate(attrs)
            # Include user info in the response
            
            data.update({
                "User" : {
                    "id" : self.user.id,
                    "email": self.user.email,
                    "full_name": getattr(self.user, "full_name", "")
                }
            })
            return data