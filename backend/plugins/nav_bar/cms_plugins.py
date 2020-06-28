from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from backend.plugins.default.module_name import MODULE_NAME
from backend.plugins.default.nav_bar.models import NavBarPluginModel


@plugin_pool.register_plugin
class NavBarPlugin(CMSPluginBase):
    module = MODULE_NAME
    name = _("Navigation Bar")
    model = NavBarPluginModel
    render_template = 'nav_bar/nav_bar.html'