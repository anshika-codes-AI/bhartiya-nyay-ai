from transition_engine.models import LegalSection, SectionMapping


def map_ipc_to_bns(ipc_sections):
    """
    ipc_sections: list of strings, e.g. ["IPC 420"]
    """
    mappings = []

    for sec in ipc_sections:
        try:
            act, number = sec.split()
        except ValueError:
            continue

        try:
            ipc_obj = LegalSection.objects.get(
                act=act,
                section_number=number
            )
            mapping = SectionMapping.objects.get(ipc_section=ipc_obj)
            mappings.append(mapping)
        except (LegalSection.DoesNotExist, SectionMapping.DoesNotExist):
            continue

    return mappings