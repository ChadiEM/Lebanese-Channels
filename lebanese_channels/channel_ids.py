from lebanese_channels.services.future import Future
from lebanese_channels.services.jadeed import Jadeed
from lebanese_channels.services.lb2 import LB2
from lebanese_channels.services.lbc import LBC
from lebanese_channels.services.lbcsports import LBCSports
from lebanese_channels.services.manar import Manar
from lebanese_channels.services.mtv import MTV
from lebanese_channels.services.nbn import NBN
from lebanese_channels.services.noursat import Noursat
from lebanese_channels.services.otv import OTV

CHANNEL_LIST = [
    LBC(),
    LB2(),
    MTV(),
    OTV(),
    Jadeed(),
    Future(),
    NBN(),
    Manar(),
    Noursat(),
    LBCSports()
]
