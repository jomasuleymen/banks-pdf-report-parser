from transliterate import get_translit_function
from transliterate.base import TranslitLanguagePack, registry


class KazakhLanguagePack(TranslitLanguagePack):
    language_code = "kk"
    language_name = "Kazakh"

    mapping = (
        u"аәбвгғдеёзийкқлмнңоөпрстуұүфхһцъыіьэАӘБВГҒДЕЁЗИЙКҚЛМНҢОӨПРСТУҰҮФХҺЦЪЫІЬЭ",
        u"aabvggdeeziikqlmnnooprstuuufhhc'yi'eAABVGGDEEZIIKQLMNNOOPRSTUUUFHHC'YI'E"
    )

    # TODO
    # reversed_specific_mapping = (
    # )

    # TODO
    # reversed_specific_pre_processor_mapping = {
    # }

    pre_processor_mapping = {
        u"ч": u"ch",
        u"ж": u"zh",
        u"щ": u"sh",
        u"ш": u"sh",
        u"ю": u"iu",
        u"я": u"ia",
        u"Ч": u"Ch",
        u"Ж": u"Zh",
        u"Щ": u"Sh",
        u"Ш": u"Sh",
        u"Ю": u"Iu",
        u"Я": u"Ia",
    }


registry.register(KazakhLanguagePack)

translit_kk = get_translit_function("kk")


def translit(value: str) -> str:
    """Transliterate the text."""
    return translit_kk(value)
