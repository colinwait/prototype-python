import os
import time
from os import path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def index(request):
    context = {
        "categories": __getCategories(),
        "types": __getTypes(),
        'schnappis': __getSchnappis()
    }
    return render(request, 'prototype/index.html', context)


def list(request, category):
    request_type = request.GET.get('type', 'prototypes')

    prototype_path = settings.BASE_DIR + settings.PROTOTYPE_PATH
    files = {}
    files[category] = {}
    types = __getTypes()
    categories = __getCategories()

    for tp, type_name in types.items():
        files[category][tp] = []
        type_dir = prototype_path + category + '/' + tp

        if not os.path.isdir(type_dir):
            continue
        type_files = os.listdir(type_dir)

        for type_file in type_files:
            type_file_path = type_dir + '/' + type_file
            file_info = {}
            file_info['name'] = type_file
            update_time = os.stat(type_file_path).st_ctime
            file_info['update_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(update_time))
            if os.path.isdir(type_file_path) and not os.path.isfile(type_file_path + '/index.html'):
                continue

            if os.path.isdir(type_file_path):
                file_info['url'] = 'http://' + request.get_host() + settings.PROTOTYPE_PATH \
                                   + category + '/' + tp + '/' + type_file + '/index.html'
            else:
                file_info['url'] = 'http://' + request.get_host() + settings.PROTOTYPE_PATH \
                                   + category + '/' + tp + '/' + type_file
            files[category][tp].append(file_info)

    # context = {
    #     'files': files,
    #     "types": types,
    #     'current_type': request_type,
    #     'category': category,
    #     "categories": categories,
    #     'test': files
    # }
    #
    # return render(request, 'test.html', context)

    context = {
        'files': files,
        "types": types,
        'current_type': request_type,
        'category': category,
        "categories": categories,
        'schnappis': __getSchnappis()
    }

    return render(request, 'prototype/list.html', context)


def __getCategories():
    cat = {
        'new-m2o': 'M2O-Plus',
        'yindou': '音豆',
        'team': '协同',
        'fusion': '融合号',
        'factory': '工厂',
        'cloud': '云服务',
        'ai': 'AI',
        'party': '党建',
    }

    return cat


def __getTypes():
    types = {
        'prototypes': '原型文档',
        'designs': '设计稿（标注）',
        'docs': '普通文档',
    }

    return types


def __getSchnappis():
    static_url = settings.STATIC_URL
    schnappi_dir = 'images/schnappis/'
    static_dir = settings.BASE_DIR + static_url + schnappi_dir
    files = os.listdir(static_dir)
    schnappis = []
    for file in files:
        schnappis.append(static_url + schnappi_dir + file)

    return schnappis
