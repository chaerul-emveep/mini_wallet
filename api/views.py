
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

import datetime

from rest_framework import status
from .models import Wallet, Deposit, Withdraw
from .serializers import WalletSerializer, DepositSerializer, WithdrawSerializer

class ListUsers(APIView):
    """
    View to list all users in the system.  

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

class CustomAuthToken(ObtainAuthToken):
 
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class WalletApiView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        wallet = Wallet.objects.filter(owned_by=int(request.user.id)).first()

        if wallet is not None and wallet.status == "enabled":
            serializer = WalletSerializer(wallet)

            res = {
                "status": "success",
                    "data": {
                        "wallet": {
                            "id": wallet.id,
                            "owned_by": wallet.owned_by.id,
                            "status": wallet.status,
                            "enabled_at": wallet.enabled_at,
                            "balance": wallet.balance
                        }
                    }
                }

            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response("Please Enable wallet first", status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, format=None):

        wallet = Wallet.objects.filter(owned_by=request.user.id).first()
        
        if request.data.get("is_disabled") is not None and request.data.get("is_disabled") is True:
            
            data = {
                "status": "disabled",
                "disabled_at": datetime.datetime.now()
            }

        else:
           
            if wallet is not None and wallet.status == "enabled":
                return Response("Wallet Already enabled", status=status.HTTP_400_BAD_REQUEST)

            data = {
                "owned_by": request.user.id,
                "status": "enabled",
                "enabled_at": datetime.datetime.now()
            }

        
        if wallet is not None:
            serializer = WalletSerializer(instance=wallet, data=data, partial=True)
        else:
            serializer = WalletSerializer(data=data)
        if serializer.is_valid():

            obj_w = serializer.save()
            res = {}
            
            if obj_w.status == "enabled":
                res = {
                    "status": "success",
                    "data": {
                        "wallet": {
                            "id": obj_w.id,
                            "owned_by": obj_w.owned_by.id,
                            "status": obj_w.status,
                            "enabled_at": obj_w.enabled_at,
                            "balance": obj_w.balance
                        }
                    }
                }
            
            else:
                res = {
                    "status": "success",
                    "data": {
                        "wallet": {
                            "id": obj_w.id,
                            "owned_by": obj_w.owned_by.id,
                            "status": obj_w.status,
                            "disabled_at": obj_w.disabled_at,
                            "balance": obj_w.balance
                        }
                    }
                }


            return Response(res, status=status.HTTP_200_OK)
            
class DepositApiView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):

        wallet = Wallet.objects.filter(owned_by=request.user.id).first()
        
        if wallet.status == "enabled":
            amount = request.data.get('amount')
            data_deposit = {
                    "deposited_by": request.user.id,
                    "status": "success",
                    "amount": amount,
                    "reference_id": request.data.get('reference_id'),
                    "wallet_id": wallet.id,
            }

            data_wallet = {
                "balance": wallet.balance + amount
            }

            serializer_deposit = DepositSerializer(data=data_deposit)
            serializer_wallet = WalletSerializer(instance = wallet, data=data_wallet, partial = True)

            if serializer_deposit.is_valid() and serializer_wallet.is_valid():
                obj_deposit = serializer_deposit.save()
                serializer_wallet.save()

                res = {
                    "status": "success",
                    "data": {
                        "deposit": {
                            "id": obj_deposit.id,
                            "deposited_by": obj_deposit.deposited_by,
                            "status": obj_deposit.status,
                            "deposited_at": obj_deposit.deposited_at,
                            "amount": obj_deposit.amount,
                            "reference_id": obj_deposit.reference_id
                        }
                    }
                }

                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response(serializer_deposit.errors)
        else:
            return Response("Please enable wallet first", status=status.HTTP_400_BAD_REQUEST)


class WithdrawApiView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        
        wallet = Wallet.objects.filter(owned_by=int(request.user.id)).first()
        amount = request.data.get('amount')
        
        if wallet.status == "disabled":
            return Response("Please activate wallet first", status=status.HTTP_404_NOT_FOUND)

        if wallet.balance > int(amount):
            data_withdraw = {
                    "withdrawn_by" : request.user.id,
                    "status" : "success",
                    "amount" : amount,
                    "reference_id" : request.data.get('reference_id'),
                    "wallet_id" : wallet.id,
            }

            data_wallet = {
                "balance" : wallet.balance - amount
            }

            serializer_withdrawl = WithdrawSerializer(data=data_withdraw)
            serializer_wallet = WalletSerializer(instance = wallet, data=data_wallet, partial = True)

            if serializer_withdrawl.is_valid() and serializer_wallet.is_valid():
                obj_w = serializer_withdrawl.save()
                serializer_wallet.save()

                data_response = {
                        "status": "success",
                        "data": {
                            "withdrawal": {
                                "id": obj_w.id,
                                "withdrawn_by": obj_w.withdrawn_by.id,
                                "status": obj_w.status,
                                "withdrawn_at": obj_w.withdrawn_at,
                                "amount": obj_w.amount,
                                "reference_id": obj_w.reference_id
                            }
                        }
                    }
                    
                return Response(data_response, status=status.HTTP_200_OK)
            else:
                return Response(serializer_withdrawl.errors)
        else:
            return Response("Withdrawl amount more than Wallet balance", status=status.HTTP_404_NOT_FOUND)