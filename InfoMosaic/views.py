import random
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.db import connection
# from django.contrib.sessions import session
from django.conf import settings
from azure.storage.blob import BlobServiceClient

# Create your views here.

# Website First Page


def welcome(request):
    if request.method == "POST":
        return render(request, "first.html")
    return render(request, "Welcome.html")

# Service Provider or User Selection Page


def user(request):
    return render(request, "first.html")

# Service Provider Sign Up page


def spSignUp(request):
    return render(request, "serviceProvider_signup.html")


def spsignedup(request):
    if request.method == "POST":
        name_entered = request.POST['fullname']
        username_entered = request.POST['username']
        password = request.POST['password']
        email_entered = request.POST['email']
        phoneno_entered = request.POST['phoneno']
        services = request.POST['service']
        location_entered = request.POST['location']
        print(name_entered)
        print(username_entered)
        print(password)
        print(email_entered)
        print(location_entered)
        # Generate a random service provider ID
        provider_id = random.randint(1000, 9999)
        print(provider_id)

        # Split the services string into a list of individual services
        service_list = [service.strip() for service in services.split(',')]
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM spDetails WHERE sp_username = %s", [username_entered])
            row = cursor.fetchone()
            if row[0] > 0:
                error_message = 'Username already exists'
                return render(request, 'serviceProvider_signup.html', {'error_message': error_message})
            else:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO spDetails (providerId,sp_username,password) VALUES (%s,%s,%s)", [
                                   provider_id, username_entered, password])
                    for service in service_list:
                        cursor.execute(
                            "INSERT INTO service_provider (providerId,name,email,phoneNo,service,location) VALUES (%s,%s,%s,%s,%s,%s)", [
                                provider_id, name_entered, email_entered, phoneno_entered, service, location_entered]
                        )
    return render(request, "InfoMosaic.html")

# Service Provider account Login Page


def splogin(request):
    if request.method == "POST":
        login_username = request.POST['login_username']
        login_password = request.POST['login_password']
        print(login_username)
        print(login_password)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM spDetails WHERE sp_username = %s", [login_username])
        row = cursor.fetchone()

        user_exists = row[0] > 0
        if user_exists:
            # Verify the password for the user
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM spDetails WHERE sp_username = %s AND password = %s", [
                               login_username, login_password])
                row = cursor.fetchone()
                password_matches = row[0] > 0

            if password_matches:
                # Password is correct, redirect to another page
                # Replace 'another_page' with the actual URL name or path
                request.session['username'] = login_username
                return redirect("edit")
            else:
                # Password is incorrect
                error_message = 'Incorrect password'
        else:
            # User does not exist
            error_message = 'User does not exist'

        context = {'error_message': error_message}

        return render(request, "InfoMosaic.html", context)
    return render(request, "InfoMosaic.html")

# Edit Service Provider Account details Page


def sp(request):
    if 'username' in request.session:
        username = request.session.get('username')
        # Fetch the user's information from the database
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT providerId from spDetails WHERE sp_username=%s", [username])
            row = cursor.fetchone()
            providerId = row
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name,email,phoneNo,location FROM service_provider WHERE providerId = %s", [providerId])
            row = cursor.fetchone()
            if row:
                sp_fullname = row[0]
                sp_email = row[1]
                sp_phoneno = row[2]
                sp_location = row[3]
                cursor.execute(
                    "SELECT service FROM service_provider WHERE providerId = %s", [providerId])
                services_rows = cursor.fetchall()
                services = [row[0] for row in services_rows]
                user = {
                    'username': username,
                    'name': sp_fullname,
                    'email': sp_email,
                    'phone': sp_phoneno,
                    'location': sp_location,
                    'services': services
                }
            else:
                # Handle the case when the user doesn't exist in the database
                user = None
        if request.method == "POST":
            action = request.POST.get('action')
            if action == 'update':
                password = request.POST['sp_password']
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT COUNT(*) FROM spDetails WHERE sp_username = %s", [username])
                row = cursor.fetchone()
                user_exists = row[0] > 0
                if user_exists:
                    # Verify the password for the user
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT COUNT(*) FROM spDetails WHERE sp_username = %s AND password = %s", [
                            username, password])
                        row = cursor.fetchone()
                        password_matches = row[0] > 0
                        if password_matches:
                            if 'sp_fullname' in request.POST:
                                fullname = request.POST.get('sp_fullname')
                                with connection.cursor() as cursor:
                                    cursor.execute("UPDATE service_provider SET name = %s WHERE providerId = %s", [
                                        fullname, providerId])

                            if 'sp_email' in request.POST:
                                email = request.POST.get('sp_email')
                                with connection.cursor() as cursor:
                                    cursor.execute("UPDATE service_provider SET email = %s WHERE providerId = %s", [
                                        email, providerId])

                            if 'sp_phoneno' in request.POST:
                                phoneno = request.POST.get('sp_phoneno')
                                with connection.cursor() as cursor:
                                    cursor.execute("UPDATE service_provider SET phoneNo = %s WHERE providerId = %s", [
                                        phoneno, providerId])

                            if 'sp_location' in request.POST:
                                location = request.POST.get('sp_location')
                                with connection.cursor() as cursor:
                                    cursor.execute("UPDATE service_provider SET location = %s WHERE providerId = %s", [
                                        location, providerId])
                            error_message = 'Profile updated successfully.'
                        else:
                            # If password doesn't matches
                            error_message = 'Incorrect Password.'
                        context = {
                            'user': user,
                            'error_message': error_message
                        }
                        return render(request, "serviceprovider.html", context)
            elif action == 'logout':
                # Log out of account
                del request.session['username']
                if 'session_key' in request.session:
                    print("hey")
                else:
                    print("No")
                error_message = 'You have been logged out successfully.'
                return render(request, "InfoMosaic.html", {'error_message': error_message})
        return render(request, "serviceprovider.html", {'user': user, })
    return render(request, "serviceprovider.html")

