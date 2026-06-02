import moviepy, pkgutil, os
p = os.path.dirname(moviepy.__file__)
print('moviepy path:', p)
print('\nfiles:')
for fn in sorted(os.listdir(p)):
    print('-', fn)
print('\nmodules:')
for m in pkgutil.iter_modules([p]):
    print('-', m.name)
