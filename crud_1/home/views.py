# home/views.py
from django.views.generic import TemplateView
from django.apps import apps

class HomePageView(TemplateView):
    template_name = "home/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # intentamos obtener modelos (si existen)
        def safe_count(app_label, model_name):
            try:
                Model = apps.get_model(app_label, model_name)
                return Model.objects.count()
            except Exception:
                return None

        ctx['persona_count'] = safe_count('persona', 'Persona')
        ctx['oficina_count'] = safe_count('oficina', 'Oficina')
        return ctx

