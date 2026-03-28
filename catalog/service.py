from django.template.defaulttags import now

from catalog.models import Tag, Category


def create_tags(tags_to_create: set) -> list or None:
    tag_titles_already_exist = set(Tag.objects
                               .filter(title__in=tags_to_create)
                               .values_list('title', flat=True))

    new_tags = [Tag(title=t) for t in tags_to_create if t not in tag_titles_already_exist]
    Tag.objects.bulk_create(new_tags)

    return new_tags

def get_context_catalog_data():
    category = (Category.objects
                .prefetch_related('products', 'products__alerts', 'products__tag', 'archives')
                .get(id=pk))
    last_deal_obj = category.archives.order_by('-alert_finished_at').first()
    products = category.products.all()

    last_deal = None
    if last_deal_obj:
        last_deal = (now().date() - last_deal_obj.alert_finished_at.date()).days
