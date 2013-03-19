import string
import random

def confirm(prompt_str="Confirm", allow_empty=False, default=False):
  fmt = (prompt_str, 'y', 'n') if default else (prompt_str, 'n', 'y')
  if allow_empty:
    prompt = '%s [%s]|%s: ' % fmt
  else:
    prompt = '%s %s|%s: ' % fmt
 
  while True:
    ans = raw_input(prompt).lower()
 
    if ans == '' and allow_empty:
      return default
    elif ans == 'y':
      return True
    elif ans == 'n':
      return False
    else:
      print 'Please enter y or n.'

def option(prompt_str="", allow_empty=False, default=False):
  fmt = (prompt_str, default) if default else (prompt_str, '')
  if allow_empty:
    prompt = '%s [%s]: ' % fmt
  else:
    prompt = '%s %s: ' % fmt

  while True:
    ans = raw_input(prompt).lower()
 
    if allow_empty:
      if ans == '':
        return default
      return ans
    else:
      if ans != '':
        return ans

def password_generator(size=12, chars=string.ascii_letters + string.digits):
  return ''.join(random.choice(chars) for x in range(size))