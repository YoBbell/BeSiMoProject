# from datetime import datetime, time
# from django.shortcuts import redirect

# class StoreStatusMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         now = datetime.now().time()
#         if not is_store_open(now):
#             if not request.path.startswith('/closed'):
#                 return redirect('/closed')
#         response = self.get_response(request)
#         return response

# def is_store_open(now):
#     opening_time = time(9, 0)  # replace with actual opening time
#     closing_time = time(22, 0)  # replace with actual closing time
#     return opening_time <= now <= closing_time
