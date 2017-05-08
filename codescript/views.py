import os

import simplejson
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from Djangoooo4.settings import BASE_DIR
from codescript.forms import CodeForm
from codescript.models import CodeScript


def code_scripts(request):
    list = CodeScript.objects.all()
    paginator = Paginator(list, 3)  # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)
    return render(request, "codeScripts.html", {"list": list})


@login_required
def save_code_script(request):
    context = {'error': ''}
    homeDir = os.getcwd()

    if request.method == 'POST':
        # form must contain 'content' field
        if request.POST.__contains__('title'):
            codeFolder = "codes"
            user_id = request.user.id
            path = os.path.join(BASE_DIR, 'media', codeFolder, str(user_id), request.POST['title'])
            if not os.path.exists(path):
                os.makedirs(path)
            os.chdir(path)
            writeFile(request.POST['html'], "temp.html", context)
            writeFile(request.POST['js'], "temp.js", context)
            writeFile(request.POST['css'], "temp.css", context)
            html_path = os.path.join(path, "temp.html")
            css_path = os.path.join(path, "temp.css")
            js_path = os.path.join(path, "temp.js")
            code = CodeScript(title=request.POST['title'],
                              html_file_path=html_path,
                              css_file_path=css_path,
                              js_file_path=js_path,
                              creator=request.user)
            code.save()
            print(code.id)
            return_dict = {'message': 'code script saved ', 'code': ''}
            json = simplejson.dumps(return_dict)
            os.chdir(homeDir)
            return HttpResponse(json)
        else:
            context['error'] += 'Request doen not contain any content to create the file.\n'
    else:
        context['error'] += 'Request type must be POST.\n'

    return_dict = {'message': 'code script saved ', 'code': ''}
    # json = simplejson.dumps(return_dict)
    return HttpResponseRedirect("codenow/", "success")


@login_required
def load_code_script(request, id):
    context = {'error': ''}
    code_script = CodeScript.objects.get(id=id)
    html = code_script.html_file_path
    css = code_script.css_file_path
    js = code_script.js_file_path
    codeName = code_script.title
    readFile(html, context)
    htmlContent = context['fileContent']
    readFile(css, context)
    cssContent = context['fileContent']
    readFile(js, context)
    jsContent = context['fileContent']
    form = CodeForm(request.POST or None,initial={'title':codeName})

    context = {'code': code_script, 'form': form, 'html': htmlContent, 'css': cssContent, 'js': jsContent,
               'title': codeName}
    return render(request, "CodeNow.html", context)


@login_required
def new_code_script(request):
    form = CodeForm(request.POST or None)
    context = {'form': form}
    return render(request, "CodeNow.html", context)


# file handling function

def openFile(fileName, mode, context):
    # open file using python's open method
    # by default file gets opened in read mode
    try:
        fileHandler = open(fileName, mode)
        return {'opened': True, 'handler': fileHandler}
    except IOError:
        context['error'] += 'Unable to open file ' + fileName + '\n'
    except:
        context['error'] += 'Unexpected exception in openFile method.\n'
    return {'opened': False, 'handler': None}


def readFile(fileName, context):
    # open file in read-only mode
    fileHandler = openFile(fileName, 'r', context)

    if fileHandler['opened']:
        # create Django File object using python's file object
        file = File(fileHandler['handler'])

        # we have atleast empty file now
        context['fileContent'] = ''
        # use chunks to iterate over the file in chunks.
        # this is helpful when file is large enough.
        # '10' represents the size of each chunk
        for chunk in file.chunks(10):
            context['fileContent'] += chunk

        # make sure to close the file before exit
        file.close()


def writeFile(content, fileName, context):
    # open file write mode
    fileHandler = openFile(fileName, 'w', context)

    if fileHandler['opened']:
        # create Django File object using python's file object
        file = File(fileHandler['handler'])
        # write content into the file
        file.write(content)
        # flush content so that file will be modified.
        file.flush()
        # close file
        file.close()


def deleteFile(fileName, context):
    try:
        os.remove(fileName)
    except:
        context['error'] += 'Exception raised while deleting temp file.\n'
    pass
