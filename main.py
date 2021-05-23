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
class STR(str):
  pass
class LIST(list):
  pass
class NULL():
    def __str__(self):
        return "null"
    def __repr__(self):
        return f'null'
    def __bool__(self):
      raise ValueInterpretingError(f"Could not process value as it evaluated to nothing")
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
    elif val in re.findall("^.*==.*", val):
        val = val.split("==")
        val = EXECorEVAL(val[0]) == EXECorEVAL(val[1])
        if val:
          val = "a"
        else:
          val = ""
        TYPE=bool
    elif val=="true":
      val = "a"
      TYPE = bool
    elif val=="false":
      val = ""
      TYPE = bool
    if TYPE == None or type(val)==NULL:
      raise GenericError(f"Cannot convert null to bool.")
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
        elif command=='if':
          sargs = args.replace(": ",":").split(":")

          if EXECorEVAL(sargs[0]):
            a= sargs[1].split(" ")
            c = a.pop(0)
            a = " ".join(a)
            if c=="moveplate":
             if a.isdigit():
              if int(a)>len(lines):
                raise ValueInterpretingError(f"Could not process value {a} because it is not a vaild number.")
              return (served, int(a)-1)
            else:
              raise ValueInterpretingError(f"Could not process value {a} because it is not a vaild number.")
        elif command=="moveplate":
          if args.isdigit():
            if int(args)>len(lines):
              raise ValueInterpretingError(f"Could not process value {args} because it is not a vaild number.")
            return (served, int(args)-1)
          else:
            raise ValueInterpretingError(f"Could not process value {args} because it is not a vaild number.")
        EXECorEVAL(line)
        return (served, linenum+1)
def EXEC(i):
  args = i.split("#", 1)
  args = args[0]
  args = args.split(" ")
  command = args.pop(0)
  args = " ".join(args)
  if command == "spit": # Print.
    print(EXECorEVAL(args))
  elif command == "digest": # Eval, if error try to exec.
    return EXECorEVAL(EXECorEVAL(args))
  elif command == "smell": # Repr.
    return repr(EXECorEVAL(args))
  elif command == "moveplate": # Goto. Only works in a file.
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
  elif command=="serve": # When put in a file, serve will pass its args to eat. This does not stop the script. It always returns the args passed.
    return EXECorEVAL(args)
  elif command=="if":
    sargs = args.replace(": ",":").split(":")
    if EXECorEVAL(sargs[0]): EXECorEVAL(sargs[1])
  elif command=="": pass
  else: # Raise Command Not Found.
    raise CommandNotFound(f"Command {command} not found.")

  return NULL()
while True:
  try:
    i = input(">>> ")
    args = i.split("#", 1)
    args = args[0]
    args = args.split(" ")
    command = args.pop(0)
    del args
    ei = EXECorEVAL(i)
    if not command=="":
      print(f"=> {repr(ei)}")
  except Exception as e:
    print(f"\033[91m{type(e).__name__}: {e}\033[0m")