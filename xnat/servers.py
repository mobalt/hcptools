from utils.decorators import classproperty


class Server:
    def __init__(self, host):
        self.host = host

    @classproperty
    def shadow01(cls):
        return cls("hcpi-shadow01.nrg.wustl.edu")

    @classproperty
    def shadow02(cls):
        return cls("hcpi-shadow02.nrg.wustl.edu")

    @classproperty
    def shadow03(cls):
        return cls("hcpi-shadow03.nrg.wustl.edu")

    @classproperty
    def shadow10(cls):
        return cls("hcpi-shadow10.nrg.wustl.edu")

    @classproperty
    def shadow11(cls):
        return cls("hcpi-shadow11.nrg.wustl.edu")

    @classproperty
    def shadow12(cls):
        return cls("hcpi-shadow12.nrg.wustl.edu")

    @classproperty
    def shadow13(cls):
        return cls("hcpi-shadow13.nrg.wustl.edu")

    @classproperty
    def shadow14(cls):
        return cls("hcpi-shadow14.nrg.wustl.edu")

    @classproperty
    def shadow15(cls):
        return cls("hcpi-shadow15.nrg.wustl.edu")

    @classproperty
    def shadow16(cls):
        return cls("hcpi-shadow16.nrg.wustl.edu")

    @classproperty
    def shadow17(cls):
        return cls("hcpi-shadow17.nrg.wustl.edu")

    @classproperty
    def shadow18(cls):
        return cls("hcpi-shadow18.nrg.wustl.edu")

    @classproperty
    def shadow19(cls):
        return cls("hcpi-shadow19.nrg.wustl.edu")

    @classproperty
    def shadow20(cls):
        return cls("hcpi-shadow20.nrg.wustl.edu")

    @classproperty
    def moises1(cls):
        return cls("hcpi-dev-moise1.nrg.wustl.edu")

    @classproperty
    def moises2(cls):
        return cls("hcpi-dev-moise2.nrg.wustl.edu")

    @classproperty
    def moises3(cls):
        return cls("hcpi-dev-moise3.nrg.wustl.edu")

    @classproperty
    def hodge1(cls):
        return cls("hcpi-dev-hodge1.nrg.wustl.edu")

    @classproperty
    def hodge2(cls):
        return cls("hcpi-dev-hodge2.nrg.wustl.edu")
