import xmlrpc.client

# configuration
url = 'https://demo4.odoo.com/'
db = 'demo_saas-172_2ba3f9eb7a15_1716965727'
username = 'admin'
password = 'admin'

# common endpoint
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/common')
uid = common.authenticate(db,username,password,{})

if uid:
    # object endpoint
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/object')

    # example Read partner records

    # create
    # models.execute_kw(db,uid,password,'res.partner','create',
    #                   [{'name': 'ramukaka'}])

    # write
    # models.execute_kw(db, uid, password, 'res.partner', 'write',
    #                   [[92],{'name': 'rajukaka'}])

    # search_count
    # count = models.execute_kw(db, uid, password, 'res.partner', 'search_count',[[['customer_rank','>',0]]])
    # print(count)

    # searching ramukaka
    # partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search',
    #                                 [[['name', '=', 'ramukaka']]])

    # unlink
    # models.execute_kw(db, uid, password, 'res.partner', 'unlink',
    #                   [partner_id])

    # read
    # customer_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['customer_rank', '>', 0]]])
    # read_records = models.execute_kw(db, uid, password, 'res.partner', 'read', [customer_ids],{'fields':['name']})
    # for record in read_records:
    #     print(record)

    # search_read
    partners = models.execute_kw(db,uid,password,
                                 'res.partner','search_read',
                                 [[]],{'fields':['name'],'limit':5})
    for partner in partners:
        print(partner)
else:
    print('authentication failed')