import functools
import email

'''
meta_args = {
    "email": {
        "to": ["madmouse@hacking.allowed.org"],
        "from": "madmouse@hacking.allowed.org",
        "subject": "Error",
        "credentials": ("madmouse", "@sshol3Z"),
        "server": "mail.hacking.allowed.org:25",
        "tls": False
    }
    "exceptions": {
        AttributeError: handler
    }
}
'''

def catch_exception(f, meta_args):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            if "exceptions" in meta_args:
                if type(e) in meta_args["exceptions"]:
                    meta_args["exceptions"][type(e)](e, f)
            else:
                message = "%s\nCaught a %s exception in %s: \n%s\n" % (
                        type(args[0]).__name__,
                        type(e).__name__,
                        f.__name__,
                        e.message if hasattr(e, "message") else e
                )
                if "email" in meta_args:
                    try:
                        email.sendemail(
                            meta_args["email"]["to"],
                            meta_args["email"]["from"],
                            meta_args["email"]["subject"], message,
                            meta_args["email"]["credentials"],
                            meta_args["email"]["server"],
                            tls=meta_args["email"]["tls"])
                    except Exception as e:
                        print("couldn't send email...\n%s\n%s" % (
                            e.message if hasattr(e, "message") else e,
                            message))
                else:
                    print(message)
    return func


class ErrorCatcher(type):
    class InvalidMetaArgs(Exception): pass
    
    
    def __new__(cls, name, bases, dct):
        if "meta_args" in dct:
            meta_args = dct["meta_args"]
        else:
            raise cls.InvalidMetaArgs

        for m in dct:
            if hasattr(dct[m], '__call__'):
                dct[m] = catch_exception(dct[m], meta_args)
        return type.__new__(cls, name, bases, dct)

