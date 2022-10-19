{
    'name': 'Chatbot',
    'version': '15.0.1.0',
    'category':'Productivity',
    'depends': [
        'base',
        'mail_bot',
    ],
    'data':[
        'security/ir.model.access.csv',
        'views/chatbot_settings.xml',
        'views/chatbot_view.xml',
        'views/command_view.xml',
        'views/menu.xml',
    ],
}