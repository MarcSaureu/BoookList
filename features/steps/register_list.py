from behave import *
import operator
from functools import reduce
from django.db.models import Q

use_step_matcher("parse")

@when(u'I register List')
def step_impl(context):
    for row in context.table:
        context.browser.visit(context.get_url('create_list'))
        form = context.browser.find_by_tag('form').first
        for heading in row.headings:
            context.browser.fill(heading, row[heading])
        form.find_by_value('Submit').first.click()

@then(u'I\'m viewing the details page for list by "{user}"')
def step_impl(context, user):
    q_list = [Q((attribute, context.table.rows[0][attribute])) for attribute in context.table.headings]
    from BookList.models import List
    list = List.objects.filter(reduce(operator.and_, q_list)).get()
    assert context.browser.url == context.get_url(list)

@then(u'There are {count:n} lists')
def step_impl(context, count):
    from BookList.models import List
    assert count == List.objects.count()
