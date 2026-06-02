import importlib
try:
    import moviepy
    print('moviepy OK', getattr(moviepy,'__file__',None))
    try:
        import moviepy.editor
        print('moviepy.editor OK')
    except Exception as e:
        print('moviepy.editor ERR', type(e).__name__, e)
except Exception as e:
    print('moviepy ERR', type(e).__name__, e)
