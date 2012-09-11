#!/usr/bin/env python

import sys, os, md5
import keyring
import cloudfiles

source_path = sys.argv[1]

pwd = keyring.get_password('Cloud Files', 'kgriffs')

connection = cloudfiles.get_connection('kgriffs', pwd)
container = connection.get_container('blog')

def hash(path):
  h = md5.new()
  f = open(path)
  while True:
    data = f.read(4096)
    if not data:
      break

    h.update(data)

  return h.hexdigest()

def list_local_filenames(dir, base = ''):
  paths = []

  dir_len = len(dir)
  if dir[-1] != os.sep:
    dir_len += 1

  for dirpath, dirnames, filenames in os.walk(dir):
    for filename in filenames:
      base = dirpath[dir_len:]

      if not filename.startswith('.') and not base.startswith('.'):
        paths.append(os.path.join(base, filename) if base else filename)

  return paths


local_paths = list_local_filenames(source_path)
remote_paths = [
  (entry['name'].encode('utf-8'), entry['hash'].encode('ascii')) for entry in container.list_objects_info()]

remote_paths_to_delete = []
remote_paths_to_skip = []
for remote_name, remote_hash in remote_paths:
  if remote_name not in local_paths:
    print 'To delete: ' + remote_name
    remote_paths_to_delete.append(remote_name)
  elif remote_hash == hash(os.path.join(source_path, remote_name)):
    print 'To skip: ' + remote_name
    remote_paths_to_skip.append(remote_name)
  else: 
    print 'To upload: ' + remote_name

for local_name in local_paths:
  if local_name not in remote_paths_to_skip:
    print 'To upload: ' + local_name

for local_name in local_paths:
  if local_name in remote_paths_to_skip:
    print 'Skipping: ' + local_name
    continue

  print 'Uploading ' + local_name
  #obj = container.create_object(local_name)
  #obj.load_from_filename(os.path.join(source_path, local_name))

for path_to_delete in remote_paths_to_delete:
  print 'Deleting ' + path_to_delete
  #container.delete_object(path_to_delete)
