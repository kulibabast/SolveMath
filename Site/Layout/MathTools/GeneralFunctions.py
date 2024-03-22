def split_params(params):
    return params.split('=')[1]

def split_params_for_equation(params):
    return '='.join(params.split('=')[1:])