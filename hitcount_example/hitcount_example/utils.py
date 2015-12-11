def example_custom_callback(request, object_pk=None, ctype_pk =None):
    return 'this is the callback response! object_pk = %s ctype_pk = %s' % (str(object_pk), str(ctype_pk))