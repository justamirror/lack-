import re
def cilf(l, func):
  x = True
  for val in l: x = x and func(val)
  return x
class GenericError(Exception):
  pass
class CommandNotFound(GenericError):
  pass
class ValueInterpretingError(GenericError):
  pass
class STR():
    def __init__(self, content):
        self.content = content
    def __str__(self):
        return self.content
    def __repr__(self):
        return f"'{str(self)}'"
class LIST(list):
  pass
class NULL():
    def __str__(self):
        return "null"
    def __repr__(self):
        return f'null'
def EXECorEVAL(val):
  try:
    return EVAL(val)
  except Exception:
    return EXEC(val)
def EVAL(val):
    TYPE = None
    if val in re.findall("^'.*'", val.replace('"', "'")):
        TYPE = STR
        val = val[1:-1]
    elif val in re.findall("^'.*'", val.replace('"', "'")):
        TYPE = LIST
    if TYPE == None:
      raise ValueInterpretingError(f"Could not process value {val}")
    evalval = TYPE(str(val))
    return evalval
def proc(lines, linenum):
        line = lines[linenum]
        served = LIST([])
        args = line.split(" ")
        command = args.pop(0)
        args = " ".join(args)
        if command=="serve":
          served.append(EXECorEVAL(args))
        elif command=="moveplate":
          if args.isdigit():
            if int(args)>len(lines):
              raise ValueInterpretingError(f"Could not process value {args} because it is not a vaild number.")
            return (served, int(args)-1)
          else:
            raise ValueInterpretingError(f"Could not process value {args} because it is not a vaild number.")
        else:
          EXECorEVAL(line)
        return (served, linenum+1)
def EXEC(i):
  args = i.split(" ")
  command = args[0]
  del args[0]
  args = " ".join(args)
  if command == "spit": # Print.
    print(EXECorEVAL(args))
  elif command == "digest": # Eval, if error try to exec.
    return EXECorEVAL(args)
  elif command == "smell": # Repr.
    return repr(EXECorEVAL(args))
  elif command == "moveplate": # Goto.
    pass
  elif command == "eat": # Run script.
    served = LIST([])
    with open(str(EXECorEVAL(args)), "r") as file:
      lines = file.read().replace("\n", ";").split(";")
      linenum = 0
      while linenum<len(lines):
        x = proc(lines, linenum)
        served+=x[0]
        linenum=x[1]
    return served
  elif command=="serve": # When put in a script, serve will pass its args to eat. This does not stop the script.
    return EXECorEVAL(args)
  else: # Raise Command Not Found.
    raise CommandNotFound(f"Command {command} not found.")

  return NULL()
while True:
  try:
    i = input(">>> ")
    ei = EXECorEVAL(i)
    if ei:
      print(f"=> {repr(ei)}")
  except Exception as e:
    print(f"\033[91m{type(e).__name__}: {e}\033[0m")