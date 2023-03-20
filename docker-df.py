from collections import OrderedDict

import docker
import os 
import sys

client = None
try:
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
except Exception as err:
    print('Erro:')
    print("  * Docker não disponível")
    sys.exit(1)

disk_usage = {}

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def print_stats(path, size):
    dir_size = sizeof_fmt(size)
    print('  {0:>15} {1:>25} {2:<100}'.format(dir_size, size, path))

def get_dir_size(path='.'):
    if path in disk_usage:
        return disk_usage[path]

    total = 0
    try: 
        with os.scandir(path) as it:
            for entry in it:
                try:
                    if not entry.is_symlink():
                        if entry.is_file():
                            total += entry.stat().st_size
                        elif entry.is_dir():
                            total += get_dir_size(entry.path)
                except PermissionError as e:
                    pass
        disk_usage[path] = total
    except FileNotFoundError:
        pass

    return total

def get_df(path_list=list(), show_details=False):
    total = 0
    if path_list:
        for path in path_list:
            total += get_dir_size(path)
            if show_details:
                print_stats(path, total)

    return total
 
def get_df_graph(obj, paths=list(), add_internal_paths=False):
    if obj:
        if add_internal_paths:
            dirs = obj['LowerDir'].split(':')
            for dir in dirs:
                paths.append(dir)
        paths.append(obj['MergedDir'])
        paths.append(obj['UpperDir'])
        paths.append(obj['WorkDir'])

    return paths

def get_df_mounts(obj, paths=list()):
    if obj: 
        for mount in obj:
            if mount['Type'] == "volume":
                paths.append(mount['Source'])

    return paths

def get_container_paths(cnf, show_internal_paths = False):
    paths = list()
    if 'GraphDriver' in cnf and cnf['GraphDriver']:
        get_df_graph(cnf['GraphDriver']['Data'], paths, show_internal_paths)
    if 'Mounts' in cnf and cnf['Mounts']:
        get_df_mounts(cnf['Mounts'], paths)

    return paths

def get_container_df(cnf, ordered=True, show_internal_paths=False):
    sizes = dict()
    for path in get_container_paths(cnf, show_internal_paths):
        path_size = get_dir_size(path)
        sizes[path] = path_size

    if ordered:
        sizes = dict(sorted(sizes.items(), key=lambda item: item[1], reverse=True))

    return sizes

def get_container_data(cnf, ordered=True, show_internal_paths=False):
    name = cnf['Name']
    cid = cnf['Id']
    sid = cid[0:12]

    if name[0] == '/':
        name = name[1:]

    container = dict()
    container['id'] = cid
    container['sid'] = sid
    container['name'] = name

    c_paths = get_container_df(cnf, ordered, show_internal_paths)
    container['paths'] = c_paths

    instance_total = 0
    for _, size in c_paths.items():
        instance_total += size

    container['size'] = instance_total

    return container

def get_containers(ordered=True, show_internal_paths=False):
    containers = list()
    for container in client.containers(all=True):
        if not is_container_name(container, 'tool-docker-df'):
            cnf = client.inspect_container(container['Id'])
            ct = get_container_data(cnf, ordered, show_internal_paths)
            containers.append(ct)

    return containers

def print_container_df(cnf, show_internal_paths=False):
    
    container = get_container_data(cnf, True, show_internal_paths)

    print('=' * 150)
    print(' Nome: {0}'.format(container['name']))
    print(' Id  : {0}'.format(container['id']))
    print('=' * 150)
    print('  {0:>15} {1:>25} {2:<100}'.format("Tamanho", "Tamanho (Bytes)", "Path"))
    print('=' * 150)

    total = 0
    c_paths = container['paths']
    for path, size in c_paths.items():
        total += size
        print_stats(path, size)

    print('-'*50)
    print_stats('Total', total)
    print('')


def print_containers_list(show_internal_paths=False):
    print('=' * 145)
    print('  {0:<12}  {1:<75} {2:>25} {3:>25}'.format("Id", "Nome", "Tamanho", "Tamanho (Bytes)"))
    print('=' * 145)

    containers = get_containers(True, show_internal_paths)
    containers = list(sorted(containers, key=lambda item: item['size'], reverse=True))

    for ct in containers:
        total_size = sizeof_fmt(ct['size'])
        print('  {0:<12}  {1:<75} {2:>25} {3:>25}'.format(ct['sid'], ct['name'], total_size, ct['size']))

    print('-' * 145)


def is_container_name(container, term):
    if 'Names' in container:
        for name in container['Names']:
            if name == term or name == f'/{term}':
                return True
    return False

def is_container_id(container, term):
    if container['Id']:
        if container['Id'] == term or container['Id'][0:12] == term:
            return True
    return False

def search_container(term):
    for container in client.containers(all=True):
        if is_container_name(container, term) or is_container_id(container, term):
            return client.inspect_container(container['Id'])
    return None

def print_container_info(term, show_internals=False):
    cfg = search_container(term)
    if cfg:
        print_container_df(cfg, show_internals)        
    else:
        print('Not found')

def main():
    show_internals = False
    args = list()
    for arg in sys.argv:
        if arg == '--full' or arg == '-f':
            show_internals = True    
        else:
            args.append(arg)

    if len(args) > 1:
        print_container_info(args[1], show_internals)
    else:
        print_containers_list(show_internals)


if __name__ == '__main__':
    main()
