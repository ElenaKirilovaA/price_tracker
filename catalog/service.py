from catalog.models import Tag


def create_tags(tags_to_create: set) -> list or None:
    tag_titles_already_exist = (Tag.objects
                               .filter(title__in=tags_to_create)
                               .values_list('title', flat=True))  #  value_list flat=True -> ['cool', 'fun'] ;
                                                                         #  flat=False [('cool'), ('fun')];
                                                                         #  without valUe_list -> [<Tag: cool>, <Tag: fun>]
    new_tags = [Tag(title=t) for t in tags_to_create if t not in tag_titles_already_exist]  # bulk_create needs [obj]
    Tag.objects.bulk_create(new_tags)

    return new_tags
