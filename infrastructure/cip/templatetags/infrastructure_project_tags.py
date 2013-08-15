
from infrastructure.cip.models import *
from django import template
from django.core.urlresolvers import *
import urllib

register = template.Library()
phase_class = {
        'Design' : 'design',
        'Construction' : 'construction',
        'Post Construction' : 'post-construction',
        'Planning' : 'planning',
        'Bid and Award' : 'bid',
        'Complete' : 'completed'
        }
phase_images = {
        'Design' : '234_brush',
        'Construction' : '430_construction_cone',
        'Post Construction' : '331_dashboard',
        'Planning' : '335_pushpin',
        'Bid and Award' : '458_money',
        'Complete' : '206_ok_2'
        }
asset_type_class = {
        'Buildings': 'buildings',
        'Airports' : 'airport',
        'Storm Water Drainage' : 'storm-water-drainage ',
        'Parks' : 'parks',
        'Transportation' : 'transportation',
        'Sewer' : 'sewer',
        'Water' : 'water'
        }

asset_type_images = {
        'Buildings': 'commercial',
        'Airports' : 'airport',
        'Storm Water Drainage' : 'telephone',
        'Parks' : 'park2',
        'Transportation' : 'bus',
        'Sewer' : 'wetland',
        'Water' : 'water'
        }
@register.inclusion_tag('shortcuts.haml')
def show_shortcuts():
    """docstring for generate_shortcuts"""
    shortcuts = []
    phase_links = { 'links' : [], 'title': 'Phase' }
    for (key, value) in PROJECT_PHASES:
        phase_links['links'].append(generate_link('phase',key,value,phase_class[value]))
    shortcuts.append(phase_links)
    asset_group_links = { 'links' : [], 'title': 'Asset Type' }
    for (key, value) in ASSET_TYPE_GROUPS:
        asset_group_links['links'].append(generate_link('asset_group',key,value, asset_type_class[value]))
    shortcuts.append(asset_group_links)
    client_departement_links = { 'links' : [], 'title': 'Current Projects by asset type group' }

    return {'shortcuts': shortcuts}

def generate_link(type,key,value,image_class):
    """docstring for generate_link"""
    link = {}
    link['url'] = reverse("projects_filter_list",kwargs={'filter':type, 'value':iri_to_uri(re.sub(r"[\(\)-]"," ",value))})
    link['name'] = value
    link['key'] = key
    link['image_class'] = image_class
    return link

@register.inclusion_tag('project_list_item.haml')
def project_list_item(project):
    """docstring for project_list_item"""
    project_link_path = reverse('project_detail', args=[project.id] )
    asset_type_image = "images/icons/%s-18.png" % asset_type_images[project.SP_ASSET_TYPE_GROUP] 
    return { 'project' : project, 'link': project_link_path, 'phase': phase_class[project.SP_PROJECT_PHASE], 'asset_type_image': asset_type_image }

@register.inclusion_tag('pagination.haml',takes_context=True)
def pagination(context):
    """docstring for pagination"""
    return {
        'paginator': context['paginator'],
        'page_obj': context['page_obj']
        }
@register.inclusion_tag('pagination_count', takes_context=True)
def pagination_count(context):
    """docstring for pagination_count"""
    return {
        'paginator': context['paginator'],
        'page_obj': context['page_obj']
        }
