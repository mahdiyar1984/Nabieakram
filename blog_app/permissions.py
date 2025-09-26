ACCESS_RIGHTS = {
    'ArticleCategory': {
        'admin':    ['add', 'change', 'delete', 'view_all'],
        'editor':   ['add', 'change', 'delete', 'view_all'],
        'author':   ['view_select'],  # فقط انتخاب در فرم
        'subscriber':['view_all']
    },
    'ArticleTag': {
        'admin':    ['add', 'change', 'delete', 'view_all'],
        'editor':   ['add', 'change', 'delete', 'view_all'],
        'author':   ['view_select'],  # فقط انتخاب در فرم
        'subscriber':['view_all']
    },
    'Article': {
        'admin':    ['add', 'change', 'delete', 'view_all'],
        'editor':   ['add', 'change', 'delete', 'view_all'],
        'author':   ['add_myself', 'change_myself', 'delete_myself', 'view_myself', 'view_published'],
        'subscriber':['view_published']
    },
    'ArticleComment': {
        'admin':    ['add', 'change', 'delete', 'view_all'],
        'editor':   ['add', 'change', 'delete', 'view_all'],
        'author':   ['add_myself', 'change_myself', 'delete_myself', 'view_myself'],
        'subscriber':['view_published']
    }
}