# Log out of account


def logout(request):

    return render(request, "InfoMosaic.html")

# User Sign Up Page


def signIn(request):
    if request.method == "POST":
        name_entered = request.POST['Fullname']
        username_entered = request.POST['Username']
        password = request.POST['Password']
        email_entered = request.POST['Email']
        phoneno_entered = request.POST['Phoneno']
        print(name_entered)
        print(username_entered)
        print(password)
        print(email_entered)
        print(phoneno_entered)
        # Generate a random service provider ID
        user_id = random.randint(10000, 99999)
        print(user_id)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM userDetails WHERE username = %s", [username_entered])
            row = cursor.fetchone()
            if row[0] > 0:
                error_message = 'Username already exists'
                return render(request, 'userSignUp.html', {'error_message': error_message})
            else:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO userDetails (userId,name,username,password,phoneno,email) VALUES (%s,%s,%s,%s,%s,%s)", [
                                   user_id, name_entered, username_entered, password, phoneno_entered, email_entered])
                    return render(request, "login.html")
    return render(request, "userSignUp.html")


def usersignUp(request):
    if request.method == "POST":
        name_entered = request.POST.get['Fullname']
        username_entered = request.POST.get['Username']
        password = request.POST.get['Password']
        email_entered = request.POST.get['Email']
        phoneno_entered = request.POST.get['Phoneno']
        print(name_entered)
        print(username_entered)
        print(password)
        print(email_entered)
        print(phoneno_entered)
        # Generate a random service provider ID
        user_id = random.randint(10000, 99999)
        print(user_id)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM userDetails WHERE username = %s", [username_entered])
            row = cursor.fetchone()
            if row[0] > 0:
                error_message = 'Username already exists'
                return render(request, 'userSignUp.html', {'error_message': error_message})
            else:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO userDetails (userId,name,username,password,phoneno,email) VALUES (%s,%s,%s,%s,%s)", [
                                   user_id, name_entered, username_entered, password, phoneno_entered, email_entered])
                    return render(request, "login.html")
    return render(request, "userSignUp.html")

# User Log In Page


def login(request):
    return render(request, "login.html")


def home(request):
    if request.method == "POST":
        login_username = request.POST['loginusername']
        password_entered = request.POST['password']
        print(login_username)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM userDetails WHERE username = %s", [login_username])
        row = cursor.fetchone()

        user_exists = row[0] > 0
        if user_exists:
            # Verify the password for the user
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM userDetails WHERE username = %s AND password = %s", [
                               login_username, password_entered])
                row = cursor.fetchone()
                password_matches = row[0] > 0

            if password_matches:

                # Password is correct, redirect to another page
                # Replace 'another_page' with the actual URL name or path
                return redirect("main")
            else:
                # Password is incorrect
                error_message = 'Incorrect password'
        else:
            # User does not exist
            error_message = 'User does not exist'

        context = {'error_message': error_message}

        return render(request, "login.html", context)
    return render(request, "login.html")

# Main Page


def main(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT DISTINCT location FROM service_provider')
        locations = [row[0] for row in cursor.fetchall()]
        cursor.execute('SELECT DISTINCT service FROM service_provider')
        services = [row[0] for row in cursor.fetchall()]
        cursor.execute('SELECT DISTINCT ratings FROM service_provider')
        ratings = [row[0] for row in cursor.fetchall()]
    if request.method == "GET":
        location_entered = request.GET.get('location')
        service_entered = request.GET.get('service')
        rating_entered = request.GET.get('rating')

        query = """
            SELECT * FROM service_provider
            WHERE
                (location = %s OR %s IS NULL OR %s = '') AND
                (service = %s OR %s IS NULL OR %s = '') AND
                (ratings >= %s OR %s IS NULL)
        """
        params = [location_entered, location_entered, location_entered, service_entered,
                  service_entered, service_entered, rating_entered, rating_entered]
        params = [param if param is not None and param !=
                  '' else None for param in params]

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()

            search_params = {
                'location': location_entered,
                'service': service_entered,
                'ratings': rating_entered,
            }

            if not any(params):  # Check if any search parameter is None or empty
                results = None

        return render(request, "main.html", {'locations': locations, 'services': services, 'ratings': ratings, 'results': results, 'search_params': search_params})
    return render(request, "main.html", {'locations': locations, 'services': services, 'ratings': ratings})


"""def sp_home(request):
    if request.method == 'POST':
        document_file = request.FILES.get('documen')
        blob_service_client = BlobServiceClient.from_connection_string(
            settings.AZURE_STORAGE_CONNECTION_STRING)
        container_name = 'verificationdocument'
        file_name = document_file.name
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=file_name)
        blob_client.upload_blob(document_file)
        print("Success")
    return render(request, "sp_first.html")"""


def sp_home(request):
    if 'username' in request.session:
        username = request.session['username']
        print(username)
        return render(request, 'serviceprovider.html', {'username': username})
    else:
        return redirect('edit')
