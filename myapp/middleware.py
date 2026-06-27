import time
from django.http import HttpResponseForbidden

# Creating my own middleware 
class LogRequestMiddleware:
    def __init__(self,get_response):
         self.get_response = get_response

    def __call__(self,request): 
        #  process before
        print(f"[Middleware] Request Path:{request.path}")
        response = self.get_response(request) # it calls the next middleware 
        # process after view
        print(f"[Middleware] Response Status:{response.status_code}")
        return response

#Creating  a middleware to measure response time
class TimerMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start 
        print(f"[Middleware] Request took {duration:.2f} seconds")
        return response
    
# Creating a middleware to block some IP addresses
class BlockIPMiddleware:
    BLOCKED_IPS = [""]
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        ip = request.META.get("REMOTE_ADDR")
        if ip in self.BLOCKED_IPS:
            return HttpResponseForbidden("Your IP is blocked")
        return self.get_response(request)



