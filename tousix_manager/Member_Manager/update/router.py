#    Copyright 2015 Rémy Lapeyrade <remy at lapeyrade dot net>
#    Copyright 2015 LAAS-CNRS
#
#
#    This file is part of TouSIX-Manager.
#
#    TouSIX-Manager is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    TouSIX-Manager is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with TouSIX-Manager.  If not, see <http://www.gnu.org/licenses/>.

from tousix_manager.Member_Manager.forms.router import RouterForm
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.core.mail import mail_admins
from tousix_manager.Authentication.LoginMixin import LoginRequiredMixin
from tousix_manager.Database.models import Hote, UserMembre
from tousix_manager.Member_Manager.update.UpdateMixin import UpdateUrlMixin


class RouterUpdateView(LoginRequiredMixin, UpdateView, UpdateUrlMixin, SuccessMessageMixin):
    """
    This view updates router associated with the requesting user.
    """
    model = Hote
    form_class = RouterForm
    template_name = "update_member.html"

    def get_object(self, queryset=None):
        return Hote.objects.filter(idmembre=UserMembre.objects.filter(user=self.request.user).first().membre.idmembre).first()

    def get_context_data(self, **kwargs):
        context = super(UpdateUrlMixin, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        return redirect(reverse("update member"))

    def form_valid(self, form):
        if form.has_changed():
            form.instance.valid = False
            form.save()
            return True
        return False

    def form_invalid(self, form):
        messages.error(self.request, "Erreur: Certains champs sont invalides.")

    def post(self, request, *args, **kwargs):
        hosts = []
        for hote in Hote.objects.filter(
                idmembre=UserMembre.objects.filter(user=self.request.user).first().membre.idmembre):
            hosts.append(RouterForm(data=request.POST, instance=hote, prefix="router_" + str(hote.idhote)))
        for router in hosts:
            if router.is_valid():
                if self.form_valid(router) is True:
                    messages.info(self.request,  "Changement routeur enregistré. Un administrateur doit confirmer la modification.")
                    subject = "Demande de changement paramètre routeur"
                    content = "Bonjour,\n\n Une demande a été envoyé pour appliquer les modifications sur le routeur "+ router.instance.nomhote+"."
                    mail_admins(subject, content)
        return self.render_to_response(self.create_context_data({"router": hosts}))

    def get_membre(self):
        return UserMembre.objects.filter(user=self.request.user).first().membre