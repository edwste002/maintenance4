import sys, traceback

try:
    a  = 5/0

except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(exc_type, exc_value, exc_traceback)
