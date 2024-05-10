import os
import random
import re
import string
from datetime import datetime

from django.contrib.auth.models import User
from django.http import JsonResponse

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
phone_regex = r'09(\d{9})$'


def is_it_numeric(txt):
    if txt is None or txt == '':
        return False
    if type(txt) is int:
        return True
    for char in txt:
        if not char.isdigit():
            return False
    return True


# Models Tools
def get_file_ext(filepath_and_name):
    # این اسم فایل و پسوندشو از بقیه جدا میکنه مثلا D:/1.jpg رو میگیره فقط 1.jpg رو برمیگردونه
    base_name = os.path.basename(filepath_and_name)
    # این اسم و پسوند فایل رو جدا میکنه
    name, ext = os.path.splitext(base_name)
    return name, ext


def is_image(filename):
    if filename:
        _, ext = os.path.splitext(filename)
        return ext.lower() in ('.jpg', '.jpeg', '.png')
    else:
        return False


def get_file_extension(file_name):
    _, extension = os.path.splitext(file_name)
    return extension


def is_valid_date(date_str, date_format='%m-%d-%Y'):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def is_valid_url(url):
    # Regular expression for URL validation
    url_pattern = re.compile(
        r"^(?:http|ftp)s?://"  # http:// or https:// or ftp://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or IP
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$", re.IGNORECASE)

    return bool(re.match(url_pattern, url))


def upload_image_path(instance, filename):
    name, ext = get_file_ext(filename)
    return f"images/profile_images/{instance.title.replace(' ', '-')}/{instance.title}{ext}"


def upload_image_with_rand_num_name(instance, filename):
    name, ext = get_file_ext(filename)
    rand = random.randint(1000, 9999)
    final = f"{instance}/{rand}{ext}"
    return final


def give_me_model_by_id(the_model, model_id):
    if not is_it_numeric(model_id):
        return None
    found_model = the_model.objects.filter(id=model_id, active=True)
    # found_model = the_model.objects.filter(id=id, active=True)
    if found_model.count() != 0:
        return found_model.first()
    return None


def email_to_url(email: str, add_random_num=False):
    split_mail = email.split('@')
    final_address = split_mail[0].replace('.', '')
    if add_random_num:
        final_address += str(random.randint(1000, 9999))
    return final_address


def is_it_email(_email):
    if re.fullmatch(email_regex, _email):
        return True
    else:
        return False


def is_it_password_with_nums_and_letters(password: str, min_len=8, max_len=50):
    if password is None:
        return False

    if (len(password) < min_len) or (len(password) > max_len):
        return False

    have_letter = False
    have_num = False

    for char in password:
        if char.isdigit():
            have_num = True
        elif char.isalpha():
            have_letter = True

    return have_letter and have_num


def validate_phone_number(phone):
    if phone is None or phone == '':
        return False
    if is_it_numeric(phone):
        int_phone = int(phone)
    else:
        return False

    if (phone[0] != '0' or phone[1] != '9') and (phone[0] != '۰' or phone[1] != '۹'):
        return False
    if re.fullmatch(phone_regex, '0' + str(int_phone)):
        return True
    else:
        return False


def is_ajax(req) -> bool:
    """
    Return Boolean response - if the request is AJAX : True; else: false
    """

    if req.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if req.headers.get('x-requested-with') == 'XMLHttpRequest':
            return True
    return False


def giveme_a_random_user_num():
    num = random.randint(10000, 99999)
    while True:
        if User.objects.filter(username=num).count() > 0:
            num = random.randint(10000, 99999)
        else:
            return num


def bad_request_ajax_error() -> JsonResponse:
    """
    return this function if the AJax Request is Bad (400)
    """
    # if response is None:
    response = {}
    # error_list = ["Error 400 -- Bad Request"]
    # response['is_there_error'] = False
    # response['error_list'] = error_list
    return JsonResponse(response, status=400)


def validate_name(name: str, english: bool = True, persian: bool = True, minlength: int = 2,
                  maxlength: int = 20) -> bool:
    """
    if the name is correct returns True else => false
    """

    english_name_regex = r"^[A-Za-z][A-Za-z]*$"
    persian_name_regex = r"^[\sآ-ی][\sآ-ی]*$"

    if not name:
        return False
    if len(name) > maxlength or len(name) < minlength:
        return False
    # the name cannot be english and persian at same time
    per_check = True
    eng_check = True
    if persian:
        if not re.fullmatch(persian_name_regex, name):
            per_check = False
    if english:
        if not re.fullmatch(english_name_regex, name):
            eng_check = False
    if persian and not per_check and not english:
        return False
    if english and not eng_check and not persian:
        return False

    if persian and english:
        if not (per_check != eng_check):
            return False
    return True


# region  API tools
def extract_matching_fields(the_model, the_dict):
    result = {}
    model_field_names = [field.name for field in the_model._meta.get_fields()]
    for key, value in the_dict.items():
        if key in model_field_names:
            result[key] = value
    return result


def password_generator(length: int) -> str:
    """Generate a random password of the specified length."""
    # Define the characters to choose from for the password
    characters = string.ascii_letters + string.digits + string.punctuation

    # Generate the password by randomly selecting characters
    password = ''.join(random.choice(characters) for _ in range(length))

    return password

# def google_recaptcha_verify(req):
#     recaptcha_response = req.POST.get('g_recaptcha_response')
#     url = 'https://www.google.com/recaptcha/api/siteverify'
#     values = {
#         'secret': settings.GOOGLE_SECRET_KEY,
#         'response': recaptcha_response
#     }
#     data = urlencode(values).encode()
#     recaptcha_req = lib_request.Request(url, data=data)
#     recaptcha_response = lib_request.urlopen(recaptcha_req)
#     recaptcha_result = json.loads(recaptcha_response.read().decode())
#
#     if recaptcha_result['success']:
#         return True
#     return False


# def giveme_datetime_now_iran():
#     return datetime.now(tz=pytz.timezone('Iran'))

# def log_it_in(req, user: User, password=None):
#     if user is not None:
#
#         if password:
#             rdy_to_login = authenticate(username=user.username, password=password)
#         else:
#             rdy_to_login = user
#
#         # keep Session for after login
#         sessions = EshopSessions(req)
#         login(request=req, user=rdy_to_login)
#         append_session_to_db(req=req, eshop_sessions=sessions)
#         return user
#
#     return None
