from enum import Enum
from typing import Union

LocaleLike = Union['Locale', str]


# https://discord.com/developers/docs/reference#locales
class Locale(str, Enum):
    BG = 'bg'
    """ Bulgarian """

    CS = 'cs'
    """ Czech """

    DA = 'da'
    """ Danish """

    DE = 'de'
    """ German """

    EL = 'el'
    """ Greek """

    EN_GB = 'en-GB'
    """ English, UK """

    EN_US = 'en-US'
    """ English, US """

    ES_ES = 'es-ES'
    """ Spanish """

    FI = 'fi'
    """ Finnish """

    FR = 'fr'
    """ French """

    HI = 'hi'
    """ Hindi """

    HR = 'hr'
    """ Croatian """

    HU = 'hu'
    """ Hungarian """

    IT = 'it'
    """ Italian """

    JA = 'ja'
    """ Japanese """

    KO = 'ko'
    """ Korean """

    LT = 'lt'
    """ Lithuanian """

    NL = 'nl'
    """ Dutch """

    NO = 'no'
    """ Norwegian """

    PL = 'pl'
    """ Polish """

    PT_BR = 'pt-BR'
    """ Portuguese, Brazilian """

    RO = 'ro'
    """ Romanian, Romania """

    RU = 'ru'
    """ Russian """

    SV_SE = 'sv-SE'
    """ Swedish """

    TH = 'th'
    """ Thai """

    TR = 'tr'
    """ Turkish """

    UK = 'uk'
    """ Ukrainian """

    VI = 'vi'
    """ Vietnamese """

    ZH_CN = 'zh-CN'
    """ Chinese, China """

    ZH_TW = 'zh-TW'
    """ Chinese, Taiwan """

    # Aliases
    BULGARIAN = BG
    CZECH = CS
    DANISH = DA
    GERMAN = DE
    GREEK = EL
    ENGLISH_UK = EN_GB
    ENGLISH_US = EN_US
    SPANISH = ES_ES
    FINNISH = FI
    FRENCH = FR
    HINDI = HI
    CROATIAN = HR
    HUNGARIAN = HU
    ITALIAN = IT
    JAPANESE = JA
    KOREAN = KO
    LITHUANIAN = LT
    DUTCH = NL
    NORWEGIAN = NO
    POLISH = PL
    PORTUGUESE_BRAZILIAN = PT_BR
    ROMANIAN_ROMANIA = RO
    RUSSIAN = RU
    SWEDISH = SV_SE
    THAI = TH
    TURKISH = TR
    UKRAINIAN = UK
    VIETNAMESE = VI
    CHINESE_CHINA = ZH_CN
    CHINESE_TAIWAN = ZH_TW

    @classmethod
    def is_valid(cls, value: LocaleLike) -> bool:
        try:
            return cls(value) in cls
        except ValueError:
            return False
