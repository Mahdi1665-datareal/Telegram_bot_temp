import functools
import time
from langdetect import detect
from deep_translator import (GoogleTranslator, single_detection)

def singleton(cls):
    instances = {}
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

def count_use_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if (args[1].from_user.first_name) in wrapper.user_message_count:
            wrapper.user_message_count[str(args[1].from_user.first_name)] += 1
        else:
            wrapper.user_message_count[str(args[1].from_user.first_name)] = 1
        print(f"Function {func.__name__} has been used {wrapper.user_message_count[str(args[1].from_user.first_name)]} times by {args[1].from_user.first_name}")        
        return func(*args, **kwargs)
    wrapper.user_message_count = {}
    return wrapper

def message_time_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        
        normal_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(args[1].date))
        
        if  time.localtime().tm_hour< 12:
            wrapper.message_time = "morning"
        elif time.localtime().tm_hour < 18:
            wrapper.message_time = "afternoon"
        else:
            wrapper.message_time = "evening"
            
        print(f"Message time: {wrapper.message_time}")
        return func(*args, **kwargs)
    wrapper.message_time = None
    return wrapper

def message_lang_detect_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.detected_lang = detect(args[1].text)
        return func(*args, **kwargs)
    wrapper.detected_lang = None
    return wrapper




