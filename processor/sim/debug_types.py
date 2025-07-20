from SuperStruct import SuperStruct
from cocotb.handle import ModifiableObject


class dmcontrol_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 32, offset)

    @property
    def active(self):
        return self.read_bits(0, 0)

    @active.setter
    def active(self, value):
        self.write_bits(0, 0, value)

    @property
    def reset(self):
        return self.read_bits(1, 1)

    @reset.setter
    def reset(self, value):
        self.write_bits(1, 1, value)

    @property
    def clrresethaltreq(self):
        return self.read_bits(2, 2)

    @clrresethaltreq.setter
    def clrresethaltreq(self, value):
        self.write_bits(2, 2, value)

    @property
    def setresethaltreq(self):
        return self.read_bits(3, 3)

    @setresethaltreq.setter
    def setresethaltreq(self, value):
        self.write_bits(3, 3, value)

    @property
    def clrkeepalive(self):
        return self.read_bits(4, 4)

    @clrkeepalive.setter
    def clrkeepalive(self, value):
        return self.write_bits(4, 4, value)

    @property
    def setkeepalive(self):
        return self.read_bits(5, 5)

    @setkeepalive.setter
    def setkeepalive(self, value):
        return self.write_bits(5, 5, value)

    @property
    def heartselhi(self):
        return self.read_bits(6, 15)

    @heartselhi.setter
    def heartselhi(self, value):
        self.write_bits(6, 15, value)

    @property
    def heartsello(self):
        return self.read_bits(16, 25)

    @heartsello.setter
    def heartsello(self, value):
        self.write_bits(16, 25, value)

    @property
    def hasel(self):
        return self.read_bits(26, 26)

    @hasel.setter
    def hasel(self, value):
        self.write_bits(26, 26, value)

    @property
    def ackunavail(self):
        return self.read_bits(27, 27)

    @ackunavail.setter
    def ackunavail(self, value):
        self.write_bits(27, 27, value)

    @property
    def ackhavereset(self):
        return self.read_bits(28, 28)

    @ackhavereset.setter
    def ackhavereset(self, value):
        self.write_bits(28, 28, value)

    @property
    def heartreset(self):
        return self.read_bits(29, 29)

    @heartreset.setter
    def heartreset(self, value):
        self.write_bits(29, 29, value)

    @property
    def resumereq(self):
        return self.read_bits(30, 30)

    @resumereq.setter
    def resumereq(self, value):
        self.write_bits(30, 30, value)

    @property
    def haltreq(self):
        return self.read_bits(31, 31)

    @haltreq.setter
    def haltreq(self, value):
        self.write_bits(31, 31, value)


class dmstatus_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 32, offset)

    @property
    def version(self):
        return self.read_bits(0, 3)

    @version.setter
    def version(self, value):
        self.write_bits(0, 3, value)

    @property
    def confstrptrvalid(self):
        return self.read_bits(4, 4)

    @property
    def hasresethaltreq(self):
        return self.read_bits(5, 5)

    @hasresethaltreq.setter
    def hasresethaltreq(self, value):
        self.write_bits(5, 5, value)

    @property
    def authbusy(self):
        return self.read_bits(6, 6)

    @authbusy.setter
    def authbusy(self, value):
        self.write_bits(6, 6, value)

    @property
    def authenticated(self):
        return self.read_bits(7, 7)

    @authenticated.setter
    def authenticated(self, value):
        self.write_bits(7, 7, value)

    @property
    def anyhalted(self):
        return self.read_bits(8, 8)

    @anyhalted.setter
    def anyhalted(self, value):
        self.write_bits(8, 8, value)

    @property
    def allhalted(self):
        return self.read_bits(9, 9)

    @allhalted.setter
    def allhalted(self, value):
        self.write_bits(9, 9, value)

    @property
    def anyrunning(self):
        return self.read_bits(10, 10)

    @anyrunning.setter
    def anyrunning(self, value):
        self.write_bits(10, 10, value)

    @property
    def allrunning(self):
        return self.read_bits(11, 11)

    @allrunning.setter
    def allrunning(self, value):
        self.write_bits(11, 11, value)

    @property
    def anyunavail(self):
        return self.read_bits(12, 12)

    @anyunavail.setter
    def anyunavail(self, value):
        self.write_bits(12, 12, value)

    @property
    def allunavail(self):
        return self.read_bits(13, 13)

    @allunavail.setter
    def allunavail(self, value):
        self.write_bits(13, 13, value)

    @property
    def anynonexistent(self):
        return self.read_bits(14, 14)

    @anynonexistent.setter
    def anynonexistent(self, value):
        self.write_bits(14, 14, value)

    @property
    def allnonexistent(self):
        return self.read_bits(15, 15)

    @allnonexistent.setter
    def allnonexistent(self, value):
        self.write_bits(15, 15, value)

    @property
    def anyresumeack(self):
        return self.read_bits(16, 16)

    @anyresumeack.setter
    def anyresumeack(self, value):
        self.write_bits(16, 16, value)

    @property
    def allresumeack(self):
        return self.read_bits(17, 17)

    @allresumeack.setter
    def allresumeack(self, value):
        self.write_bits(17, 17, value)

    @property
    def anyhavereset(self):
        return self.read_bits(18, 18)

    @anyhavereset.setter
    def anyresumeack(self, value):
        self.write_bits(18, 18, value)

    @property
    def allhavereset(self):
        return self.read_bits(19, 19)

    @allhavereset.setter
    def allhavereset(self, value):
        self.write_bits(19, 19, value)

    @property
    def impebreak(self):
        return self.read_bits(22, 22)

    @impebreak.setter
    def impebreak(self, value):
        self.write_bits(22, 22, value)

    @property
    def stickyunavail(self):
        return self.read_bits(23, 23)

    @stickyunavail.setter
    def stickyunavail(self, value):
        self.write_bits(23, 23, value)

    @property
    def ndmresetpending(self):
        return self.read_bits(24, 24)

    @ndmresetpending.setter
    def ndmresetpending(self, value):
        self.write_bits(24, 24, value)


class abstractcs_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 32, offset)
