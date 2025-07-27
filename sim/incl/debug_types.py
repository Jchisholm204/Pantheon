from incl.SuperStruct import SuperStruct
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

    @property
    def datacount(self):
        return self.read_bits(0, 3)

    @datacount.setter
    def datacount(self, value):
        self.write_bits(0, 3, value)

    @property
    def cmderr(self):
        return self.read_bits(8, 10)

    @cmderr.setter
    def cmderr(self, value):
        self.write_bits(8, 10, value)

    @property
    def relaxedpriv(self):
        return self.read_bits(11, 11)

    @relaxedpriv.setter
    def relaxedpriv(self, value):
        self.write_bits(11, 11, value)

    @property
    def busy(self):
        return self.read_bits(12, 12)

    @busy.setter
    def busy(self, value):
        self.write_bits(12, 12, value)

    @property
    def progbufsize(self):
        return self.read_bits(24, 28)

    @progbufsize.setter
    def progbufsize(self, value):
        self.write_bits(24, 28, value)


class command_access_reg_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 32, offset)

    @property
    def regno(self):
        return self.read_bits(0, 15)

    @regno.setter
    def regno(self, value):
        self.write_bits(0, 15, value)

    @property
    def write_en(self):
        return self.read_bits(16, 16)

    @write_en.setter
    def write_en(self, value):
        self.write_bits(16, 16, value)

    @property
    def transfer(self):
        return self.read_bits(17, 17)

    @transfer.setter
    def transfer(self, value):
        self.write_bits(17, 17, value)

    @property
    def postexec(self):
        return self.read_bits(18, 18)

    @postexec.setter
    def postexec(self, value):
        self.write_bits(18, 18, value)

    @property
    def aarpostincrement(self):
        return self.read_bits(19, 19)

    @aarpostincrement.setter
    def aarpostincrement(self, value):
        self.write_bits(19, 19, value)

    @property
    def aarsize(self):
        return self.read_bits(20, 22)

    @aarsize.setter
    def aarsize(self, value):
        self.write_bits(20, 22, value)

    @property
    def cmdtype(self):
        return self.read_bits(24, 31)

    @cmdtype.setter
    def cmdtype(self, value):
        self.write_bits(24, 31)


class command_quick_access_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 32, offset)

    @property
    def cmdtype(self):
        return self.read_bits(24, 31)

    @cmdtype.setter
    def cmdtype(self, value):
        self.write_bits(24, 31)


class command_access_mem_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 32, offset)

    @property
    def target_specific(self):
        return self.read_bits(14, 15)

    @target_specific.setter
    def target_specific(self, value):
        self.write_bits(14, 15, value)

    @property
    def write_en(self):
        return self.read_bits(16, 16)

    @write_en.setter
    def write_en(self, value):
        self.write_bits(16, 16, value)

    @property
    def aampostincrement(self):
        return self.read_bits(19, 19)

    @aampostincrement.setter
    def aampostincrement(self, value):
        self.write_bits(19, 19, value)

    @property
    def aamsize(self):
        return self.read_bits(20, 22)

    @aamsize.setter
    def aamsize(self, value):
        self.write_bits(20, 22, value)

    @property
    def aamvirtual(self):
        return self.read_bits(23, 23)

    @aamvirtual.setter
    def aamvirtual(self, value):
        self.write_bits(23, 23, value)

    @property
    def cmdtype(self):
        return self.read_bits(24, 31)

    @cmdtype.setter
    def cmdtype(self, value):
        self.write_bits(24, 31, value)


class command_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 32, offset)
        self.acc_reg = command_access_reg_t(self)
        self.qa = command_quick_access_t(self)
        self.acc_mem = command_access_mem_t(self)


class sbcs_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 32, offset)

    @property
    def access8(self):
        return self.read_bits(0, 0)

    @access8.setter
    def access8(self, value):
        self.write_bits(0, 0, value)

    @property
    def access16(self):
        return self.read_bits(1, 1)

    @access16.setter
    def access16(self, value):
        self.write_bits(1, 1, value)

    @property
    def access32(self):
        return self.read_bits(2, 2)

    @access32.setter
    def access32(self, value):
        self.write_bits(2, 2, value)

    @property
    def access64(self):
        return self.read_bits(3, 3)

    @access64.setter
    def access64(self, value):
        self.write_bits(3, 3, value)

    @property
    def access128(self):
        return self.read_bits(4, 4)

    @access128.setter
    def access128(self, value):
        self.write_bits(4, 4, value)

    @property
    def size(self):
        return self.read_bits(5, 11)

    @size.setter
    def size(self, value):
        self.write_bits(15, 11)

    @property
    def error(self):
        return self.read_bits(12, 14)

    @error.setter
    def error(self, value):
        self.write_bits(12, 14, value)

    @property
    def readondata(self):
        return self.read_bits(15, 15)

    @readondata.setter
    def readondata(self, value):
        self.write_bits(15, 15, value)

    @property
    def autoincrement(self):
        return self.read_bits(16, 16)

    @autoincrement.setter
    def autoincrement(self, value):
        self.write_bits(16, 16, value)

    @property
    def access(self):
        return self.read_bits(17, 19)

    @access.setter
    def access(self, value):
        self.write_bits(17, 19, value)

    @property
    def readonaddr(self):
        return self.read_bits(20, 20)

    @readonaddr.setter
    def readonaddr(self, value):
        self.write_bits(20, 20, value)

    @property
    def busy(self):
        return self.read_bits(21, 21)

    @busy.setter
    def busy(self, value):
        self.write_bits(21, 21, value)

    @property
    def busyerror(self):
        return self.read_bits(22, 22)

    @busyerror.setter
    def busyerror(self, value):
        self.write_bits(22, 22, value)

    @property
    def version(self):
        return self.read_bits(29, 31)

    @version.setter
    def version(self, value):
        self.write_bits(29, 31, value)


class debug_type_t(SuperStruct):
    def __init__(self, parent, offset=0):
        super().__init__(parent, 32, offset)
        self.dmcontrol = dmcontrol_t(self)
        self.dmstatus = dmstatus_t(self)
        self.abstractcs = abstractcs_t(self)
        self.command = command_t(self)
        self.sbcs = sbcs_t(self)
