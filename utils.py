def get_industries_featured():
    _industries = IndustryFocus.objects.filter(featured=True).order_by('order')
    industries = [{'text': i.title} for i in _industries]
    industries.append({'text': 'Другая'})
    return industries


def get_industries_featured_dry():
    _industries = IndustryFocus.objects.filter(featured=True).order_by('order')
    industries = [i.title for i in _industries]
    return industries