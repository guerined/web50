# QR Club

QR Club is a Django web app that is used to generate dynamic QR code that redirect to a given URL

## Description

It consists of a 'traditional' website that describes the service: - Home: this is the home page which introduces the service - FAQ: provides answers to the most common questions about dynamic QR codes. - login: for users already registered to log into the app - register: for new users
We also have a few pages that can be reached in the footpage: terms of use, privacy and cookies.
Last but not least, we have a Contact Us page where a visitor can leave a message and this message is store in the database where a superuser can access them via the admin page.

A user has the ability to create an account with login and password to generate your QR code. The member section provides a dashboard where you can generate new QR code, see and download all QR codes created by you, as well as delete the qr codes you no longer wish to keep. In the profile section, you can change your password to a new one.

The QR code created are dynamic QR codes. Dynamic QR codes send users on to specific information or web pages, just like any other QR code. What makes them "dynamic" is that the URL encoded in them redirects to a second URL that can be changed on demand, even after a code is printed. Static QR codes can't be changed in that way. As such, on the dashboard we can see how many times a specific QR code has been scanned

## Distinctiveness and Complexity

The project by its nature (a QR code generator app) is very distinct from the other projects done so far: e-commerce, email app and social network.
The project leverages Bootstrap 5 in order to provide mobile responsiveness.
I have customized Bootstrap 5 leveraging SaSS (using scout on mac to compile bootstrap css)
On the FAQ page, I implemented a bootstrap accordion.
The complexity was to create dynamic qr codes. I had to create an URL shortener and then encode this shorten URL that redirects to the URL given by the user.
The complexity was to integrate a python library to create the QR code and manages the created image so that it can be downloaded by the user. It also include a register / login functionality with the possibility for a user to change its password. For security reason, the user will have to retype its current password before changing to a new one.

## Dependencies

The required dependencies are listed in the requirements/txt file located at the rood of the folder, and listed below:
asgiref==3.6.0
autopep8==2.0.1
backports.zoneinfo==0.2.1
bandit==1.7.4
Django==4.1.4
gitdb==4.0.10
GitPython==3.1.30
pbr==5.11.0
Pillow==9.3.0
pycodestyle==2.10.0
pypng==0.20220715.0
PyYAML==6.0
qrcode==7.4.2
smmap==5.0.0
sqlparse==0.4.3
stevedore==4.1.1
tomli==2.0.1
typing_extensions==4.6.3

## Project Files

The django project is called qrclub and is uses only one app called 'Pages'. HTML templates are located in the template folder and are leveraging partials for navbar, header and footer.
Assets as well as CSS and JS scripts are stored into a static folder.

## How to run QR Club

To run the project, install the requirements and then run "python3 manage.py runserver"
