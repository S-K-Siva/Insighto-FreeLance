from django.contrib.auth.base_user import BaseUserManager
from .helpers import send_otp_phone
class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_superuser(self,phone,password=None,**kwargs):
        kwargs.setdefault('is_active',True)
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_superuser',True)
        if not phone:
            return ValueError("Phone number is required")
        
        verificationDone = False
        while True:
            getOTP = send_otp_phone(phone)
            entered_opt = input("Enter OTP:")
            if str(getOTP) == str(entered_opt):
                verificationDone = True
                break
            option = input("Do you want to continue (y/n):")
            if option not in ['Y','y']:
                break
        
        if not verificationDone:
            print("User Creation Stopped")
            return
        else:
            user = self.model(
                phone = phone,
                otp = getOTP,
                is_verified = True,
                **kwargs
            )
            user.set_password(password)
            user.save()
            return user
    def create_user(self,phone,password,otp,is_verified,**kwargs):
        print("Triggered")
        user = self.model(
            phone=phone,
            otp=otp,
            is_verified=is_verified,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user
    # def create_user(self,phone,password=None,**kwargs):
    #     if not phone:
    #         return ValueError("Phone number is required!")
        
    #     # verification of the phone number using twilio
    #     verificationDone = False
    #     while True:
    #         getOTP = send_otp_phone(phone)
    #         entered_otp = input("Enter OTP:")
    #         if str(entered_otp) == str(getOTP):
    #             verificationDone = True
    #             break
    #         option = input("Do you want to continue (y/n):")
    #         if option not in ['y','Y']:
    #             break
    #     if not verificationDone:

    #         print("User Creation Stopped")
    #         return
    #     else:
    #         user = self.model(
    #             phone = phone,
    #             otp = getOTP,
    #             is_verified = True,
    #             **kwargs
    #         )
    #         user.set_password(password)
    #         user.save()
    #         return user


            

    # def create_superuser(self,phone,password=None,**kwargs):
    #     kwargs.setdefault('is_active',True)
    #     kwargs.setdefault('is_staff', True)
    #     kwargs.setdefault('is_superuser', True)

    #     return self.create_user(phone,password,**kwargs)    