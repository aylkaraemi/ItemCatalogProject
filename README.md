# Item Catalog Project - Reading List
A Project for the Udacity Full Stack Nanodegree

This web app runs a reading list app running off of the localhost domain. It allows logged in users to create and maintain a list of books to read. When not logged in the app displays a sample list of books. The user can view their full reading list, a list of books of a selected genre, or detail on a single book.

**Dependencies: (install details in the dependencies section)**
- Python 2.7 or 3
- Unix shell program
- VirtualBox & Vagrant
- web browser
- Google account - app uses Google's OAuth API for authentication so a Google account is required to log in
- Google client ID and secret to run the Google OAuth authentication

## Dependencies
This app requires python (2 or 3), VirtualBox, Vagrant, a Unix-style terminal to run the files. Instructions for downloading and installing each of these are below.

### Python
To download python click [here](https://www.python.org/downloads/) and select the version to install. This tool works on python version 2.7 and later so if you are using a version earlier than 2.7 you will need to upgrade.

_Note_: The site should detect the OS, but if not there are links to the installers for each OS directly below the button for the latest version.

Once the installer is downloaded, run it and follow the instructions to install.

### Unix shell
For Mac or Linux systems the built-in terminal program can be used.

For Windows you will need to download a program, such as Git Bash, if you do not already have one. You can download Git Bash [here](https://git-scm.com/downloads) and find information on how to use it [here](https://git-scm.com/doc).

### VirtualBox & Vagrant
VirtualBox and Vagrant work together to run the virtual machine this tool runs in. VirtualBox runs the VM and Vagrant is how the VM is accessed and used.

VirtualBox can be downloaded [here](https://www.virtualbox.org/wiki/Downloads). There are links for each OS in the section "VirtualBox 5.2.22 platform packages". Once the installer is downloaded, run it and follow the instructions.

_Note_: some users have difficulty using newer versions of VirtualBox with Vagrant, so you may need to use an older version of VirtualBox instead which can be downloaded [here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1).

Vagrant can be downloaded [here](https://www.vagrantup.com/downloads.html). Select the correct version for your OS and download and run the installer.

_Note_: if you are using Git Bash make sure to run it as an administrator or you may have issues getting vagrant to function

Documentation for Vagrant can be found [here](https://www.vagrantup.com/docs/index.html) to assist in troubleshooting any issues.

#### VM Configuration
To make sure you have the correct configuration of your VM you can either download the zipfile [here](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) or fork and clone [this](https://github.com/udacity/fullstack-nanodegree-vm) repository on GitHub.
Either link will give you a new directory containing the necessary VM files.

To start the VM:
1. change to the new directory using `cd`
2. inside is another directory called vagrant, change to that with `cd vagrant/`
3. enter the command `vagrant up` to prompt Vagrant to download the linux operating system and install it
4. once completed enter the command `vagrant ssh` to log in to the VM.
   - **note**: for some versions of Windows you may need to use `winpty vagrant ssh` instead
5. when you are ready to exit your vm type `exit` in the shell prompt to log out

If you wish to log in again you can just cd back to the vagrant directory and type `vagrant ssh` as long as you have not rebooted your computer. If you reboot your computer, you will need to use `vagrant up` again to initialize the vm, then `vagrant ssh` to log in.

**Note** Troubleshooting tips and VM configuration instructions sourced from Udacity "Installing the Virtual Machine" lesson within the Intro to Relational Databases course.

### Web Browser
This app should work on any web browser. Most computers come with browsers installed, but if an alternative is desired I recommend [Firefox](https://www.mozilla.org/en-US/firefox/new/) or [Chrome](https://www.google.com/chrome/).

### Google Account
If you wish to use this app but do not already have a Google account you can sign up [here](https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp).

## Running the Web App
### Downloading the files
To download the files for this app simply click the green 'Clone or download' button above the list of files. If you have Git you can use this button to clone the repo to your computer, or you can simply choose to download the files as a ZIP file.

The files and directories downloaded will need to be saved inside the vagrant directory located inside the directory you set your virtual machine up in. I recommend creating a new directory inside the vagrant directory to keep the files and directories together and organized.

### Getting a Client ID and Secret from Google
To generate a client Id and secret to use with the Google OAuth API you will need to go to [https://console.developers.google.com](https://console.developers.google.com).

Once there, log in and follow the instructions for [Step 1: Create a client ID and client secret](https://developers.google.com/identity/sign-in/web/server-side-flow). The Authorized JavaScript origins URL and the Authorized redirect URI should both be `http://localhost:8000` **Note:** The instructions say you do not need to enter a redirect URI but there will be issues with the authentication if you do not.

Once you have created the project and generated the credentials, download the ID and secret as a JSON file (use the download button on the far right of the client ID).

Rename the file it to 'client_secrets.json' and save it to the same directory as the other Reading List app files.

You will also need to copy the client ID from the dashboard and paste it in the login.html file (located in the 'templates' directory) within the code for the Google Sign-in button where it says `data-clientid=`.

### Setting up the Database
Change to the directory you saved the files to (either /vagrant or the directory you created inside /vagrant) so you can access them.

Enter the command `python models.py` to initialize the database.

Enter the command `python samplelist.py` to load the database with the sample data to be displayed when there is no logged in user.

### Setting Up the Web App
Enter the command `python views.py` to run the Flask web server.

In your browser visit `http://localhost:8000` to view the Reading List app.

You will see the full sample reading list on visiting the main page. Clicking on one of the genre categories will allow you to view all sample books of that genre. Clicking on an individual book will allow you to view the detail page about that book. You will not be able to add, edit or delete any of the sample data.

Clicking the login button at the top will allow you to login using your Google account. Once successful you will be brought to your personal reading list. You will be able to access the same views for your personal list (full list, genre list and specific book) as well as being able to add, edit or delete books.